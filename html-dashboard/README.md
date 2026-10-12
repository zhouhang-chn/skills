# html-dashboard

Standalone Agent Skill for generating interactive, evidence-aware, **single-file offline HTML dashboards**. Inspired by observable Claude Dashboard exports, independently implemented without Claude internal code. No npm, CDNs, database credentials, servers or network dependencies.

## Quick start

```bash
python3 scripts/build.py examples/nyc_taxi.json -o dashboard.html
python3 scripts/check.py dashboard.html
# Open dashboard.html in any modern browser; no server needed.
```

The source JSON holds `datasets`, `params`, `calcs`, and `widgets`. The generated HTML embeds the data, deterministic JavaScript runtime, responsive styles and SVG charts. Every widget exposes Evidence for traceability.

See `SKILL.md` for agent execution instructions and `references/contract.md` for authoring syntax and limitations.

## API overview

`dash.data(id)` · `dash.calc(id, spec)` · `dash.params()` · `dash.setParams()` · `dash.onData()` · `dash.evidence()`.

**Offline only:** No SQL runner, live refresh or authenticated artifact store. Source query/refresh metadata is retained only when available in supplied evidence.

## Directory

- `SKILL.md` — portable Agent Skills entry point
- `scripts/build.py` — zero-dependency bundler
- `scripts/check.py` — standalone HTML validator (optional Playwright browser test)
- `assets/runtime.js`, `assets/styles.css` — independent reusable runtime
- `references/contract.md` — precise spec and extension API
- `examples/nyc_taxi.json` — sample based on a supplied NYC Taxi export
- `tests/test_build.py` — contract/build/security tests

MIT licensed. This is not affiliated with or endorsed by Anthropic.
