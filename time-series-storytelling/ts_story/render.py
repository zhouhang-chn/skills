"""Frame-addressable 2D renderer. Draw(t) has no dependence on prior frames.

MVP uses Pillow + ffmpeg raw pipe, not external video/image generation.
"""
from __future__ import annotations
import math
from pathlib import Path
import subprocess
import tempfile
from PIL import Image, ImageDraw, ImageFont
from .data import Series
from .audio import synthesize
from .validate import verify_or_raise

BG='#0A1425'; WHITE='#EEF5F5'; DIM='#A4B7BF'; SUB='#6B8391'; GRID='#1D3344'; CYAN='#7FE1C9'; ORANGE='#FDAE76'


def _font(size:int,bold:bool=False):
    fs=(['/usr/share/fonts/opentype/inter/InterDisplay-SemiBold.otf', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf']
        if bold else ['/usr/share/fonts/opentype/inter/InterDisplay-Regular.otf','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'])
    for p in fs:
        if Path(p).exists(): return ImageFont.truetype(p,size)
    return ImageFont.load_default()


def ease(x):
    x=max(0.,min(1.,x))
    return x*x*(3.-2*x)


def _current_beat(spec,t):
    for i,b in enumerate(spec['beats']):
        if t < b['start']+b['duration'] or i==len(spec['beats'])-1:
            return i,b,ease((t-b['start'])/b['duration'])
    raise AssertionError


def point_progress(spec,series:Series,t:float)->float:
    """Reveal position expressed as fractional source index, inspectable and deterministic."""
    n=len(series.values)
    anchor=spec['evidence']['anchor']['index']
    # Monotonic targets; even early anomalies cannot make previously seen points disappear.
    end_context=min(n-1,max(3,round(n*.2)))
    build=max(end_context, min(n-1,anchor-1))
    ends=[0,end_context,build,max(build,anchor),n-1,n-1]
    idx,b,u=_current_beat(spec,t)
    prev=ends[idx-1] if idx else 0
    if idx==0:return 0.
    if idx==5:return float(n-1)
    return float(prev+(ends[idx]-prev)*u)


def point_timings(spec,series:Series,fps=24)->list[float]:
    out=[]
    ix=0
    nframes=math.ceil(spec['duration']*fps)
    for i in range(nframes):
        t=i/fps
        p=point_progress(spec,series,t)
        while ix<=min(len(series.values)-1,math.floor(p)):
            out.append(t);ix+=1
    out.extend([spec['duration']-.01]*(len(series.values)-len(out)))
    return out


def frame(spec:dict,series:Series,t:float,size:tuple[int,int]=(960,540))->Image.Image:
    w,h=size
    if w<480 or h<320:raise ValueError('Minimum size 480x320')
    s=w/960
    # Keep aspect ratio consistent: coordinates scale with width and are shifted vertically.
    v=lambda x,y:(int(x*s),int((y-270)*s+h/2))
    im=Image.new('RGB',size,BG);g=ImageDraw.Draw(im)
    def txt(x,y,label,font_size,color=WHITE,bold=False,anchor=None):
        g.text(v(x,y),label,font=_font(max(8,round(font_size*s)),bold),fill=color,anchor=anchor,stroke_width=0)
    def ln(coords,fill=GRID,width=1):
        g.line([v(x,y) for x,y in coords],fill=fill,width=max(1,round(width*s)),joint='curve')
    idx,b,u=_current_beat(spec,t)
    n=len(series.values);p=point_progress(spec,series,t)
    color=ORANGE if b['kind']=='turn' else CYAN
    # restrained title language + typographic layout
    txt(57,34,'SERIES  /  LAB',13,CYAN,True)
    txt(824,34,f'0{idx+1} / 0{len(spec["beats"])}',13,DIM,True)
    ln([(57,61),(903,61)],GRID)
    txt(57,80,spec['metric'].upper()[:38],15,DIM,True)
    title=b['headline']
    ts=35 if len(title)>25 else 44
    txt(55,108,title,ts,WHITE,True)
    txt(57,164,b['subline'][:83],16,DIM)
    # evidence panel can only read values directly from verified source observations
    refs=b['evidence_refs']
    if refs:
        ref=spec['evidence'][refs[0]]
        val=ref['value'];unit=spec['unit']
        val_label=(f'{val:,.2f}' if abs(val)<1000 else f'{val:,.0f}')+(f' {unit}' if unit else '')
        txt(58,195,ref['date'],12,SUB,True)
        txt(58,211,val_label,21,ORANGE if idx==3 else CYAN,True)
    # plotting region
    l,r,top,bottom=83,889,266,448
    xs=series.xs;ys=series.values
    low=float(min(ys));high=float(max(ys));dy=max(high-low,1e-6)
    low-=dy*.15;high+=dy*.2
    x0=float(xs[0]);xr=max(float(xs[-1]-xs[0]),1.)
    px=lambda i:l+(r-l)*float((xs[i]-x0)/xr)
    py=lambda vv:bottom-(bottom-top)*(float(vv)-low)/(high-low)
    # axis and unobtrusive grid
    for j in range(5):
        yy=top+j*(bottom-top)/4
        ln([(l,yy),(r,yy)],GRID)
        val=high-(high-low)*j/4
        txt(26,yy-7,f'{val:.1f}',11,SUB)
    for j in range(5):
        i=round(j*(n-1)/4)
        xx=px(i)
        ln([(xx,top),(xx,bottom)],GRID)
        txt(xx-14,bottom+10,series.dates[i][:7],10,SUB)
    # draw revealed history including fractional final segment
    curr=min(n-1,max(0,int(math.floor(p))))
    points=[(px(i),py(ys[i])) for i in range(curr+1)]
    if p>curr and curr<n-1:
        q=p-curr
        points.append((px(curr)*(1-q)+px(curr+1)*q,py(ys[curr])*(1-q)+py(ys[curr+1])*q))
    if len(points)>1:
        poly=[(points[0][0],bottom),*points,(points[-1][0],bottom)]
        layer=Image.new('RGBA',size,(0,0,0,0));lg=ImageDraw.Draw(layer)
        lg.polygon([v(x,y) for x,y in poly],fill=(83,202,183,22))
        im=Image.alpha_composite(im.convert('RGBA'),layer).convert('RGB');g=ImageDraw.Draw(im)
        ln(points,CYAN,3)
    for i in range(curr+1):
        xx,yy=px(i),py(ys[i]);rr=2.6 if i<curr else 4.2
        x,y=v(xx,yy)
        g.ellipse((x-round(rr*s),y-round(rr*s),x+round(rr*s),y+round(rr*s)),fill=CYAN)
    if points:
        x,y=v(*points[-1]);rr=max(4,round(5*s))
        g.ellipse((x-rr,y-rr,x+rr,y+rr),fill=WHITE)
    # meaningful emphasis uses evidence anchor position, not freehand numbers
    if idx in (3,4,5) and spec['pattern'] in ('regime_shift','anomaly'):
        a=spec['evidence']['anchor']['index']
        if p >= a:
            xx,yy=px(a),py(ys[a]);r0=8+8*(1-u if idx==3 else .1)
            x,y=v(xx,yy)
            rad=round(r0*s)
            g.ellipse((x-rad,y-rad,x+rad,y+rad),outline=ORANGE,width=max(2,round(2*s)))
            ln([(xx,yy+14),(xx,bottom)],ORANGE,1)
            # callout constrained to safe upper chart region
            ty=max(top+4, yy-34)
            label=series.dates[a]
            txt(max(l+4,min(xx-26,r-95)),ty,label,12,ORANGE,True)
    if idx==4 and spec['pattern']=='regime_shift':
        k=spec['evidence']['anchor']['index']
        for start,end_,col in [(0,k,CYAN),(k,n,ORANGE)]:
            yy=py(float(ys[start:end_].mean()))
            ln([(px(start),yy),(px(end_-1),yy)],col,2)
    # progress section and legend
    ln([(57,485),(903,485)],GRID,2)
    segw=(903-57)/len(spec['beats'])
    for i in range(len(spec['beats'])):
        aa=57+i*segw
        fill=CYAN if i<idx else ORANGE if i==idx else GRID
        ex=aa+segw*(u if i==idx else .92 if i<idx else 0)
        ln([(aa,485),(ex,485)],fill,3)
    txt(57,502,'OBSERVED DATA  /  NOT A FORECAST',11,SUB,True)
    txt(637,502,('SOURCE: '+spec['source'])[:50],10,SUB)
    return im


def render_video(spec:dict,series:Series,output:str|Path,*,fps:int=24,size:tuple[int,int]=(960,540),poster:str|Path|None=None):
    verify_or_raise(spec,series)
    if fps not in (12,24,30):raise ValueError('fps must be 12, 24 or 30')
    w,h=size
    if w%2 or h%2:raise ValueError('Video dimensions must be even')
    output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
    timings=point_timings(spec,series,fps)
    if poster:
        poster=Path(poster);poster.parent.mkdir(parents=True,exist_ok=True)
        frame(spec,series,spec['beats'][4]['start']+spec['beats'][4]['duration']*.88,size).save(poster)
    with tempfile.TemporaryDirectory(prefix='ts-story-') as tmp:
        audio=Path(tmp)/'audio.wav'
        synthesize(series,timings,spec['duration'],audio)
        cmd=['ffmpeg','-hide_banner','-loglevel','error','-y', '-f','rawvideo','-pix_fmt','rgb24','-s',f'{w}x{h}',
             '-r',str(fps),'-i','pipe:0','-i',str(audio),'-c:v','libx264','-preset','veryfast','-crf','20',
             '-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart','-shortest',str(output)]
        p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
        try:
            for fi in range(math.ceil(spec['duration']*fps)):
                b=frame(spec,series,fi/fps,size).tobytes()
                p.stdin.write(b)
            p.stdin.close()
            err=p.stderr.read().decode(errors='replace')
            p.wait()
            if p.returncode:raise RuntimeError(f'ffmpeg exited {p.returncode}: {err[-1200:]}')
        except BaseException:
            p.kill();p.wait()
            if output.exists():output.unlink()
            raise
    return {'path':str(output),'frames':math.ceil(spec['duration']*fps),'fps':fps,'duration':spec['duration']}
