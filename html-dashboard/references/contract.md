# html-dashboard contract v0.1

## Minimal document

```json
{
  "title": "Orders monitor",
  "subtitle": "Paid orders by month",
  "metadata": { "as_of": "Data through September 2026" },
  "datasets": {
    "monthly": {
      "columns": ["month", "orders", "revenue"],
      "rows": [["2026-08", 100, 12000], ["2026-09", 120, 14000]],
      "source": {
        "label": "orders, aggregated from warehouse",
        "query": "SELECT date_trunc('month', order_date) AS month, count(*) AS orders, sum(net_revenue) AS revenue FROM orders WHERE status = 'paid' GROUP BY 1",
        "as_of": "Extracted 2026-10-01 UTC",
        "notes": "Sample query for illustrative data only"
      }
    }
  },
  "params": [],
  "calcs": [],
  "widgets": [
    {"id":"orders", "type":"kpi", "title":"Total orders", "span":3, "dataset":"monthly", "field":"orders", "aggregate":"sum", "format":"integer"},
    {"id":"revenue", "type":"line", "title":"Revenue trend", "span":9, "dataset":"monthly", "x":"month", "y":"revenue", "format":"currency"}
  ]
}
```

This JSON is a contract example **with illustrative data and SQL**, not a real executed query. Do not reuse the SQL or source statement for unrelated data.

## Root fields

| Field | Meaning |
| --- | --- |
| `title` | Required dashboard title. |
| `kicker`, `subtitle` | Optional header label and explanatory subheading. |
| `metadata.as_of` | Optional visible honest data coverage or extract timestamp. |
| `datasets` | Required map of source dataset ID to rows, columns and source metadata. |
| `params` | Optional select-only filters, each with `id`, `label`, `options`, `default`. |
| `calcs` | Optional named derived datasets, each with unique `id`, `op` and `input`. |
| `widgets` | Required ordered array of visualizations. |
| `custom_js`, `custom_css` | Optional local relative file paths to trusted JS/CSS inlined by the bundler. |

## Data

Data can be `rows` of objects or `columns` plus array-of-array rows. A dataset can instead use `"file": "data.csv"` or `"file": "data.json"` relative to the spec. CSV is parsed during build, not by the browser. `source.label`/`query`/`as_of`/`notes` are optional metadata, but `source.label` is recommended. Missing upstream SQL is explicitly reported as absent.

The builder rejects malformed dimensions, duplicate IDs and missing references. Numeric values in the source may be strings; charts will coerce them. Ensure all date labels sort lexicographically in chronological order (e.g. `YYYY-MM`). Null or non-numeric measure rows should be fixed upstream; don't treat missing metrics as genuine zero.

## Parameters

```json
{"params":[{"id":"month","label":"Month","options":["2026-08","2026-09"],"default":"2026-09"}]}
```

Only string-valued select widgets are exposed as filters in v0.1. If the input options are numeric, convert them to strings in the spec to prevent mismatch with HTML select values. Params are public local UI state, not access-control tokens.

## Calculations

Filter rows by one or more conditions:

```json
{"id":"selected", "op":"filter", "input":"monthly",
 "description":"Month equals the selected month",
 "where":[{"field":"month","param":"month"}]}
```

A condition accepts `{field,param}` or `{field,value}`, optional `operator` (`eq` default, `in`, `gte`, `lte`) and optional `skip_value` (e.g. `"All"`). Multiple conditions use AND. `in` expects a list-valued parameter/value.

Group by fields with sum/avg/count:

```json
{"id":"by_region", "op":"group_by", "input":"orders",
 "group_by":["region"],
 "measures":{"total":{"field":"amount","op":"sum"},"orders":{"field":"amount","op":"count"}}}
```

`group_by` and `filter` can chain to create a calculation graph, but cycles are invalid at runtime. Client transforms are not a replacement for warehouse SQL when large/raw datasets are involved.

## Widgets

All widgets have `id`, `type`, `title`, optional `subtitle`, and `span` (3,4,6,8,9,12). All except `text` and `custom` need `dataset`.

| Type | Required / useful fields |
| --- | --- |
| `kpi` | `field`, `aggregate` (`first`, `sum`, `avg`, `min`, `max`, `count`), `format`, `note` |
| `line` | `x`, `y`, `format`, optional `highlight_param` |
| `bar` | `x`, `y`, `format`, `limit` (default 8) |
| `table` | `columns`: array of `{field,title,format}`, `sort_by`, `limit` (default 20) |
| `text` | `text` plain text paragraph |
| `custom` | Custom JS finds `[data-widget-id="your-id"] .widget-body` and inserts DOM/SVG |

Built-in `format`: `compact` (e.g. 1.3M), `currency` (e.g. $1.3M), `money` ($23.50), `percent` (0.25 → 25.0%), `integer`, `decimal`. Percent assumes a 0–1 fraction. Set meaningful units in labels. For KPI month-over-month change:

```json
{"compare": {"dataset":"monthly", "field":"orders", "previous_by":"month", "selector_param":"month"}}
```

Comparison obtains the previous chronological row by lexicographically sorted `previous_by`. Only use if the `month` key is unique and chronologically sortable. KPI shows relative percent change, not absolute or percentage-point change.

## `window.dash` API

- `dash.data(id) -> { status: 'ok', data: object[], columns }` or `{status:'missing'|'error', reason}`. Source datasets and calcs have the same interface.
- `dash.params() -> {...}` returns current parameter snapshot.
- `dash.setParams({month:'2026-09'})` validates declared parameter options, recomputes calcs and rerenders widgets.
- `dash.resetParams()` restores defaults.
- `dash.calc(id,{inputs:['orders'],fn:(rows)=>...})` adds a trusted inline JS transform. This is only used in `custom_js`, not eval of JSON text. It may depend on `dash.params()`.
- `dash.onData(callback)` subscribes to recalculation and immediately invokes callback; returns unsubscribe closure.
- `dash.evidence(id)` returns a list of source and calc definitions for an ID.
- `dash.refresh()` and `dash.loader()` return `{status:'unavailable'}` — deliberately no fake live refresh.

Custom visualization example in a local `custom.js`:

```js
const target = document.querySelector('[data-widget-id="custom-example"] .widget-body');
window.dash.onData(() => {
  target.replaceChildren();
  const rows = dash.data('selected').data;
  const p = document.createElement('p');
  p.textContent = `Selected rows: ${rows.length}`;
  target.append(p);
});
```

Use `createElement`, `textContent`, SVG DOM APIs, avoid `innerHTML` with input data. For a multi-chart custom visualization, work with bounded aggregates and update on `onData`.

## Evidence semantics

Evidence panel includes: widget definition, current params, source/calc lineage, calculation definitions, original source query **only if supplied**, source notes/date and up to five materialized rows. This is inspection of **snapshot evidence**, not connection-level lineage, permissioned query results, or proof that a SQL statement was executed.

## Non-goals v0.1

No live connectors, warehouse refresh, SQL execution, artifact store, multi-file runtime dependencies, editable dashboard design studio, cross-filter brushing, row-level security, PDF export, or advanced chart grammars. Offline HTML is a transportable *view plus snapshot*; it is not a BI platform or online Claude Artifact replacement.
