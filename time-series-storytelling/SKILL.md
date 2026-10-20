---
name: time-series-storytelling
description: Turn a timestamped numeric series into a source-grounded narrative plan and a reproducible code-rendered short video. Use for visual time-series explainers, trend/regime-shift/anomaly stories, or repeatable data-to-video workflows; not for predicting the future or inventing causes.
---

# Time-Series Storytelling

**Goal:** Transform time-series observations into an evidence-grounded story, preserving the numbers while varying the narrative.

1. **Ingest and establish meaning.** Require a `date,value` CSV, metric name, unit and data source. Ask for higher-is-better/operational meaning only when it affects the interpretation. Don't silently impute, deduplicate or change units.
2. **Discover before directing.** Run `python -m ts_story plan ...` to inspect trend, persistent level shift and isolated anomaly. When none clears the gate, report that finding instead of fabricating drama. Treat detected patterns as descriptive, not causal or statistically proven.
3. **Choose a story structure.** Use the proposed Story Spec as an editable first draft. Choose the audience's central question, temporal scope and one main insight. Use the documented beat grammar (`references/story-spec.md`); add only claims linked to source data or externally verified evidence. Do not recycle a demo's plot or character by default.
4. **Verify before rendering.** Run `python -m ts_story verify story.json --csv data.csv`. Any modified observation, missing source, changed file hash, unreferenced numeric headline, or invalid timing is a hard stop. The narrative may change how information is revealed, never what the data says. Avoid pacing or rescaling that makes acceleration or causation appear data-derived when it is not.
5. **Produce and evaluate.** Run `python -m ts_story render story.json --csv data.csv --out film.mp4 --poster poster.png`. Watch the movie with audio. Review legibility, temporal honesty, source/date accuracy, audience understanding and whether the selected insight is meaningful. Revise the Story Spec and rerender; change runtime only for a capability gap.
6. **Deliver.** Provide the film, poster, `story.json`, source CSV/source link and caveats. Clearly label synthetic datasets and provisional observations. Say what was actually rendered and checked.

**Runtime:** Python 3.10+, NumPy, Pillow, FFmpeg. Commands, constraints and tests are in `README.md`. Current MVP has 3 archetypes, plus a no-clear-pattern fallback; it does not include voice, LLM generation, causal inference, multi-series charts or narrative quality automation.
