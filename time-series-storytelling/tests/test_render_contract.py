import math
from pathlib import Path
from ts_story.data import load_csv
from ts_story.plan import build
from ts_story.render import frame, point_timings

ROOT=Path(__file__).resolve().parents[1]

def test_all_archetypes_have_visually_valid_frames():
    for name in ['step_up','growth','spike','flat']:
        series=load_csv(ROOT/'examples'/f'{name}.csv')
        spec=build(series,metric='Demo',unit='units',source='Synthetic fixture')
        times=point_timings(spec,series)
        assert len(times)==len(series.values)
        assert max(times)<spec['duration']
        for t in [0.0,spec['beats'][3]['start']+1.2,spec['duration']-.01]:
            im=frame(spec,series,t,(480,320))
            assert im.size==(480,320)
            assert im.getbbox() is not None
