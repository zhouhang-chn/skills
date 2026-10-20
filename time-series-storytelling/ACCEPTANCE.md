# MVP Acceptance — 2026-10-20

Scope: rule-based plan + deterministic renderer for one dated numeric series; 3 patterns plus no-clear-pattern fallback.

## Executed checks

- 29 local pytest cases: pattern routing (trend/shift/anomaly/unclear), hash/evidence tampering, malformed/missing/out-of-order dates, non-finite values, invalid claims/timelines, deterministic frame(t), ordered audio events and representative render frames.
- Rendered 23.5-second MP4: `output/film.mp4`, 960x540, 24 fps, H.264 + AAC, 564 frames. Poster inspected.
- Rendered 23.5-second Trend/Anomaly comparison MP4s at 640x360, 12 fps, using exactly the same renderer. Posters inspected.
- Ran ffprobe on default film to check both video and audio streams.
- No external benchmarks, human preference tests, or reproduction of Lemo-Opuscar quality were performed.

## Known gaps

- Data source metadata is user-provided and is not independently verified.
- Qualitative story text is not semantically fact-checked; numeric claims cannot appear in title/subline (digits banned).
- Pattern detectors are heuristics without significance guarantees; only locally isolated spikes and clear persistent steps are accepted.
- Story Spec currently supports one line chart and a fixed visual style. Voice-over, editor UI, multiseries, seasonal narratives and real-data cross-domain evaluation are future work.
- Runtime reuses narration grammar but **not** the upstream library's implementation. It is a clean independent prototype.
