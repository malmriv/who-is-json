"""Minimal English/Spanish string table for the UI."""

STRINGS = {
    "lang_toggle": {
        "en": "🇪🇸",
        "es": "🇬🇧",
    },
    "lang_toggle_help": {
        "en": "Cambiar a español",
        "es": "Switch to English",
    },
    "app_title": {
        "en": "who is json? 🤨",
        "es": "who is json? 🤨",
    },
    "app_title_help": {
        "en": "and why does it need a schema?",
        "es": "¿y por qué necesita un esquema?",
    },
    "app_caption": {
        "en": (
            "Paste one or more sample JSON messages and get a single JSON Schema, "
            "ready to use in SAP Integration Suite message mappings (or any other "
            "JSON Schema-aware platform). Everything runs locally: your payloads "
            "never leave this machine."
        ),
        "es": (
            "Pega uno o varios mensajes JSON de ejemplo y obtén un único JSON Schema, "
            "listo para usar en los message mappings de SAP Integration Suite (o en "
            "cualquier otra plataforma compatible con JSON Schema). Todo se ejecuta en "
            "local: tus mensajes nunca salen de esta máquina."
        ),
    },
    "settings": {"en": "Settings", "es": "Configuración"},
    "draft_label": {"en": "JSON Schema draft", "es": "Versión (draft) de JSON Schema"},
    "draft_help": {
        "en": "draft-04 is the safest choice for SAP Integration Suite message mappings.",
        "es": "draft-04 es la opción más segura para los message mappings de SAP Integration Suite.",
    },
    "schema_title_label": {"en": "Schema title", "es": "Título del esquema"},
    "require_common": {
        "en": "Mark fields present in ALL samples as required",
        "es": "Marcar como obligatorios los campos presentes en TODAS las muestras",
    },
    "require_common_help": {
        "en": (
            "Off by default: for mappings it is usually safer to keep every field "
            "optional, so the schema never rejects a valid-but-sparse message."
        ),
        "es": (
            "Desactivado por defecto: para los mappings suele ser más seguro dejar "
            "todos los campos opcionales, de modo que el esquema nunca rechace un "
            "mensaje válido aunque incompleto."
        ),
    },
    "detect_formats": {
        "en": "Detect date/time formats",
        "es": "Detectar formatos de fecha/hora",
    },
    "detect_formats_help": {
        "en": "Adds 'format: date-time' / 'format: date' to ISO 8601-looking strings.",
        "es": "Añade 'format: date-time' / 'format: date' a las cadenas con aspecto ISO 8601.",
    },
    "widen_integers": {
        "en": "Treat all integers as number",
        "es": "Tratar todos los enteros como number",
    },
    "widen_integers_help": {
        "en": (
            "Safer when a field that looks like an integer in your sample "
            "(e.g. 5) may carry decimals in real traffic (e.g. 5.5)."
        ),
        "es": (
            "Más seguro cuando un campo que parece entero en tu ejemplo "
            "(p. ej. 5) puede llevar decimales en tráfico real (p. ej. 5.5)."
        ),
    },
    "actions_header": {"en": "Actions", "es": "Acciones"},
    "actions_caption": {
        "en": (
            "Each action becomes a definition in the schema (one per mapping). "
            "Add several samples to the same action to merge them: fields seen in "
            "any sample are included, and types are widened (e.g. string + null)."
        ),
        "es": (
            "Cada acción se convierte en una definición del esquema (una por mapping). "
            "Añade varias muestras a la misma acción para fusionarlas: se incluyen los "
            "campos vistos en cualquier muestra y los tipos se amplían (p. ej. string + null)."
        ),
    },
    "action_title": {"en": "Action {n}", "es": "Acción {n}"},
    "action_name": {"en": "Action name", "es": "Nombre de la acción"},
    "action_name_placeholder": {"en": "e.g. CreateOrder", "es": "p. ej. CrearPedido"},
    "http_verb": {"en": "HTTP verb", "es": "Verbo HTTP"},
    "sample_label": {"en": "Sample JSON #{n}", "es": "JSON de ejemplo n.º {n}"},
    "sample_placeholder": {
        "en": '{"orderId": 1042, "customer": {"name": "ACME"}, "items": [...]}',
        "es": '{"idPedido": 1042, "cliente": {"nombre": "ACME"}, "lineas": [...]}',
    },
    "add_sample": {"en": "➕ Add sample", "es": "➕ Añadir muestra"},
    "remove_sample": {"en": "➖ Remove last sample", "es": "➖ Quitar última muestra"},
    "add_action": {"en": "➕ Add action", "es": "➕ Añadir acción"},
    "remove_action": {"en": "🗑️ Remove this action", "es": "🗑️ Eliminar esta acción"},
    "generate": {"en": "⚙️ Generate JSON Schema", "es": "⚙️ Generar JSON Schema"},
    "output_header": {"en": "Generated schema", "es": "Esquema generado"},
    "download": {"en": "⬇️ Download schema", "es": "⬇️ Descargar esquema"},
    "warnings_header": {"en": "Warnings", "es": "Avisos"},
    "err_parse": {
        "en": "Action '{action}', sample {n}: invalid JSON — {msg}",
        "es": "Acción '{action}', muestra {n}: JSON no válido — {msg}",
    },
    "warn_action_skipped": {
        "en": "Action '{action}' has no valid samples and was skipped.",
        "es": "La acción '{action}' no tiene muestras válidas y se ha omitido.",
    },
    "err_no_actions": {
        "en": "Nothing to generate: add at least one action with a valid JSON sample.",
        "es": "Nada que generar: añade al menos una acción con un JSON de ejemplo válido.",
    },
    "warn_null_only": {
        "en": (
            "'{path}' was always null in the samples; its type defaulted to "
            "[string, null]. Adjust it in the output if needed."
        ),
        "es": (
            "'{path}' siempre era null en las muestras; su tipo se ha fijado a "
            "[string, null]. Ajústalo en el resultado si es necesario."
        ),
    },
    "warn_empty_array": {
        "en": (
            "'{path}' was always an empty array in the samples, so the item type "
            "is unknown (left as an unconstrained object)."
        ),
        "es": (
            "'{path}' siempre era un array vacío en las muestras, por lo que el tipo "
            "de sus elementos es desconocido (se deja sin restricciones)."
        ),
    },
    "warn_duplicate_name": {
        "en": "Duplicate action name '{name}' renamed to '{renamed}'.",
        "es": "Nombre de acción duplicado '{name}', renombrado a '{renamed}'.",
    },
    "verb_description": {
        "en": "{verb} — {name}",
        "es": "{verb} — {name}",
    },
}


def t(key, lang, **kwargs):
    text = STRINGS[key][lang]
    return text.format(**kwargs) if kwargs else text
