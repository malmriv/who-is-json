import json

import streamlit as st

from i18n import t
from schema_inference import (
    build_definition,
    build_root_schema,
    sanitize_name,
)

HTTP_VERBS = ["POST", "GET", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"]

st.set_page_config(
    page_title="who is json?",
    page_icon="🤨",
    layout="wide",
)

# ---------------------------------------------------------------- state
if "lang" not in st.session_state:
    st.session_state.lang = "en"
if "actions" not in st.session_state:
    # Each entry: {"id": stable widget key, "n_samples": number of text areas}
    st.session_state.actions = [{"id": 0, "n_samples": 1}]
    st.session_state.next_id = 1


def _(key, **kwargs):
    return t(key, st.session_state.lang, **kwargs)


# ---------------------------------------------------------------- sidebar
with st.sidebar:
    if st.button(_("lang_toggle"), help=_("lang_toggle_help")):
        st.session_state.lang = "es" if st.session_state.lang == "en" else "en"
        st.rerun()

    st.header(_("settings"))
    draft = st.selectbox(
        _("draft_label"), ["draft-04", "draft-07"], index=0, help=_("draft_help")
    )
    schema_title = st.text_input(_("schema_title_label"), value="IntegrationMessages")
    require_common = st.checkbox(
        _("require_common"), value=False, help=_("require_common_help")
    )
    detect_formats = st.checkbox(
        _("detect_formats"), value=True, help=_("detect_formats_help")
    )
    widen_integers = st.checkbox(
        _("widen_integers"), value=False, help=_("widen_integers_help")
    )

options = {
    "require_common": require_common,
    "detect_formats": detect_formats,
    "widen_integers": widen_integers,
}

# ---------------------------------------------------------------- main
st.title(_("app_title"), help=_("app_title_help"))
st.caption(_("app_caption"))

st.subheader(_("actions_header"))
st.caption(_("actions_caption"))

action_to_remove = None
for idx, action in enumerate(st.session_state.actions, start=1):
    aid = action["id"]
    default_name = st.session_state.get(f"name_{aid}", "")
    label = default_name.strip() or _("action_title", n=idx)
    with st.expander(f"**{label}**", expanded=True):
        col_name, col_verb = st.columns([3, 1])
        with col_name:
            st.text_input(
                _("action_name"),
                key=f"name_{aid}",
                placeholder=_("action_name_placeholder"),
            )
        with col_verb:
            st.selectbox(_("http_verb"), HTTP_VERBS, key=f"verb_{aid}")

        for s in range(action["n_samples"]):
            st.text_area(
                _("sample_label", n=s + 1),
                key=f"sample_{aid}_{s}",
                height=180,
                placeholder=_("sample_placeholder"),
            )

        col_add, col_del_sample, col_del_action = st.columns([1, 1, 1])
        with col_add:
            if st.button(_("add_sample"), key=f"add_sample_{aid}"):
                action["n_samples"] += 1
                st.rerun()
        with col_del_sample:
            if action["n_samples"] > 1 and st.button(
                _("remove_sample"), key=f"del_sample_{aid}"
            ):
                action["n_samples"] -= 1
                st.rerun()
        with col_del_action:
            if len(st.session_state.actions) > 1 and st.button(
                _("remove_action"), key=f"del_action_{aid}"
            ):
                action_to_remove = aid

if action_to_remove is not None:
    st.session_state.actions = [
        a for a in st.session_state.actions if a["id"] != action_to_remove
    ]
    st.rerun()

if st.button(_("add_action")):
    st.session_state.actions.append(
        {"id": st.session_state.next_id, "n_samples": 1}
    )
    st.session_state.next_id += 1
    st.rerun()

st.divider()

# ---------------------------------------------------------------- generation
if st.button(_("generate"), type="primary"):
    errors = []
    warnings = []  # translated strings
    infer_warnings = []  # (kind, path) tuples from the inference engine
    definitions = {}

    for idx, action in enumerate(st.session_state.actions, start=1):
        aid = action["id"]
        raw_name = st.session_state.get(f"name_{aid}", "").strip() or f"Action{idx}"
        verb = st.session_state.get(f"verb_{aid}", "POST")
        name = sanitize_name(raw_name, f"Action{idx}")
        if name in definitions:
            renamed = f"{name}_{idx}"
            warnings.append(_("warn_duplicate_name", name=name, renamed=renamed))
            name = renamed

        samples = []
        for s in range(action["n_samples"]):
            raw = st.session_state.get(f"sample_{aid}_{s}", "").strip()
            if not raw:
                continue
            try:
                samples.append(json.loads(raw))
            except json.JSONDecodeError as exc:
                errors.append(_("err_parse", action=raw_name, n=s + 1, msg=exc))

        if not samples:
            warnings.append(_("warn_action_skipped", action=raw_name))
            continue

        definition = build_definition(samples, options, infer_warnings, name)
        definition["description"] = _("verb_description", verb=verb, name=raw_name)
        definitions[name] = definition

    for kind, path in infer_warnings:
        if kind == "null_only":
            warnings.append(_("warn_null_only", path=path))
        elif kind == "empty_array":
            warnings.append(_("warn_empty_array", path=path))

    for error in errors:
        st.error(error)

    if definitions:
        schema = build_root_schema(
            definitions, draft, schema_title.strip() or "IntegrationMessages"
        )
        schema_text = json.dumps(schema, indent=2, ensure_ascii=False)

        if warnings:
            with st.expander(f"⚠️ {_('warnings_header')} ({len(warnings)})"):
                for warning in warnings:
                    st.warning(warning)

        st.subheader(_("output_header"))
        st.download_button(
            _("download"),
            data=schema_text,
            file_name=f"{schema.get('title', 'schema')}.schema.json",
            mime="application/json",
        )
        st.code(schema_text, language="json")
    elif not errors:
        st.error(_("err_no_actions"))
