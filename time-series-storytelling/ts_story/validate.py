"""Validate generated or edited specs against their immutable source observations."""
from __future__ import annotations
import math
import re
from .data import Series
from .plan import PATTERNS


def verify(spec: dict, series: Series) -> list[str]:
    failures = []
    def require(pred, message):
        if not pred: failures.append(message)
    require(spec.get('schema') == 'ts-story/v1', 'Unsupported story schema')
    require(spec.get('data_sha256') == series.sha256, 'Data content hash mismatch; re-plan after data changes')
    require(spec.get('observation_count') == len(series.values), 'Observation count mismatch')
    require(spec.get('date_range') == [series.dates[0], series.dates[-1]], 'Date range mismatch')
    require(spec.get('pattern') in PATTERNS, 'Unknown story pattern')
    require(bool(spec.get('source')), 'Missing source attribution')
    require(bool(spec.get('metric')), 'Missing metric')
    evidence = spec.get('evidence', {})
    require(isinstance(evidence, dict), 'Evidence must be an object')
    if isinstance(evidence, dict):
        for ref, item in evidence.items():
            try:
                i = item['index']
                require(type(i) is int and 0 <= i < len(series.values), f'{ref}: index out of range')
                if type(i) is int and 0 <= i < len(series.values):
                    require(item['date'] == series.dates[i], f'{ref}: date not from source')
                    require(math.isclose(float(item['value']),float(series.values[i]), rel_tol=1e-10, abs_tol=1e-10),f'{ref}: value not from source')
                require(item['kind'] == 'observation', f'{ref}: unexpected evidence kind')
            except (ValueError, TypeError, KeyError) as exc:
                failures.append(f'{ref}: malformed evidence {exc}')
    beats = spec.get('beats', [])
    require(isinstance(beats,list) and len(beats) >= 3,'Need at least 3 beats')
    if isinstance(beats,list):
        end=0.
        for j, b in enumerate(beats):
            if not isinstance(b,dict):
                failures.append(f'Beat {j}: not an object'); continue
            try:
                start=float(b['start']);duration=float(b['duration'])
                require(math.isfinite(start) and math.isfinite(duration) and duration >= .5,f'Beat {j}: invalid timing')
                require(abs(start-end) < .002, f'Beat {j}: non-contiguous timing')
                end=start+duration
                require(b['kind'] in {'intro','context','build','turn','reveal','outro'}, f'Beat {j}: unknown kind')
                for f in ['headline','subline']:
                    s=b.get(f)
                    require(isinstance(s,str) and len(s)<100 and not re.search(r'\d',s) and '\n' not in s,
                            f'Beat {j}: {f} must be short and number-free; numeric claims must use evidence refs')
                for ref in b.get('evidence_refs',[]):
                    require(ref in evidence,f'Beat {j}: missing evidence ref {ref}')
            except (KeyError, ValueError, TypeError) as exc:
                failures.append(f'Beat {j}: invalid {exc}')
        require(abs(float(spec.get('duration',-1))-end) < .002,'Story duration mismatch')
    return failures


def verify_or_raise(spec:dict,series:Series):
    failures=verify(spec,series)
    if failures: raise ValueError('Story verification failed:\n- '+'\n- '.join(failures))
