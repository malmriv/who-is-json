# who is json? 🤨

> *"who is json?" — every vibecoder, at some point.*

(The name is a joke: this particular tool was 100% vibecoded to solve a
recurring problem; I see no benefit in spending hours of
[yak-shaving](https://en.wiktionary.org/wiki/yak_shaving) to hand-craft an
automation for something that would take me half as long to do manually.)

<p align="center">
  <img src="assets/xkcd_1319_automation.png" alt="xkcd 1319: Automation. Theory: automating a task frees you from it. Reality: ongoing development leaves no time for the original task.">
  <br>
  <em><a href="https://xkcd.com/1319/">"Automation"</a> by Randall Munroe (xkcd), licensed under <a href="https://creativecommons.org/licenses/by-nc/2.5/">CC BY-NC 2.5</a>.</em>
</p>

Generate a **JSON Schema** from one or more sample JSON messages, ready to use in
**SAP Integration Suite** message mappings (or any other platform that consumes
JSON Schema). It solves a common pain: there is usually no way to obtain a JSON
schema for a given payload, and hand-writing one for every mapping wastes a
significant part of the day.

This is *not* an OpenAPI generator: it produces a plain, reusable JSON Schema
focused on message mappings, not endpoints.

**Everything runs locally and is purely algorithmic (no LLMs, no network calls),
so confidential payloads never leave your machine and results are deterministic.**

## Features

- **Multiple actions in a single schema file.** Each action (e.g. `CreateOrder`,
  `UpdateOrder`) has a name and an HTTP verb (metadata only, kept as the
  definition's `description`) and becomes an entry under `definitions`, exposed
  at the root via `$ref`. One schema file can then be reused across as many
  mappings as needed.
- **Multiple samples per action.** Samples of the same message are merged:
  fields seen in *any* sample are included, and types are widened
  (e.g. `"type": ["string", "null"]`, `integer` + `number` → `number`).
- **Loose cardinality by default.** No field is marked `required` and
  `additionalProperties` is never set to `false`, so the schema won't reject a
  valid-but-sparse message. An opt-in setting marks fields present in *all*
  samples as required.
- **Faithful types.** Strings, booleans, integers, numbers, objects, arrays and
  nulls are inferred from the actual values. Optional helpers: detect ISO 8601
  date/date-time formats, or widen all integers to `number`.
- **Warnings** for fields whose type can't be known (always-`null` values,
  always-empty arrays) so you can adjust them consciously.
- **Draft selector.** `draft-04` by default (the safest choice for SAP
  Integration Suite), `draft-07` available.
- **Bilingual UI.** One-click toggle between English and Spanish.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Run with Docker

```bash
docker build -t who-is-json .
docker run -p 8501:8501 who-is-json
```

Then open http://localhost:8501.
