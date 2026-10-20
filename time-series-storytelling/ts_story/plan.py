"""Deterministic evidence-bound story plan, editable as JSON."""
from __future__ import annotations
from pathlib import Path
import json
import re
from .data import Series
from .analyze import choose


BEAT_DURS = [2.8, 4.2, 4.3, 4.8, 4.8, 2.6]
PATTERNS = {
 "trend": [("intro", "EVERY POINT HAS A DATE", "Start with one observation"),
           ("context", "ESTABLISH THE BASELINE", "Watch the earliest observations"),
           ("build", "THE DIRECTION EMERGES", "Follow the recorded values"),
           ("turn", "THE LONG VIEW", "Compare the starting and ending observations"),
           ("reveal", "ONE CONTINUOUS RECORD", "Show the complete series"),
           ("outro", "WHAT COMES NEXT?", "Future values are unknown")],
 "regime_shift": [("intro", "THE STORY IN THE SERIES", "Each mark represents a real observation"),
           ("context", "BEFORE THE SHIFT", "Establish the earlier level"),
           ("build", "A STABLE START", "Follow the early observations"),
           ("turn", "A DIFFERENT LEVEL", "The later values step away from the earlier ones"),
           ("reveal", "BEFORE / AFTER", "Compare the two observed periods"),
           ("outro", "THE NEXT POINT IS UNKNOWN", "A pattern does not guarantee the future")],
 "anomaly": [("intro", "THE PATTERN STARTS", "A single series, in order"),
           ("context", "THE USUAL RANGE", "Establish the local baseline"),
           ("build", "MOST POINTS STAY CLOSE", "Watch the observations accumulate"),
           ("turn", "ONE POINT BREAKS AWAY", "Inspect the unusual observation"),
           ("reveal", "THE EXCEPTION IN CONTEXT", "Show what happened before and after"),
           ("outro", "AN ANOMALY IS NOT A CAUSE", "An investigation starts with the source")],
 "no_clear_pattern": [("intro", "THE AVAILABLE RECORD", "Every point is an observation"),
           ("context", "READ THE FIRST POINTS", "Build the chart without a claim"),
           ("build", "CONTINUE THE RECORD", "No turning point is assumed"),
           ("turn", "NO CLEAR PATTERN FOUND", "Avoid making a dramatic claim"),
           ("reveal", "HERE IS THE FULL SERIES", "Examine the whole range"),
           ("outro", "THE DATA IS THE EVIDENCE", "Interpretation needs more context")]
}


def _clean_copy(s: str) -> str:
    if re.search(r"\d", s):
        raise ValueError("Editorial headline/subline cannot contain numeric claims; use evidence references")
    if len(s) > 90 or "\n" in s:
        raise ValueError("Editorial copy must fit a single title/card")
    return s


def build(s: Series, *, metric: str, unit: str, source: str, pattern: str = "auto") -> dict:
    if not metric.strip() or not source.strip():
        raise ValueError("metric and source are mandatory; do not invent provenance")
    f = choose(s, pattern)
    n = len(s.values)
    i = f.anchor if f.anchor is not None else n - 1
    point_ids = {"first": 0, "last": n-1, "anchor": i}
    if f.pattern == "regime_shift":
        point_ids["before"] = i - 1
    ev = {k: {"id":k,"kind":"observation","index":idx,"date":s.dates[idx],"value":float(s.values[idx])} for k,idx in point_ids.items()}
    beats = []
    start = 0.0
    for j, ((kind, headline, subline), duration) in enumerate(zip(PATTERNS[f.pattern], BEAT_DURS)):
        anchor = "anchor" if j == 3 else "first" if j in (0,1) else "last" if j >= 4 else None
        beats.append({"id":f"b{j+1}", "kind":kind,"start":round(start,3),"duration":duration,
                      "headline":_clean_copy(headline),"subline":_clean_copy(subline),
                      "evidence_refs":[anchor] if anchor else []})
        start += duration
    return {"schema":"ts-story/v1", "metric":metric.strip(), "unit":unit.strip(), "source":source.strip(),
            "data_sha256":s.sha256,"observation_count":n,"date_range":[s.dates[0],s.dates[-1]],
            "pattern":f.pattern,"confidence_heuristic":f.score,"analysis":f.evidence,
            "caveats":list(dict.fromkeys([*s.warnings,*f.caveats])),
            "evidence":ev,"beats":beats,"duration":round(start,3),"style":"midnight-ink"}


def save(spec:dict, path:str | Path):
    Path(path).parent.mkdir(parents=True,exist_ok=True)
    Path(path).write_text(json.dumps(spec,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
