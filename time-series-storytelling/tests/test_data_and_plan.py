import csv
import json
from pathlib import Path
import numpy as np
import pytest
from ts_story.data import load_csv
from ts_story.analyze import choose, inspect
from ts_story.plan import build
from ts_story.validate import verify
from ts_story.render import frame,point_progress,point_timings

ROOT=Path(__file__).resolve().parents[1]

def fixture(name):
    return load_csv(ROOT/'examples'/f'{name}.csv')

def spec(name='step_up'):
    return build(fixture(name),metric='Demo metric',unit='units',source='Synthetic fixture')

@pytest.mark.parametrize('name,pattern',[('step_up','regime_shift'),('growth','trend'),('spike','anomaly'),('flat','no_clear_pattern')])
def test_pattern_selection(name,pattern):
    assert choose(fixture(name)).pattern==pattern

@pytest.mark.parametrize('name',["step_up","spike","growth","flat"])
def test_all_plans_verify(name):
    assert verify(spec(name),fixture(name))==[]

def test_wrong_pattern_gate():
    with pytest.raises(ValueError,match='Insufficient evidence'):
        choose(fixture('flat'),'regime_shift')

def test_data_modified_is_detected(tmp_path):
    p=tmp_path/'values.csv'
    p.write_bytes((ROOT/'examples'/'step_up.csv').read_bytes())
    s=load_csv(p);sp=build(s,metric='a',unit='u',source='Synthetic')
    p.write_text(p.read_text().replace('100.','101.',1))
    assert any('hash mismatch' in e for e in verify(sp,load_csv(p)))

def test_forged_observation_is_blocked():
    sp=spec();sp['evidence']['anchor']['value']+=1
    assert any('not from source' in e for e in verify(sp,fixture('step_up')))

def test_unlinked_numeric_claim_is_blocked():
    sp=spec();sp['beats'][1]['headline']='120% growth'
    assert any('number-free' in e for e in verify(sp,fixture('step_up')))

def test_invalid_evidence_ref_is_blocked():
    sp=spec();sp['beats'][2]['evidence_refs']=['invented']
    assert any('missing evidence ref' in e for e in verify(sp,fixture('step_up')))

def test_noncontiguous_beats_are_blocked():
    sp=spec();sp['beats'][1]['start']+=.3
    assert any('non-contiguous' in e for e in verify(sp,fixture('step_up')))

def test_missing_provenance_is_blocked():
    sp=spec();sp['source']=''
    assert any('Missing source' in e for e in verify(sp,fixture('step_up')))

@pytest.mark.parametrize('rows',[
    [('2025-01','1'),('2025-01','2')],
    [('2025-02','1'),('2025-01','2')],
    [('2025-01','NaN'),('2025-02','3')],
    [('2025-01','1'),('2025-02','inf')],
])
def test_bad_csv_is_not_silently_fixed(tmp_path,rows):
    p=tmp_path/'bad.csv';p.write_text('date,value\n'+'\n'.join(f'{d},{v}' for d,v in (rows*8)))
    with pytest.raises(ValueError):load_csv(p)

def test_sparse_fails(tmp_path):
    p=tmp_path/'sparse.csv';p.write_text('date,value\n2024-01,1\n2024-02,2\n')
    with pytest.raises(ValueError,match='12 observations'):load_csv(p)

def test_irregular_gaps_disclosed(tmp_path):
    p=tmp_path/'gap.csv'
    vals=[f'2023-{i:02d},{i}' for i in range(1,12)] + ['2025-12,15']
    p.write_text('date,value\n'+'\n'.join(vals))
    assert any('Irregular' in w for w in load_csv(p).warnings)

def test_frame_is_pure_deterministic():
    s=fixture('step_up');sp=spec()
    a=frame(sp,s,12.75,size=(640,360)).tobytes()
    frame(sp,s,18.1,size=(640,360))
    b=frame(sp,s,12.75,size=(640,360)).tobytes()
    assert a==b

def test_reveal_monotonicity_and_source_order():
    s=fixture('step_up');sp=spec()
    timeline=[point_progress(sp,s,i*.09) for i in range(260)]
    assert all(a<=b+1e-9 for a,b in zip(timeline,timeline[1:]))
    times=point_timings(sp,s)
    assert len(times)==len(s.values)
    assert all(a<=b for a,b in zip(times,times[1:]))

def test_no_future_value_is_generated():
    sp=spec(); s=fixture('step_up')
    assert max(e['index'] for e in sp['evidence'].values())<len(s.values)
    assert all('forecast' not in b['headline'].lower() for b in sp['beats'])

@pytest.mark.parametrize('name', ['step_up','growth','spike','flat'])
def test_story_json_serializable_for_every_pattern(name):
    json.dumps(spec(name))
