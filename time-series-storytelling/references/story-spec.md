# Story Spec v1 — contract and grammar

`schema: ts-story/v1`. A spec is JSON, not executable code.

- `metric`, `unit`, `source`: required provenance and measure semantics. `source` is a user-provided citation string, not verified by the runtime.
- `data_sha256`, `observation_count`, `date_range`: binding to the exact CSV snapshot. Any data change requires replanning.
- `pattern`: `trend | regime_shift | anomaly | no_clear_pattern`; the detector is heuristic, not causal nor a change-point significance test.
- `analysis` and `confidence_heuristic`: diagnostic outputs; the number is not a calibrated probability.
- `evidence`: `{ref: {kind: observation, index, date, value}}`, with exact source row equality.
- `beats`: ordered `{id, kind, start, duration, headline, subline, evidence_refs}`. The `kind` vocabulary is intro, context, build, turn, reveal, outro.
- `duration`: last beat endpoint in seconds, contiguous timeline. Each beat is at least 0.5 s.
- Editorial headline and subline must contain **no digits**; numbers only appear when rendered from verified evidence references. This guard is conservative and can reject harmless phrases such as "24/7". It cannot detect unsupported qualitative assertions.

### Default 6-beat grammar

| Beat | Intent | Common visual act |
|---|---|---|
| intro | establish observation | single point |
| context | establish scale/reference | start drawing timeline |
| build | expose pattern | chart tracks newly revealed observations |
| turn | inspect strongest evidenced event | highlight linked observation |
| reveal | show whole and disclose comparison | full-domain plot and (if level shift) period means |
| outro | end without forecast | complete record and visible limitations |

### Scope limitations

Time is encoded by actual date ordinates along x, not by index. Reveal cadence is compressed deliberately for cinematic effect and must not be described as measured velocity. All trends and anomalies require external contextual validation before claims about causation. `source` attribution is not URL fetched, licensed or vetted. Style is currently fixed (`midnight-ink`).
