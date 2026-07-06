"""Pure, deterministic JSON -> OpenAPI 3.0 schema inference.

No LLMs, no network calls: payloads never leave the machine.

The output is a minimal OpenAPI 3.0.0 document (the format SAP Integration
Suite actually accepts), not a standalone JSON Schema draft file. Each action
becomes a path whose request body references an inferred schema under
``components/schemas``. In Integration Suite the request/response distinction
is irrelevant for mappings: you simply pick whichever message structure fits
your purpose, so every action is modelled as a request.

Design decisions (deliberate, for integration/mapping use cases):
- Nothing is marked as ``required`` unless the user opts in, and even then only
  fields present in *all* provided samples of an action are marked required.
- ``additionalProperties`` is never set to ``false``.
- Types are inferred from the actual JSON values and merged across samples.
  OpenAPI 3.0 does not allow union types (``["string", "null"]``), so null is
  expressed as ``nullable: true`` and mixed-type fields are left unconstrained
  (with a warning).
"""

import re

ISO_DATETIME_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}[Tt ]\d{2}:\d{2}:\d{2}(\.\d+)?([Zz]|[+-]\d{2}:?\d{2})?$"
)
ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def infer_node(value, options, warnings, path):
    """Infer an internal schema node ({"type": set(), ...}) for a JSON value."""
    if value is None:
        return {"type": {"null"}}
    if isinstance(value, bool):
        return {"type": {"boolean"}}
    if isinstance(value, int):
        if options.get("widen_integers"):
            return {"type": {"number"}}
        return {"type": {"integer"}}
    if isinstance(value, float):
        return {"type": {"number"}}
    if isinstance(value, str):
        node = {"type": {"string"}}
        if options.get("detect_formats"):
            if ISO_DATETIME_RE.match(value):
                node["format"] = "date-time"
            elif ISO_DATE_RE.match(value):
                node["format"] = "date"
        return node
    if isinstance(value, list):
        if not value:
            warnings.append(("empty_array", path))
            return {"type": {"array"}}
        items = None
        for element in value:
            items = merge_nodes(items, infer_node(element, options, warnings, path + "[*]"))
        return {"type": {"array"}, "items": items}
    if isinstance(value, dict):
        properties = {
            key: infer_node(val, options, warnings, f"{path}.{key}")
            for key, val in value.items()
        }
        return {
            "type": {"object"},
            "properties": properties,
            "required": set(value.keys()),
        }
    # Unreachable for values coming from json.loads, but fail loudly if not.
    raise TypeError(f"Unsupported JSON value at {path}: {type(value)!r}")


def merge_nodes(a, b):
    """Merge two internal schema nodes (e.g. from two samples of one action)."""
    if a is None:
        return b
    if b is None:
        return a
    merged = {"type": set(a["type"]) | set(b["type"])}
    if {"integer", "number"} <= merged["type"]:
        merged["type"].discard("integer")

    if "properties" in a or "properties" in b:
        props_a = a.get("properties", {})
        props_b = b.get("properties", {})
        merged["properties"] = {
            key: merge_nodes(props_a.get(key), props_b.get(key))
            for key in {**props_a, **props_b}
        }
        # A field is only a "required" candidate if every sample contains it.
        # A missing "required" set means the node wasn't an object in that
        # sample, so no field can be required across both.
        merged["required"] = a.get("required", set()) & b.get("required", set())

    items = merge_nodes(a.get("items"), b.get("items"))
    if items is not None:
        merged["items"] = items

    if a.get("format") and a.get("format") == b.get("format"):
        merged["format"] = a["format"]
    return merged


def render_node(node, options, warnings, path):
    """Convert an internal node into an OpenAPI 3.0-flavoured schema dict."""
    types = set(node["type"])
    nullable = "null" in types
    types.discard("null")
    if not types:
        # A field that was always null gives no type information; default to
        # a nullable string rather than leaving it typeless.
        warnings.append(("null_only", path))
        types = {"string"}

    schema = {}
    if len(types) == 1:
        schema["type"] = next(iter(types))
    else:
        # OpenAPI 3.0 cannot express union types; leave the field
        # unconstrained and let the user decide.
        warnings.append(("mixed_types", path))
    if nullable:
        schema["nullable"] = True
    if node.get("format"):
        schema["format"] = node["format"]
    if "properties" in node:
        schema["properties"] = {
            key: render_node(child, options, warnings, f"{path}.{key}")
            for key, child in sorted(node["properties"].items())
        }
        if options.get("require_common") and node.get("required"):
            required = sorted(node["required"])
            # Only keys still present in properties (defensive ordering).
            schema["required"] = [k for k in required if k in schema["properties"]]
    if "array" in types:
        if node.get("items") is not None:
            schema["items"] = render_node(node["items"], options, warnings, f"{path}[*]")
        else:
            schema["items"] = {}
    return schema


def build_definition(samples, options, warnings, base_path):
    """Build the JSON Schema for one action from one or more JSON samples."""
    node = None
    for sample in samples:
        node = merge_nodes(node, infer_node(sample, options, warnings, base_path))
    return render_node(node, options, warnings, base_path)


def build_openapi_document(actions, title, description):
    """Combine per-action schemas into a minimal OpenAPI 3.0.0 document.

    ``actions`` maps a sanitized name to ``{"schema": ..., "verb": ...,
    "summary": ...}``. Every action is modelled as the request body of its own
    path. The 200 response carries no content: OpenAPI 3.0 requires the
    ``responses`` key to be present, but leaving it schema-less means the
    request is the only message structure in the document (no duplicates to
    choose from in Integration Suite).
    """
    paths = {}
    schemas = {}
    for name, action in actions.items():
        schemas[name] = action["schema"]
        paths[f"/{name}"] = {
            action["verb"].lower(): {
                "summary": action["summary"],
                "tags": [name],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": f"#/components/schemas/{name}"}
                        }
                    },
                },
                "responses": {"200": {"description": "Successful response"}},
            }
        }
    return {
        "openapi": "3.0.0",
        "info": {
            "title": title,
            "version": "1.0.0",
            "description": description,
        },
        "x-sap-api-type": "REST",
        "servers": [
            {
                "url": "https://{host}:{port}/http/YourEndpointHere",
                "variables": {
                    "host": {"default": "The URL of your runtime here"},
                    "port": {"default": "443"},
                },
            }
        ],
        "paths": paths,
        "components": {"schemas": schemas},
    }


def sanitize_name(name, fallback):
    """Make an action name safe to use as a definition key / JSON pointer."""
    cleaned = re.sub(r"[^0-9A-Za-z_\-]", "_", name.strip())
    cleaned = re.sub(r"_+", "_", cleaned).strip("_")
    return cleaned or fallback
