# Roadmap

The first goal is to learn whether a constrained, inspectable **Story Spec** can improve time-to-video without reducing correctness or story quality.

## v0.2 — Director and Story Spec

- Introduce an optional LLM Narrative Planner over evidence-bound findings, preserving a model-free fallback.
- Extend Story Spec with explicit camera operations, temporal mapping, sonic actions and visual transitions.
- Add semantic validity checks for claims about baselines, ratios, trend direction and causality.
- Keep rendering independent from authoring: the model writes JSON, not execution code.

## v0.3 — Styles, formats and reproducibility

- Add a style adapter (e.g. pencil chart inspired by public design grammar) without copying upstream code/assets.
- Add multi-series comparison and seasonal stories once their evidence model is specified.
- Pin or record rendering dependency versions and font fallbacks in the output manifest.

## Evaluation track

- At least 15 source-licensed/public datasets: positive, negative and ambiguous cases.
- Verify factual fidelity, chart integrity, audience comprehension and subjective story quality.
- Benchmark generation effort, tokens and edit cycles against one-off scripted video creation.
- Record both regression successes and newly introduced failures; treat unsupported narrative claims as hard failures.

Not currently claimed: statistically validated change-point detection, automated causation, guaranteed aesthetic quality, or general-purpose video direction.
