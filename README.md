# who is json? 🤨

> *"who is json?" — every vibecoder, at some point.*

(The name is a joke: **this particular tool was almost 100% vibecoded** to solve a
recurring problem; I see no benefit in spending hours of
[yak-shaving](https://en.wiktionary.org/wiki/yak_shaving) to hand-craft an
automation for something that would take me half as long to do manually.)

<p align="center">
  <img src="assets/xkcd_1319_automation.png" alt="xkcd 1319: Automation. Theory: automating a task frees you from it. Reality: ongoing development leaves no time for the original task.">
  <br>
  <em><a href="https://xkcd.com/1319/">"Automation"</a> by Randall Munroe (xkcd), licensed under <a href="https://creativecommons.org/licenses/by-nc/2.5/">CC BY-NC 2.5</a>.</em>
</p>

Generate message schemas from one or more sample JSON messages, packaged as a
minimal **OpenAPI 3.0 document** in the exact format **SAP Integration Suite**
accepts. It solves a common pain: there is usually no way to obtain a schema
for a given payload, and hand-writing one for every mapping wastes a
significant part of the day.

This is *not* a full-blown OpenAPI generator: the document is just the thin
wrapper Integration Suite requires around the message schemas. In IS the
request/response distinction is irrelevant for mappings — you simply pick
whichever message structure fits your purpose — so every action is modelled
as a request.

**Everything runs locally and is purely algorithmic (no LLMs or external calls),
so confidential payloads never leave your machine and results are deterministic.**

## Features

- **Multiple actions in a single document.** Each action (e.g. `CreateOrder`,
  `UpdateOrder`) has a name and an HTTP verb and becomes a path in the document,
  with its inferred schema under `components/schemas`. One file can then be
  reused across as many mappings as needed.
- **Multiple samples per action.** Samples of the same message are merged:
  fields seen in *any* sample are included, and types are widened
  (e.g. `nullable: true`, `integer` + `number` → `number`).
- **Loose cardinality by default.** No field is marked `required` and
  `additionalProperties` is never set to `false`, so the schema won't reject a
  valid-but-sparse message. An opt-in setting marks fields present in *all*
  samples as required.
- **Faithful types.** Strings, booleans, integers, numbers, objects, arrays and
  nulls are inferred from the actual values. Optional helpers: detect ISO 8601
  date/date-time formats, or widen all integers to `number`.
- **Warnings** for fields whose type can't be known (always-`null` values,
  always-empty arrays, mixed types) so you can adjust them consciously.
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
