#!/usr/bin/env python3
"""Validate exported HTML: structure, offline packaging; optional real browser smoke test."""
import argparse
import json
import re
import sys
from pathlib import Path

def check_html(path):
    h=path.read_text(encoding='utf-8')
    assert '<script type="application/json" id="dashboard-data">' in h,'Missing JSON payload'
    m=re.search(r'<script type="application/json" id="dashboard-data">(.*?)</script>',h,re.S)
    obj=json.loads(m.group(1))
    assert obj.get('datasets') and obj.get('widgets'),'Missing datasets/widgets'
    assert 'window.dash=dash' in h,'Missing embedded runtime'
    assert '<style>' in h and 'chart-shell' in h,'Missing embedded stylesheet'
    assert not re.search(r'<script\s+[^>]*src=',h,re.I),'External script detected'
    assert not re.search(r'<link\s+[^>]*rel=["\']stylesheet',h,re.I),'External style detected'
    assert not re.search(r'@import\s',h,re.I),'CSS import detected'
    assert not re.search(r'\b(?:fetch|XMLHttpRequest)\s*\(',h),'Network-capable code detected'
    print(f'STRUCTURE PASS: {len(obj["datasets"])} datasets, {len(obj["widgets"])} widgets; {path.stat().st_size:,} bytes; no external runtime links')
    return obj

def browser_smoke(path, obj):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
        page=browser.new_page(viewport={'width':1280,'height':900},device_scale_factor=1)
        errors=[]
        page.on('pageerror',lambda err:errors.append(str(err)))
        page.set_content(path.read_text(encoding='utf-8'),wait_until='load')  # use set_content when file:// is blocked by sandbox policy
        page.locator('.card').first.wait_for()
        assert page.locator('.card').count()==len(obj['widgets'])
        assert page.locator('svg').count()>=1
        page.locator('.evidence-btn').first.click()
        assert page.get_by_role('dialog').count()==1
        assert 'original source query' in page.locator('.drawer').inner_text().lower()
        page.get_by_role('button',name='Close evidence').click()
        selects=page.locator('select')
        if selects.count() and selects.first.locator('option').count()>1:
            old=selects.first.input_value();opt=selects.first.locator('option').first.get_attribute('value')
            if opt==old:opt=selects.first.locator('option').nth(1).get_attribute('value')
            selects.first.select_option(opt)
            assert page.evaluate('window.dash.params()')[obj['params'][0]['id']]==opt
        assert not errors,errors
        print('BROWSER PASS: charts, widgets, Evidence drawer, parameter updates, no JS exceptions')
        page.screenshot(path=str(path.with_suffix('.preview.png')),full_page=True)
        browser.close()

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('html_file',type=Path)
    parser.add_argument('--browser',action='store_true',help='Requires Playwright and Chromium (optional)')
    args=parser.parse_args()
    try:
        obj=check_html(args.html_file)
        if args.browser:browser_smoke(args.html_file,obj)
    except Exception as exc:
        print('CHECK FAILED:',exc,file=sys.stderr)
        sys.exit(1)
