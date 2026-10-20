"""Strict CSV ingestion and provenance. No silent sorting/dedup/imputation."""
from __future__ import annotations
import csv
import hashlib
import math
from datetime import date
from pathlib import Path
import re
from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class Series:
    dates: tuple[str, ...]
    xs: np.ndarray
    values: np.ndarray
    sha256: str
    warnings: tuple[str, ...]


def _date(s: str) -> date:
    if re.fullmatch(r"\d{4}", s):
        return date(int(s), 1, 1)
    if re.fullmatch(r"\d{4}-\d{2}", s):
        return date.fromisoformat(s + "-01")
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", s):
        return date.fromisoformat(s)
    raise ValueError(f"Unsupported date {s!r}; use YYYY, YYYY-MM or YYYY-MM-DD")


def load_csv(path: str | Path) -> Series:
    raw = Path(path).read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    dates: list[str] = []
    xs: list[int] = []
    ys: list[float] = []
    with Path(path).open(encoding="utf-8-sig", newline="") as f:
        rd = csv.DictReader(f)
        if rd.fieldnames != ["date", "value"]:
            raise ValueError("CSV header must be exactly: date,value")
        for n, row in enumerate(rd, start=2):
            if None in row or any(v is None for v in row.values()):
                raise ValueError(f"Malformed CSV row {n}")
            label = row["date"].strip()
            dt = _date(label)
            try:
                value = float(row["value"])
            except (ValueError, TypeError):
                raise ValueError(f"Invalid value on row {n}") from None
            if not math.isfinite(value):
                raise ValueError(f"Non-finite value on row {n}; no silent interpolation")
            if xs and dt.toordinal() <= xs[-1]:
                raise ValueError(f"Out-of-order or duplicate date on row {n}")
            dates.append(label)
            xs.append(dt.toordinal())
            ys.append(value)
    if len(ys) < 12:
        raise ValueError("At least 12 observations required for MVP pattern detection")
    x = np.array(xs, dtype=np.float64)
    gaps = np.diff(x)
    warnings = []
    if np.max(gaps) > 2.5 * np.median(gaps):
        warnings.append("Irregular time gaps detected; no imputation performed")
    if np.max(ys) == np.min(ys):
        warnings.append("Constant series: no nontrivial pattern is supported")
    return Series(tuple(dates), x, np.asarray(ys, dtype=np.float64), digest, tuple(warnings))
