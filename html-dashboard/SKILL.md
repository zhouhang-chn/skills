---
name: html-dashboard
description: Generate polished, interactive, evidence-aware, self-contained offline HTML dashboards from CSV, JSON, SQL query results, or structured analysis. Use when asked to build a Claude-Dashboard-like data artifact, KPI dashboard, exploratory report, HTML data visualization, or shareable one-file dashboard. Includes a deterministic JavaScript runtime, chart templates, provenance drawer, bundler, and browser validation.
compatibility: Requires Python 3.10+ (standard library only) for packaging. Generated dashboards work in modern desktop/mobile browsers without a server, internet connection, or external libraries. Optional Chromium/Playwright for visual QA.
metadata:
  version: "0.1.0"
---

# HTML Dashboard

Create a **single portable `.html` file** with interactive charts, filters, derived calculations and an inspectable Evidence drawer. This is an independent implementation inspired by the observable behavior of Claude Dashboard **exports**, not the Claude private runtime or online Artifact Store.

## Files to use

- `scripts/build.py`: deterministic, dependency-free bundler. Always invoke; do not copy a demo HTML and hand-edit its embedded JSON.
- `assets/runtime.js`: reusable, offline browser runtime exposing `window.dash`.
- `assets/styles.css`: responsive view and chart system.
- `references/contract.md`: JSON schema-by-example, APIs and constraints. **Read this before authoring a complex spec.**
- `examples/nyc_taxi.json`: worked example using a prior supplied export; use it to learn structure, not as another user's data.
- `scripts/check.py`: structural and optional browser smoke tests.

## Workflow (required)

1. **Understand the decision and data grain.** Identify business question, KPIs, dimensions, comparisons, time grain, target audience, caveats. Look at actual columns and rows; do not assume units, data types, source query or causal explanations.
2. **Prepare compact datasets.** Execute upstream SQL / read uploaded data using tools authorized in the current environment. The Skill itself **does not connect** to databases. Prefer aggregated extracts over raw event rows. Filter and summarize large data outside the browser. Preserve source labels, true SQL text if available, extraction time and caveats. If SQL is missing, say so; never create a fabricated “original query.”
3. **Plan views.** Choose a small set of KPI, trend, category comparison and detail views that answer the question. Use `params` for filter controls. Use named `calcs` for deterministic filters/groupings. Choose clear units, sorting, empty states and sample sizes.
4. **Write a dashboard JSON spec.** Conform to `references/contract.md`. Store original datasets independently from the widgets. Source datasets should be stable; derived datasets refer to source IDs. Record evidence for each dataset under `source`.
5. **Build the HTML.** From this Skill directory, run:

   ```bash
   python scripts/build.py /path/to/report.json -o /path/to/dashboard.html
   ```

   The output embeds HTML, CSS, JS, datasets and evidence. No CDN, server, local JS/JSON files, runtime fetch or login is needed to open the dashboard.
6. **Validate.** Run `python scripts/check.py /path/to/dashboard.html` and use a browser if possible. Change filters; inspect KPI recalculation and charts; open Evidence; check formatting, no horizontal overflow, console errors and that offline access works. If test fails, repair and rerun. Do not assert that any live-query capability exists in the export.
7. **Deliver the `.html`** and a one-sentence statement of data freshness, provenance and limitations. When useful also deliver the source JSON and Skill directory as editable artifacts.

## Authoring choices

- **Standard layouts:** author `widgets` with `kpi`, `line`, `bar`, `table`, `text` and `custom`, along with `span` for grid placement. Standard renderer uses native SVG, no D3 required.
- **Controlled transforms:** add `calcs` using `filter` or `group_by`. The runtime only executes known operations; it does **not** eval user strings.
- **Free-form visualizations:** when the standard widgets do not express the design, include a local file in `custom_js`; define `type: "custom"` widgets and render them with browser JavaScript. Use `dash.data()`, `dash.params()`, `dash.calc()` and `dash.onData()` in your custom script. Optional `custom_css` is also bundled. **Treat authored JS/CSS as trusted code and inspect before distribution.**
- **Evidence is first class:** every data-backed widget has an Evidence button showing upstream dataset/source, transformations, parameter values and result samples. Only show source SQL when it is genuinely known.
- **Snapshot means snapshot:** no invented refresh date, live data or host capabilities. `dash.refresh()` returns `unavailable` in this edition.

## Quality bar

- No invented facts, fake KPI values, silent denominators, phantom SQL or fabricated provenance.
- Accessible controls, responsive layout, interpretable axes, consistent number formats and honest missing/zero handling.
- No outbound network requests, trackers, remote fonts, CDN libraries, fake API calls, untrusted `innerHTML`, or dynamic `eval`.
- Bundle should be reusable with different datasets **without modifying the runtime**. Prefer spec changes; reserve custom JS for genuinely novel chart types.
- Keep calculations transparent, render determinate and evidence tied to displayed filtered rows. Clearly distinguish upstream SQL from client-side calculated transforms.

## Example

```bash
python scripts/build.py examples/nyc_taxi.json -o /tmp/nyc-taxi.html
python scripts/check.py /tmp/nyc-taxi.html
```

See `references/contract.md` for field definitions, parameter semantics, custom JS examples, and unsupported operations.
