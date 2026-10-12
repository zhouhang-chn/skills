#!/usr/bin/env python3
"""Package a dashboard spec as a portable offline single-file HTML document."""
from __future__ import annotations
import argparse
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ALLOWED_TYPES = {"kpi", "line", "bar", "table", "text", "custom"}
ALLOWED_AGG = {"first", "sum", "avg", "min", "max", "count"}

class SpecError(ValueError):
    pass


def _dataset_normalize(name: str, val: dict, base: Path) -> dict:
    if not isinstance(val, dict):
        raise SpecError(f"Dataset {name!r} must be an object")
    source_file = val.get("file")
    if source_file:
        path = (base / source_file).resolve()
        if not path.is_file():
            raise SpecError(f"Dataset {name!r}: file not found: {path}")
        if path.suffix.lower() == '.json':
            contents = json.loads(path.read_text(encoding='utf-8'))
            if isinstance(contents, list):
                val = {**val, "rows": contents}
            elif isinstance(contents, dict) and "rows" in contents:
                val = {**contents, **{k:v for k,v in val.items() if k != "file"}}
            else:
                raise SpecError(f"Dataset {name!r}: JSON must contain array of rows")
        elif path.suffix.lower() == '.csv':
            import csv
            with path.open(encoding='utf-8-sig', newline='') as f:
                val = {**val, "rows": list(csv.DictReader(f))}
        else:
            raise SpecError(f"Dataset {name!r}: only CSV/JSON supported")
    rows = val.get("rows")
    if not isinstance(rows, list):
        raise SpecError(f"Dataset {name!r}: rows array required")
    cols = val.get("columns")
    if cols is None:
        if rows and isinstance(rows[0], dict):
            cols = list(rows[0].keys())
        elif rows:
            raise SpecError(f"Dataset {name!r}: columns required for array rows")
        else:
            cols = []
    if not isinstance(cols, list) or len(set(cols)) != len(cols) or any(not isinstance(x,str) for x in cols):
        raise SpecError(f"Dataset {name!r}: columns must be unique strings")
    for i, r in enumerate(rows):
        if isinstance(r, list):
            if len(r) != len(cols):
                raise SpecError(f"Dataset {name!r}: row {i} has wrong column count")
        elif isinstance(r, dict):
            if set(r) - set(cols):
                raise SpecError(f"Dataset {name!r}: row {i} contains unexpected columns")
        else:
            raise SpecError(f"Dataset {name!r}: row {i} is not array/object")
    return {**{k:v for k,v in val.items() if k not in ('file','rows','columns')}, "columns":cols, "rows":rows}


def normalize(spec: dict, base: Path) -> dict:
    if not isinstance(spec, dict) or not isinstance(spec.get('title'), str) or not spec['title'].strip():
        raise SpecError("Non-empty 'title' is required")
    datasets = spec.get('datasets')
    if not isinstance(datasets, dict) or not datasets:
        raise SpecError("At least one named dataset is required")
    dataset_out = {key:_dataset_normalize(key,val,base) for key,val in datasets.items()}
    params = spec.get('params',[])
    if not isinstance(params,list): raise SpecError('params must be an array')
    for p in params:
        if not isinstance(p,dict) or not p.get('id') or not isinstance(p.get('options'),list) or not p['options']:
            raise SpecError('Each param needs id and nonempty options')
        if p.get('default',p['options'][0]) not in p['options']:
            raise SpecError(f"Param {p['id']}: default not in options")
    calcs=spec.get('calcs',[])
    if not isinstance(calcs,list): raise SpecError('calcs must be an array')
    ids=set(dataset_out)
    for c in calcs:
        if not isinstance(c,dict) or not c.get('id') or c['id'] in ids:
            raise SpecError('Every calc id must be unique and distinct from datasets')
        if c.get('op') not in ('filter','group_by'):
            raise SpecError(f"Calc {c['id']}: unsupported op {c.get('op')}")
        ids.add(c['id'])
    for c in calcs:
        if c.get('input') not in ids:raise SpecError(f"Calc {c['id']}: input does not exist")
        if c['op']=='filter':
            for cond in c.get('where',[]):
                if 'param' in cond and cond['param'] not in {p['id'] for p in params}:
                    raise SpecError(f"Calc {c['id']}: unknown param {cond['param']}")
    widgets=spec.get('widgets')
    if not isinstance(widgets,list) or not widgets:
        raise SpecError('At least one widget is required')
    widget_ids=set()
    for w in widgets:
        if not isinstance(w,dict) or w.get('type') not in ALLOWED_TYPES or not w.get('id'):
            raise SpecError('Every widget needs id and a supported type')
        if w['id'] in widget_ids: raise SpecError(f"Duplicate widget id {w['id']}")
        widget_ids.add(w['id'])
        if w['type'] not in ('text','custom') and w.get('dataset') not in ids:
            raise SpecError(f"Widget {w['id']}: dataset not found")
        if w.get('aggregate','first') not in ALLOWED_AGG:
            raise SpecError(f"Widget {w['id']}: unknown aggregation")
        if w.get('span',12) not in (3,4,6,8,9,12):
            raise SpecError(f"Widget {w['id']}: span must be 3,4,6,8,9,12")
    return {**spec,'datasets':dataset_out}


def json_for_script(obj):
    # Prevent closing the script element, even with malicious data cell contents.
    return json.dumps(obj,ensure_ascii=False,separators=(',',':'),allow_nan=False).replace('&','\\u0026').replace('<','\\u003c').replace('>','\\u003e').replace('\u2028','\\u2028').replace('\u2029','\\u2029')


def build(spec_path: Path, dest: Path) -> None:
    spec = normalize(json.loads(spec_path.read_text(encoding='utf-8')),spec_path.parent)
    css=(ROOT/'assets/styles.css').read_text(encoding='utf-8')
    js=(ROOT/'assets/runtime.js').read_text(encoding='utf-8')
    custom_js=''
    if spec.get('custom_js'):
        custom_js=(spec_path.parent/spec['custom_js']).read_text(encoding='utf-8')
        if re.search(r'</script\s*>',custom_js,re.I):
            raise SpecError('Custom JS cannot contain </script> closing tag')
    if spec.get('custom_css'):
        css+='\n'+(spec_path.parent/spec['custom_css']).read_text(encoding='utf-8')
    title = html.escape(spec['title'])
    page=f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="light"><title>{title}</title>
<style>{css}</style></head><body>
<div id="dashboard-root"></div>
<script type="application/json" id="dashboard-data">{json_for_script(spec)}</script>
<script>{js}</script>
<script>{custom_js}</script>
</body></html>'''
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(page,encoding='utf-8')
    print(f"Built {dest} ({dest.stat().st_size:,} bytes; {len(spec['datasets'])} datasets; {len(spec['widgets'])} widgets)")

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('spec',type=Path,help='JSON dashboard spec')
    p.add_argument('-o','--output',type=Path,required=True,help='Output standalone .html')
    args=p.parse_args()
    try:build(args.spec.resolve(),args.output.resolve())
    except (OSError,ValueError,KeyError,SpecError) as err:
        print(f'Build failed: {err}',file=sys.stderr);sys.exit(1)
