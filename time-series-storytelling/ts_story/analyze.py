"""Conservative MVP detectors. Findings are descriptive, never causal."""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from .data import Series


@dataclass(frozen=True)
class Finding:
    pattern: str
    score: float
    anchor: int | None
    evidence: dict
    caveats: tuple[str, ...]


def _robust_scale(a: np.ndarray) -> float:
    med = float(np.median(a))
    return max(float(1.4826 * np.median(np.abs(a - med))), 1e-12)


def inspect(s: Series) -> dict[str, Finding]:
    y = s.values
    n = len(y)
    span = max(float(np.ptp(y)), 1e-12)
    t = (s.xs - s.xs[0]) / (s.xs[-1] - s.xs[0])
    slope, intercept = np.polyfit(t, y, 1)
    pred = slope * t + intercept
    r2 = max(0., 1 - float(np.sum((y - pred)**2)) / max(float(np.sum((y - y.mean())**2)), 1e-12))
    trend = Finding("trend", round(r2, 4), n - 1, {"slope_per_span": float(slope), "r2": r2}, ("Describes association with time, not cause",))
    # Local robust residuals identify an isolated value, not a persistent level change.
    win = max(3, min(9, n // 6))
    residual = np.zeros(n)
    for i in range(n):
        neighbors = [y[j] for j in range(max(0, i-win), min(n, i+win+1)) if j != i]
        residual[i] = y[i] - np.median(neighbors)
    # Scale of first-difference innovations reduces spurious anomaly calls on steep trends.
    d = np.diff(y)
    scale = max(_robust_scale(residual), _robust_scale(d), 0.005 * span)
    # Edges excluded: local context is incomplete there.
    interior = np.abs(residual[2:-2]) / scale
    idx = int(np.argmax(interior)) + 2
    z = float(interior.max())
    # Require a clear return towards the local baseline on both sides.
    isolated = bool(abs(y[idx-1] - y[idx+1]) < 0.25 * span)
    anomaly_score = min(1.0, z / 7.0) if z >= 4.5 and isolated else 0.0
    anomaly = Finding("anomaly", round(anomaly_score, 4), idx if anomaly_score else None,
                      {"robust_local_z": round(z, 3), "local_median": float(y[idx] - residual[idx]), "isolated": isolated},
                      ("Heuristic outlier; verify measurement and context",))
    # Persistent step: compare piecewise-constant fit to both constant and linear fits.
    # Penalize trends by requiring small within-segment slopes and a one-step transition.
    lo = max(5, n // 7)
    hi = n - lo
    best = None
    global_sse = float(np.sum((y - pred)**2))
    for k in range(lo, hi+1):
        a, b = y[:k], y[k:]
        shift = float(np.mean(b) - np.mean(a))
        candidate_sse = float(np.sum((a-a.mean())**2)+np.sum((b-b.mean())**2))
        # Any reasonable linear trend should not be misclassified as a step.
        improve = max(0., 1 - candidate_sse / max(global_sse, 1e-12))
        within_a = abs(float(np.polyfit(np.arange(len(a)), a, 1)[0])) * len(a)
        within_b = abs(float(np.polyfit(np.arange(len(b)), b, 1)[0])) * len(b)
        flat_ratio = (within_a + within_b) / max(abs(shift), 1e-12)
        jump_ratio = abs(y[k] - y[k-1]) / max(abs(shift), 1e-12)
        score = improve if abs(shift) >= 0.35 * span and flat_ratio < .75 and jump_ratio > .5 else 0.
        if best is None or score > best[0]:
            best = (score, k, shift, improve, flat_ratio, jump_ratio)
    score, k, shift, improve, flat_ratio, jump_ratio = best
    score = round(score, 4) if score >= 0.55 else 0.0
    regime = Finding("regime_shift", score, k if score else None,
                     {"split_index": k, "mean_before": float(y[:k].mean()), "mean_after": float(y[k:].mean()),
                      "difference": shift, "linear_fit_improvement": improve, "flatness_ratio": flat_ratio,
                      "transition_jump_ratio": jump_ratio},
                     ("Descriptive level shift, not a statistical change-point test or causal explanation",))
    return {"trend": trend, "regime_shift": regime, "anomaly": anomaly}


def choose(s: Series, requested: str = "auto") -> Finding:
    findings = inspect(s)
    if requested not in ("auto", *findings.keys()):
        raise ValueError(f"Unknown pattern: {requested}")
    if requested != "auto":
        finding = findings[requested]
        if finding.score < (0.55 if requested == "regime_shift" else 0.5):
            raise ValueError(f"Insufficient evidence for requested {requested} (score={finding.score:.2f})")
        return finding
    # Strict gating: an anomaly or step needs clear evidence before overriding trend.
    if findings["regime_shift"].score >= .65:
        return findings["regime_shift"]
    if findings["anomaly"].score >= .70:
        return findings["anomaly"]
    if findings["trend"].score >= .50:
        return findings["trend"]
    return Finding("no_clear_pattern", 0.0, None, {}, ("No compelling supported pattern; do not manufacture a narrative arc",))
