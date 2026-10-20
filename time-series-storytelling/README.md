# Time-Series Storytelling · MVP v0.1

A **reproducible Skill + Runtime** that turns a dated numeric series into an evidence-bound, code-rendered short MP4. Inspired by the conceptual separation in Lemo-Opuscar (style grammar, narrative plan, deterministic renderer); **independent implementation**, without copying its code, films or visual assets.

**Status:** Working prototype, not a general-purpose AI director. Detection is deliberately conservative. No video-generation model, API key or internet access is needed.

## Quick start

```bash
# Requirements: Python >= 3.10, NumPy, Pillow, ffmpeg on PATH
pip install -e .
python -m ts_story run examples/step_up.csv \
  --metric 'Active accounts' --unit accounts \
  --source 'Synthetic example; generated for this demo' \
  --outdir output

# Select an archetype for which evidence is actually present
python -m ts_story plan examples/spike.csv --metric 'Request latency' --unit ms \
  --source 'Synthetic fixture' --pattern anomaly --out output/spike.json
python -m ts_story verify output/spike.json --csv examples/spike.csv
python -m ts_story render output/spike.json --csv examples/spike.csv \
  --out output/spike.mp4 --poster output/spike.png
pytest -q
```

Outputs: `film.mp4` (video plus synthesized sound), `film.png` (poster), and `story.json` (inspectable evidence, narrative beats and caveats). Video defaults to 960×540 at 24 fps, ~23.5 seconds. Override `--size 1280x720 --fps 30` for other outputs.

## Pipeline

```text
CSV (date,value) + meaning & source
        ↓  strict read; no interpolation
Heuristic insight discovery
(trend / persistent step / isolated anomaly / no clear pattern)
        ↓
Evidence-bound six-beat Story Spec (JSON)
        ↓ validation: hash, facts, refs, timing, basic copy limits
Deterministic frame(t) + observation-triggered synthesized audio
        ↓  raw RGB pipe to FFmpeg
MP4 + poster, editable Story Spec + source snapshot
```

No model is required for the MVP because planning is currently template/rule-based. An LLM can revise *qualitative* headlines and beat choices against the provided evidence, subject to the same verification contract. This is where semantic insight and audience-specific narrative reasoning would be added.

## What is truly reusable?

The 6-beat structure, evidence refs, chart operations, camera pacing, sonification, and frame-independent rendering. Per-dataset creative decisions should be represented as Story Spec rather than generated code. The renderer is a single non-parameterized midnight visual style in v0.1; reusable `STYLE.md` presets and richer plot grammars are a next increment.

The built-in case studies contain **synthetic values only**; no domain conclusions should be drawn from them.

## Architecture

- `SKILL.md`: orchestration and truthfulness gate.
- `ts_story/data.py`: strict dated-series loading and content hash.
- `ts_story/analyze.py`: 3 pattern heuristics with conservative threshold gates.
- `ts_story/plan.py`: narrative archetypes and evidence-indexed events.
- `ts_story/validate.py`: hard-stop source/value/timing/copy checks.
- `ts_story/render.py`: pure time-based frame composition and MP4 encoding through FFmpeg.
- `ts_story/audio.py`: original synthesized sound for every newly revealed observation.
- `references/story-spec.md`: structured contract for future LLM adaptation.
- `tests/`: regression gates.

## What this MVP deliberately does not claim

- A pattern score is **not** a likelihood, a rigorous change-point test, or a causal explanation.
- Artistically compressed playback does **not** mean the observed process accelerated.
- No seasonality decomposition, multiple series, interpolation, forecasting, fact-checking of external claims, TTS, narration, captions or automated aesthetics evaluation yet.
- Numeric factual statements are rendered only from CSV observations; even verified numbers can be misleading if context, units or definitions are omitted. Qualitative prose is not machine-fact-checked.
- Absolute reproducibility depends on pinned runtime, font and FFmpeg versions. Here, `frame(t)` itself is stateless and deterministic in a fixed environment.

## Acceptance for next milestone

1. At least 15 real or public datasets across domains; expected-pattern, counterexample and no-pattern cases.
2. External acceptance checks for narrative truthfulness and reader comprehension.
3. Compare end-to-end time/token cost and perceived quality to one-off code generation, not just renderer speed.
4. Move storyboard choices into more expressive but still verifiable Story Spec, then parameterize style assets.

Upstream inspiration: https://github.com/lemomo-ai/lemo-opuscar
