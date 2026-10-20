# Changelog

## v0.1.0 — 2026-10-20

Initial reproducible prototype of time-series-storytelling Skill + Runtime.

- Strict `date,value` CSV ingestion, no silent sorting/deduplication/imputation, source hash binding.
- Heuristic narrative archetypes: Trend, Regime Shift, Anomaly, and a no-clear-pattern fallback.
- JSON Story Spec with six timed beats, evidence references and validation gates.
- Deterministic `frame(t)` renderer and observation-driven synthesized audio; FFmpeg MP4 output.
- Three synthetic examples producing films, plus an uneventful control fixture.
- 29 local tests, with CI and end-to-end render smoke test.

Known limitations and validation scope are documented in `README.md` and `ACCEPTANCE.md`.
