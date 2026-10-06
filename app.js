const $=id=>document.getElementById(id);
const passage='The morning light falls softly across the room. I take a moment to settle in and begin at my own pace. Small details become clearer when I slow down and pay attention to what is around me.';
let phase=0, events=[], pending=new Map(), last=null, baseline=null, result=null, saved=false;
$('passage').textContent=passage;
$('typing').addEventListener('paste',e=>e.preventDefault());
$('typing').addEventListener('drop',e=>e.preventDefault());
$('typing').addEventListener('keydown',e=>{
 if(e.repeat||e.ctrlKey||e.metaKey||e.altKey||!(e.key.length===1||e.key==='Backspace'||e.key==='Delete'||e.key==='Enter'))return;
 const now=performance.now();const index=events.length;
 const expected=passage[$('typing').selectionStart];
 events.push({interval:last===null?0:now-last,dwell:0,backspace:e.key==='Backspace'?1:0,error:e.key.length===1&&e.key!==expected?1:0});
 pending.set(e.code,{index,time:now});last=now;
});
$('typing').addEventListener('keyup',e=>{const p=pending.get(e.code);if(p){events[p.index].dwell=performance.now()-p.time;pending.delete(e.code)}});
$('typing').addEventListener('blur',()=>{pending.clear();last=null});
$('typing').addEventListener('input',()=>{const matched=$('typing').value===passage;const pct=Math.min(100,Math.round($('typing').value.length/passage.length*100));$('progress').textContent=matched?'Passage complete ✓':`${pct}% typed · ${events.length} presses`;$('submit').disabled=!matched||events.length<40});
async function api(path,data){const response=await fetch(path,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});const json=await response.json();if(!response.ok)throw Error(json.error||'Request failed');return json}
$('submit').onclick=async()=>{try{$('error').textContent='';$('submit').disabled=true;const data=await api('/api/analyse',{events,baseline});if(phase===0){baseline=data.features;phase=1;events=[];last=null;pending.clear();$('typing').value='';$('heading').textContent='One more moment.';$('instruction').textContent='Copy the same passage again at your natural pace. We will compare these two exercises, without assuming that either reflects a calm mental state.';$('step').textContent='02 / TYPE & OBSERVE';$('s1').classList.remove('active');$('s2').classList.add('active');$('submit').innerHTML='See my patterns ↗';$('progress').textContent='Ready for your second exercise';$('typing').focus()}else{result=data;showResults()}}catch(e){$('error').textContent=e.message;$('submit').disabled=false}};
function showResults(){phase=2;$('exercise').hidden=true;$('results').hidden=false;$('s2').classList.remove('active');$('s3').classList.add('active');$('step').textContent='03 / YOUR PATTERNS';const f=result.features,d=result.delta;
$('summary').textContent=`Your median time between presses was ${f.median_interval_ms} ms. Compared with your session reference, it ${d.median_interval_ms>=0?'increased':'decreased'} by ${Math.abs(d.median_interval_ms).toFixed(1)} ms. This describes typing changes; it does not establish their cause.`;
const cards=[['Between presses',f.median_interval_ms+' ms','Median interval'],['Key hold',f.median_dwell_ms+' ms','Median dwell time'],['Long pauses',(f.pause_rate*100).toFixed(1)+'%','Intervals longer than 1 second'],['Corrections',(f.backspace_rate*100).toFixed(1)+'%','Backspace presses / all presses']];
$('metrics').replaceChildren(...cards.map(([name,value,caption])=>{const el=document.createElement('div');el.className='metric';const title=document.createElement('span'),v=document.createElement('strong'),c=document.createElement('small');title.textContent=name;v.textContent=value;c.textContent=caption;el.append(title,v,c);return el}));
const vals=events.filter(e=>e.interval>0).map(e=>e.interval);const max=Math.max(...vals,1);const points=vals.map((v,i)=>`${(i/(vals.length-1)*590+5).toFixed(1)},${(100-v/max*90).toFixed(1)}`).join(' ');$('rhythm').innerHTML=`<line x1="0" y1="100" x2="600" y2="100" stroke="#ced7c6"/><polyline points="${points}" fill="none" stroke="#7c9470" stroke-width="1.7"/>`;
$('model').textContent=result.model.available?`Experimental predicted self-report: ${result.model.predicted_self_report}/10. Training source: ${result.model.training_source}. This is a model estimate, not a mental-health score or diagnosis.`:'Research mode: no strain prediction is shown. A model needs real labelled sessions and participant-separated evaluation first. Your measured typing features are available above.';
}
$('rating').oninput=()=>{$('ratingValue').textContent=$('rating').value};
$('save').onclick=async()=>{if(saved)return;try{$('saveStatus').textContent='Saving…';await api('/api/save',{events,participant:$('participant').value,rating:Number($('rating').value),consent:$('consent').checked});saved=true;$('save').disabled=true;$('saveStatus').textContent='Saved on this computer. Thank you for contributing.'}catch(e){$('saveStatus').textContent=e.message}};
$('download').onclick=()=>{const report={project:'MindType Studio',created_at:new Date().toISOString(),reference:baseline,...result,limitation:'Session-level typing comparison. Not a clinical diagnosis. The reference is not proof of a calm state.'};const url=URL.createObjectURL(new Blob([JSON.stringify(report,null,2)],{type:'application/json'}));const a=document.createElement('a');a.href=url;a.download='mindtype-report.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000)};
$('restart').onclick=()=>location.reload();
