"""CLI: plan, verify, render, run."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from .data import load_csv
from .plan import build, save
from .validate import verify


def main(argv=None):
    p=argparse.ArgumentParser(prog='ts-story',description='Evidence-grounded time-series video stories')
    sp=p.add_subparsers(dest='command',required=True)
    pl=sp.add_parser('plan',help='Analyze CSV and create verifiable Story Spec')
    pl.add_argument('csv');pl.add_argument('--metric',required=True);pl.add_argument('--unit',default='')
    pl.add_argument('--source',required=True);pl.add_argument('--pattern',choices=['auto','trend','regime_shift','anomaly'],default='auto');pl.add_argument('--out',required=True)
    ve=sp.add_parser('verify',help='Check spec claims and provenance against original CSV')
    ve.add_argument('spec');ve.add_argument('--csv',required=True)
    re=sp.add_parser('render',help='Deterministically render video from spec')
    re.add_argument('spec');re.add_argument('--csv',required=True);re.add_argument('--out',required=True)
    re.add_argument('--poster');re.add_argument('--fps',type=int,default=24);re.add_argument('--size',default='960x540')
    ru=sp.add_parser('run',help='Plan, verify and render in one command')
    ru.add_argument('csv');ru.add_argument('--metric',required=True);ru.add_argument('--unit',default='')
    ru.add_argument('--source',required=True);ru.add_argument('--pattern',choices=['auto','trend','regime_shift','anomaly'],default='auto')
    ru.add_argument('--outdir',default='output');ru.add_argument('--fps',type=int,default=24);ru.add_argument('--size',default='960x540')
    a=p.parse_args(argv)
    s=load_csv(a.csv)
    if a.command in ('plan','run'):
        spec=build(s,metric=a.metric,unit=a.unit,source=a.source,pattern=a.pattern)
        specpath=Path(a.out) if a.command=='plan' else Path(a.outdir)/'story.json'
        save(spec,specpath)
        print('SPEC',specpath,'PATTERN',spec['pattern'],'SCORE',spec['confidence_heuristic'])
        if a.command=='plan':return 0
    else:
        spec=json.loads(Path(a.spec).read_text(encoding='utf8'))
    errs=verify(spec,s)
    if errs:
        for e in errs:print('FAIL',e)
        return 2
    print('VERIFY PASS; source hash:',s.sha256[:16])
    if a.command=='verify':return 0
    from .render import render_video
    path=Path(a.out) if a.command=='render' else Path(a.outdir)/'film.mp4'
    poster=Path(a.poster) if a.command=='render' and a.poster else path.with_suffix('.png')
    try:
        w,h=map(int,a.size.split('x'))
        result=render_video(spec,s,path,fps=a.fps,size=(w,h),poster=poster)
    except (ValueError,RuntimeError) as e:
        p.error(str(e))
    print('VIDEO',result,'POSTER',poster)
    return 0

if __name__=='__main__':raise SystemExit(main())
