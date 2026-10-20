"""Minimal original synthesized data sonification (no third-party samples)."""
from __future__ import annotations
import math
from pathlib import Path
import wave
import numpy as np
from .data import Series


def synthesize(series: Series, timings: list[float], duration: float, path: str | Path, sr:int=32000):
    samples = np.zeros(int(math.ceil(duration*sr)),dtype=np.float64)
    y=series.values
    span=max(float(np.ptp(y)),1e-9)
    for i,(v,at) in enumerate(zip(y,timings)):
        # Sonification is relative to observed data range, not a literal temperature frequency.
        midi=54+22*(float(v)-float(y.min()))/span
        hz=440*2**((midi-69)/12)
        tau=.19 if i % 3 else .3
        dur=min(.9,duration-at)
        if dur<=0:continue
        t=np.arange(int(dur*sr))/sr
        env=(1-np.exp(-t/.006))*np.exp(-t/tau)
        tone=(np.sin(2*np.pi*hz*t)+.18*np.sin(2*np.pi*2*hz*t))*env
        a=int(at*sr);b=min(len(samples),a+len(tone))
        samples[a:b]+=.24*tone[:b-a]
    # A restrained tonal pad: fixed D/A intervals, gentle amplitude movement.
    t=np.arange(len(samples))/sr
    pad=.025*(np.sin(2*np.pi*146.83*t)+.4*np.sin(2*np.pi*220*t))*(1+.25*np.sin(2*np.pi*.11*t))
    samples+=pad
    # Fixed envelope and normalization, avoids clipping regardless of sample density.
    edge=np.minimum(1., t/.12)*np.minimum(1.,np.maximum(0,duration-t)/.7)
    samples*=edge
    peak=max(float(np.max(np.abs(samples))),1e-8)
    samples=np.clip(samples/peak*.82,-1,1)
    Path(path).parent.mkdir(parents=True,exist_ok=True)
    with wave.open(str(path),'wb') as f:
        f.setnchannels(1);f.setsampwidth(2);f.setframerate(sr)
        f.writeframes(np.round(samples*32767).astype('<i2').tobytes())
