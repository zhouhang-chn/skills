/* html-dashboard deterministic offline runtime. No dependencies or remote calls. */
(() => {
'use strict';
const spec = JSON.parse(document.getElementById('dashboard-data').textContent);
const root = document.getElementById('dashboard-root');
const dataMap = new Map(), calcMap = new Map(), cache = new Map();
const params = Object.fromEntries((spec.params || []).map(p => [p.id, p.default ?? p.options[0]]));
const listeners = [];
const byId = id => document.getElementById(id);
const el = (tag, cls, text) => { const n = document.createElement(tag); if(cls)n.className=cls; if(text!==undefined)n.textContent=text; return n; };
const svgEl = (tag, attrs = {}, text) => { const n=document.createElementNS('http://www.w3.org/2000/svg',tag);Object.entries(attrs).forEach(([k,v])=>n.setAttribute(k,String(v)));if(text!==undefined)n.textContent=text;return n; };
const num = n => { if(n===null || n===undefined || n==='')return NaN;const v=Number(n); return Number.isFinite(v)?v:NaN; };
const fmt = (value, kind='compact') => {
  if (value === null || value === undefined || value === '' || !Number.isFinite(Number(value))) return '—';
  const n=Number(value);
  if(kind==='currency') return '$'+Intl.NumberFormat('en-US',{notation:'compact',maximumFractionDigits:1}).format(n);
  if(kind==='money') return '$'+Intl.NumberFormat('en-US',{maximumFractionDigits:2,minimumFractionDigits:2}).format(n);
  if(kind==='percent') return (n*100).toFixed(1)+'%';
  if(kind==='integer') return Intl.NumberFormat('en-US',{maximumFractionDigits:0}).format(n);
  if(kind==='decimal') return Intl.NumberFormat('en-US',{maximumFractionDigits:2}).format(n);
  return Intl.NumberFormat('en-US',{notation:'compact',maximumFractionDigits:1}).format(n);
};
function normalizeDataset(src){
  return (src.rows || []).map(row => Array.isArray(row) ? Object.fromEntries(src.columns.map((c,i)=>[c,row[i]])) : row);
}
Object.entries(spec.datasets).forEach(([name,src])=>dataMap.set(name,{rows:normalizeDataset(src),meta:src}));
(spec.calcs||[]).forEach(c=>calcMap.set(c.id,c));
function evaluate(name,seen = new Set()) {
  if(dataMap.has(name)){const obj=dataMap.get(name);return {status:'ok',data:obj.rows,columns:obj.meta.columns,source:name};}
  if(cache.has(name)) return cache.get(name);
  if(seen.has(name))return {status:'error',reason:'Circular calculation dependency'};
  const c=calcMap.get(name); if(!c)return {status:'missing',reason:'Dataset or calc not found: '+name};
  seen.add(name);
  const upstream = (c.inputs || (c.input?[c.input]:[])).map(id=>evaluate(id,new Set(seen)));
  if(upstream.some(x=>x.status!=='ok'))return {status:'error',reason:'Unable to resolve calc inputs'};
  try{
    let out=[];
    if(c.fn){out=c.fn(...upstream.map(x=>x.data));}
    else if(c.op==='filter'){
      out=upstream[0].data.filter(row=>(c.where||[]).every(cond=>{
        const value=('param' in cond)?params[cond.param]:cond.value;
        if('skip_value' in cond && String(value)===String(cond.skip_value))return true;
        if(cond.operator==='in')return Array.isArray(value)&&value.map(String).includes(String(row[cond.field]));
        if(cond.operator==='gte')return num(row[cond.field])>=num(value);
        if(cond.operator==='lte')return num(row[cond.field])<=num(value);
        return String(row[cond.field])===String(value);
      }));
    }else if(c.op==='group_by'){
      const fields=c.group_by||[];const groups=new Map();
      for(const row of upstream[0].data){
        const key=JSON.stringify(fields.map(f=>row[f]));
        if(!groups.has(key)){const item=Object.fromEntries(fields.map(f=>[f,row[f]]));groups.set(key,{item,counts:{}});}
        const entry=groups.get(key);
        for(const [alias,agg] of Object.entries(c.measures||{})){
          const v=num(row[agg.field]);
          entry.item[alias]=(entry.item[alias]||0)+(agg.op==='count'?1:v);
          entry.counts[alias]=(entry.counts[alias]||0)+1;
        }
      }
      out=[...groups.values()].map(e=>{Object.entries(c.measures||{}).forEach(([alias,a])=>{if(a.op==='avg')e.item[alias]/=e.counts[alias];});return e.item;});
    }else throw new Error('Unknown calc op');
    if(!Array.isArray(out))throw new Error('Calc must return an array of rows');
    const result={status:'ok',data:out,columns:out[0]?Object.keys(out[0]):[]};cache.set(name,result);return result;
  }catch(err){return {status:'error',reason:String(err)};}
}
function collectSources(id,depth=0,seen=new Set()){
  if(depth>20 || seen.has(id))return [];
  seen.add(id);
  if(dataMap.has(id))return [{id,type:'dataset',spec:dataMap.get(id).meta}];
  const c=calcMap.get(id); if(!c)return [{id,type:'missing'}];
  const parents=c.inputs||[c.input];
  return [{id,type:'calc',spec:c},...parents.flatMap(x=>collectSources(x,depth+1,seen))];
}
function emit(){cache.clear();for(const cb of listeners){try{cb();}catch(err){console.error('dashboard callback failed',err);}}}
const dash={
  data:evaluate, params:()=>({...params}),
  setParams(next){Object.entries(next||{}).forEach(([k,v])=>{const p=(spec.params||[]).find(x=>x.id===k);if(p && p.options.includes(v))params[k]=v;});emit();},
  resetParams(){(spec.params||[]).forEach(p=>params[p.id]=p.default??p.options[0]);emit();},
  calc(id,c){if(dataMap.has(id))throw Error('Cannot overwrite source dataset');calcMap.set(id,c);cache.clear();emit();},
  onData(cb){listeners.push(cb);cb();return ()=>{const i=listeners.indexOf(cb);if(i>=0)listeners.splice(i,1);};},
  evidence:collectSources,
  loader(){return {status:'unavailable',reason:'Offline snapshot does not include connectors'};},
  refresh(){return {status:'unavailable',reason:'Snapshot cannot refresh data'};},
  colors:['#315fe9','#12a78b','#f4ab42','#815be3','#dc687b']
};
window.dash=dash;
function aggregation(rows,field,agg='first'){
  if(agg==='count')return rows.length;
  const values=rows.map(r=>num(r[field])).filter(Number.isFinite);if(!values.length)return null;
  if(agg==='sum')return values.reduce((a,b)=>a+b,0);
  if(agg==='avg')return values.reduce((a,b)=>a+b,0)/values.length;
  if(agg==='min')return Math.min(...values);
  if(agg==='max')return Math.max(...values);
  return values[0];
}
function evidenceButton(w){const b=el('button','evidence-btn','↗ Evidence');b.type='button';b.setAttribute('aria-label','Show evidence for '+(w.title||w.id));b.addEventListener('click',()=>showEvidence(w));return b;}
function showEvidence(w){
  closeEvidence();const overlay=el('div','drawer-bg');overlay.id='ev-backdrop';overlay.addEventListener('click',closeEvidence);
  const drawer=el('aside','drawer');drawer.id='ev-drawer';drawer.setAttribute('role','dialog');drawer.setAttribute('aria-modal','true');drawer.setAttribute('aria-label','Chart evidence');
  const top=el('div','drawer-top');const title=el('div');title.append(el('div','eyebrow','TRACEABLE EVIDENCE'),el('h2','',w.title||w.id));
  const close=el('button','close','×');close.setAttribute('aria-label','Close evidence');close.addEventListener('click',closeEvidence);top.append(title,close);drawer.append(top);
  const section=(heading,value,pre=false)=>{drawer.append(el('h3','',heading));drawer.append(pre?el('pre','',value):el('p','',value));};
  section('Visual / metric definition',JSON.stringify({id:w.id,metric:w.field||w.y||null,x:w.x||null,aggregate:w.aggregate||null,params:dash.params()},null,2),true);
  const lineage=w.dataset?collectSources(w.dataset):[];
  section('Data lineage',lineage.map(s=>`${s.type.toUpperCase()} · ${s.id}`).join('  →  ')||'Display text (no dataset).');
  for(const entry of lineage){
    if(entry.type==='calc'){
      section('Transformation: '+entry.id,entry.spec.description||entry.spec.title||'Declarative derived dataset');
      const safe=Object.fromEntries(Object.entries(entry.spec).filter(([k])=>k!=='fn'));section('Operation specification',JSON.stringify(safe,null,2),true);
    }else if(entry.type==='dataset'){
      const d=entry.spec;section('Dataset: '+entry.id,`${d.rows.length} rows · ${d.columns.join(', ')}`);
      const src=d.source||{};
      section('Source',src.label||src.name||'Source not declared');
      if(src.as_of)section('Source date / coverage',src.as_of);
      if(src.query)section('Original source query',src.query,true);
      else section('Original source query','Not included in this snapshot. The displayed calculation is not a replacement for the upstream SQL.');
      if(src.notes)section('Data notes',src.notes);
    }
  }
  const result=w.dataset?evaluate(w.dataset):null;
  if(result){section('Materialized result',`${result.status}: ${result.data?.length??0} row(s). Showing up to 5 rows.`);if(result.status==='ok')section('Result preview',JSON.stringify(result.data.slice(0,5),null,2),true);else section('Error',result.reason||'Unknown');}
  document.body.append(overlay,drawer);close.focus();
}
function closeEvidence(){byId('ev-backdrop')?.remove();byId('ev-drawer')?.remove();}
document.addEventListener('keydown',e=>{if(e.key==='Escape')closeEvidence();});
function createCard(w){
  const card=el('section','card '+w.type);card.style.setProperty('--span',w.span||12);card.dataset.span=String(w.span||12);card.dataset.widgetId=w.id;
  const head=el('div','card-head');const label=el('div');label.append(el('div',w.type==='kpi'?'card-label':'card-title',w.title||w.id));
  if(w.subtitle)label.append(el('div','card-caption',w.subtitle));head.append(label,evidenceButton(w));card.append(head);
  const content=el('div','widget-body');card.append(content);return {card,content};
}
function renderKPI(w,body,rows){
  const v=aggregation(rows,w.field,w.aggregate||'first');body.append(el('div','kpi-number',fmt(v,w.format||'compact')));
  let note=w.note||'';
  const cmp=w.compare;
  if(cmp && v!==null){
    const d=evaluate(cmp.dataset);
    if(d.status==='ok'){
      let basis=null;
      if(cmp.previous_by && params[cmp.selector_param]){
        const selected=params[cmp.selector_param];const all=d.data.map(r=>String(r[cmp.previous_by])).sort();
        const i=all.indexOf(String(selected));const prev=i>0?all[i-1]:null;
        const prevRows=d.data.filter(r=>String(r[cmp.previous_by])===prev);
        basis=aggregation(prevRows,cmp.field||w.field,cmp.aggregate||'first');
      }
      if(basis!==null&&basis!==0){
        const pct=(v-basis)/Math.abs(basis);const label=(pct>=0?'+':'')+(pct*100).toFixed(1)+'%';
        const p=el('div','kpi-detail');const span=el('span','kpi-delta'+(pct<0?' negative':''),label);p.append(span,document.createTextNode('  vs previous period'));body.append(p);return;
      }
    }
  }
  body.append(el('div','kpi-detail',note||'Based on the selected data slice'));
}
function renderLine(w,body,rows){
  const div=el('div','chart-shell');body.append(div);
  const sorted=rows.filter(r=>Number.isFinite(num(r[w.y]))).sort((a,b)=>String(a[w.x]).localeCompare(String(b[w.x])));
  const values=sorted.map(r=>Number(r[w.y])).filter(Number.isFinite);
  if(!values.length){div.append(el('div','empty','No data in this selection'));return;}
  const width=900,height=290,left=70,right=18,top=25,bottom=38,plotW=width-left-right,plotH=height-top-bottom;
  const minY=Math.min(0,...values),maxY=Math.max(...values)*1.12||1;
  const x=i=>left+(sorted.length<=1?plotW/2:i*plotW/(sorted.length-1));
  const y=v=>top+(1-(v-minY)/(maxY-minY))*plotH;
  const svg=svgEl('svg',{viewBox:`0 0 ${width} ${height}`,role:'img','aria-label':w.title||'Line chart'});
  for(let k=0;k<=4;k++){
    const v=minY+(maxY-minY)*k/4,py=y(v);svg.append(svgEl('line',{x1:left,x2:width-right,y1:py,y2:py,class:'gridline'}));svg.append(svgEl('text',{x:left-12,y:py+4,class:'axis','text-anchor':'end'},fmt(v,'compact')));
  }
  const tickIndex=[...new Set([0,Math.round((sorted.length-1)*.25),Math.round((sorted.length-1)*.5),Math.round((sorted.length-1)*.75),sorted.length-1])];
  tickIndex.forEach(i=>{const text=String(sorted[i][w.x]);svg.append(svgEl('text',{x:x(i),y:height-13,class:'axis','text-anchor':'middle'},text));});
  const points=sorted.map((r,i)=>[x(i),y(num(r[w.y]))]);
  const d=points.map(([a,b],i)=>(i?'L':'M')+a.toFixed(1)+','+b.toFixed(1)).join(' ');
  svg.append(svgEl('path',{d:d+` L ${points[points.length-1][0]},${y(0)} L ${points[0][0]},${y(0)} Z`,class:'line-fill'}));
  svg.append(svgEl('path',{d,class:'line-path'}));
  sorted.forEach((r,i)=>{const match=String(r[w.x])===String(params[w.highlight_param]);const circle=svgEl('circle',{cx:x(i),cy:y(num(r[w.y])),r:match?6:3.3,class:'dot'+(match?' selected':'')});circle.append(svgEl('title',{},String(r[w.x])+': '+fmt(r[w.y],w.format)));svg.append(circle);});
  div.append(svg);
}
function renderBar(w,body,rows){
  const div=el('div','chart-shell');body.append(div);
  const sorted=rows.filter(r=>Number.isFinite(num(r[w.y]))).sort((a,b)=>num(b[w.y])-num(a[w.y])).slice(0,w.limit||8);
  if(!sorted.length){div.append(el('div','empty','No data in this selection'));return;}
  const width=490,left=170,right=76,top=4,rowHeight=38,height=sorted.length*rowHeight+10,max=Math.max(...sorted.map(r=>num(r[w.y])),1);
  const svg=svgEl('svg',{viewBox:`0 0 ${width} ${height}`,role:'img','aria-label':w.title||'Bar chart'});
  sorted.forEach((r,i)=>{
    const py=top+i*rowHeight,v=num(r[w.y]),barWidth=v/max*(width-left-right);
    const label=String(r[w.x]);const short=label.length>24?label.slice(0,22)+'…':label;
    const t=svgEl('text',{x:left-12,y:py+21,class:'bar-label','text-anchor':'end'},short);t.append(svgEl('title',{},label));svg.append(t);
    svg.append(svgEl('rect',{x:left,y:py+8,width:width-left-right,height:18,rx:5,fill:'#f0f3f7'}));
    const bar=svgEl('rect',{x:left,y:py+8,width:Math.max(0,barWidth),height:18,rx:5,fill:'#4b76ec'});bar.append(svgEl('title',{},label+': '+fmt(v,w.format)));svg.append(bar);
    svg.append(svgEl('text',{x:width-right+11,y:py+21,class:'bar-value'},fmt(v,w.format)));
  });div.append(svg);
}
function renderTable(w,body,rows){
  const wrap=el('div','table-wrap');body.append(wrap);
  let sorted=[...rows];if(w.sort_by)sorted.sort((a,b)=>num(b[w.sort_by])-num(a[w.sort_by]));sorted=sorted.slice(0,w.limit||20);
  if(!sorted.length){wrap.append(el('div','empty','No matching rows'));return;}
  const table=el('table');const thead=el('thead'),hrow=el('tr');
  (w.columns||[]).forEach(c=>{const th=el('th',c.format?'num':'',c.title||c.field);hrow.append(th);});thead.append(hrow);table.append(thead);
  const tbody=el('tbody');sorted.forEach(r=>{const tr=el('tr');(w.columns||[]).forEach(c=>{const v=c.format?fmt(r[c.field],c.format):String(r[c.field]??'—');tr.append(el('td',c.format?'num':'',v));});tbody.append(tr);});table.append(tbody);wrap.append(table);
}
function renderWidget(w,body){body.replaceChildren();if(w.type==='custom')return;if(w.type==='text'){body.append(el('p','desc-text',w.text||''));return;}
  const res=evaluate(w.dataset);if(res.status!=='ok'){body.append(el('div','empty','Unable to load dataset: '+(res.reason||res.status)));return;}
  if(w.type==='kpi')renderKPI(w,body,res.data);
  if(w.type==='line')renderLine(w,body,res.data);
  if(w.type==='bar')renderBar(w,body,res.data);
  if(w.type==='table')renderTable(w,body,res.data);
}
function init(){
  const app=el('main','dashboard');app.id='dashboard';
  const header=el('header','header'),hleft=el('div');hleft.append(el('div','eyebrow',spec.kicker||'ANALYTICS / DASHBOARD'),el('h1','',spec.title));
  if(spec.subtitle)hleft.append(el('p','subtitle',spec.subtitle));
  const hright=el('div','header-side');hright.append(el('div','status','Self-contained snapshot'),el('div','asof',spec.metadata?.as_of||'Offline view · No live refresh'));
  header.append(hleft,hright);app.append(header);
  const toolbar=el('section','toolbar'),filters=el('div','filter-wrap');toolbar.setAttribute('aria-label','Dashboard filters');
  (spec.params||[]).forEach(p=>{
    const block=el('div','filter');const label=el('label','',p.label||p.id),select=el('select');select.id='filter-'+p.id;label.htmlFor=select.id;
    p.options.forEach(v=>{const option=el('option','',String(v));option.value=String(v);select.append(option);});select.value=String(params[p.id]);
    select.addEventListener('change',()=>dash.setParams({[p.id]:select.value}));block.append(label,select);filters.append(block);
  });
  toolbar.append(filters,el('div','toolbar-note','Filters recalculate local snapshots'));app.append(toolbar);
  const grid=el('div','grid');const drawn=[];
  (spec.widgets||[]).forEach(w=>{const {card,content}=createCard(w);grid.append(card);drawn.push([w,content]);});app.append(grid);
  const footer=el('footer','footer');footer.append(el('span','','Generated with html-dashboard · Portable HTML / JS / SVG'),el('span','','Evidence describes bundled data, not a live warehouse connection'));app.append(footer);
  root.append(app);
  dash.onData(()=>{
    (spec.params||[]).forEach(p=>{const sel=byId('filter-'+p.id);if(sel)sel.value=String(params[p.id]);});
    drawn.forEach(([w,body])=>renderWidget(w,body));
  });
}
init();
})();
