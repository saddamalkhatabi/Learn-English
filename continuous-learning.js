/* Continuous English curriculum: all ten groups, 1962 recorded lesson units.
 * Non-destructive: original lesson modules, saved quizzes and MP3 files are untouched.
 */
(function(window, document){
"use strict";
const NAMES=["one","two","three","four","five","six","seven","eight","nine","ten"];
const LABELS=["الأولى","الثانية","الثالثة","الرابعة","الخامسة","السادسة","السابعة","الثامنة","التاسعة","العاشرة"];
const STORE="pattern-universe-continuous-v1";
const $=id=>document.getElementById(id);
const esc=s=>String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
let units=[],index=0,seconds=0,rate=1,turn=0,loaded=false,loading=null,playing=false,player=new Audio(),utter=null,seq=0,frame=0,lastWord=-2,sourceRows=new Map(),groupIndexes={},pairIndexes={},groupData=[];
let error=null;
try{const saved=JSON.parse(localStorage.getItem(STORE)||"{}");index=Math.max(0,Math.floor(saved.index||0));seconds=Math.max(0,Number(saved.seconds)||0);rate=[0.8,1,1.15].includes(saved.rate)?saved.rate:1;turn=Math.max(0,Math.floor(saved.turn||0))}catch(e){}
function save(){try{localStorage.setItem(STORE,JSON.stringify({index,seconds:Math.round(seconds*10)/10,rate,turn}))}catch(e){}}
function status(msg){if($("mlStatus"))$("mlStatus").textContent=msg}
function selected(){return units[index]}
function hasCues(row,text){const arr=text.trim().split(/\s+/);return row&&row.text===text&&row.path&&row.audio_sha256&&row.language==="en"&&Number.isFinite(row.duration_ms)&&Array.isArray(row.cues)&&row.cues.length===arr.length&&row.cues.every((c,i)=>Array.isArray(c)&&c.length===3&&c[0]===i&&c[1]>=0&&c[2]>c[1]&&c[2]<=row.duration_ms+45&&(!i||row.cues[i-1][2]<=c[1]))}
function rememberSource(json,fromPath=false){
 for(const [k,v] of Object.entries(json?.items||{})){
  const row=fromPath?{...v,path:k}:v;
  if(row?.text&&hasCues(row,row.text)&&!sourceRows.has(row.text))sourceRows.set(row.text,row);
 }
}
function entry(group,p,kind,scene,clip){
 return {group,pattern:p.id,patternTitle:p.title,kind,text:scene.en,ar:scene.ar||"",context:scene.context||"",icon:scene.icon||p.scenes?.[0]?.icon||"📖",photo:scene.photo||null,clip};
}
function addGroup(group,db){
 db.items.forEach(p=>{
  const prefix="p"+String(p.id).padStart(2,"0");
  units.push(entry(group,p,"intro",{en:p.explanationEn,ar:p.explanation||"",context:"شرح النمط",icon:"📘"},prefix+"/intro"));
  p.scenes.forEach(s=>units.push(entry(group,p,"scene",s,prefix+"/scene-"+s.id)));
  p.story.forEach(s=>units.push(entry(group,p,"story",{...s,context:"من القصة",icon:"📖"},prefix+"/story-"+s.id)));
  p.dialogue.forEach(s=>units.push(entry(group,p,"dialogue",{...s,context:"حوار "+(s.speaker||""),icon:"🗣️"},prefix+"/dialogue-"+s.id)));
 });
 (db.chapters||[]).forEach(c=>c.lines.forEach(s=>{
  units.push({group,pattern:18,patternTitle:c.title||"Story",kind:"chapter",text:s.en,ar:s.ar||"",context:c.titleAr||c.title||"قصة مترابطة",icon:c.icon||"📖",photo:null,clip:"chapters/c"+String(c.id).padStart(2,"0")+"/line-"+s.id});
 }));
}
async function json(path,optional=false){
 try{const response=await fetch(path);if(!response.ok)throw Error(path+": HTTP "+response.status);return await response.json()}
 catch(e){if(optional)return null;throw e}
}
async function load(){
 if(loaded)return;
 if(loading)return loading;
 loading=(async()=>{
  const groups=await Promise.all(NAMES.map(n=>json("data/group-"+n+".json")));
  groupData=groups;
  for(let i=0;i<groups.length;i++){
   if(groups[i]?.items?.length!==18||groups[i].items.some(p=>p.scenes?.length!==4||p.story?.length!==3||p.dialogue?.length!==2))throw Error("محتوى المجموعة "+(i+1)+" غير مكتمل");
   addGroup(NAMES[i],groups[i]);
  }
  if(units.length!==1962)throw Error("عدد وحدات التعلم غير متوقع: "+units.length);
  const base=await Promise.all([json("data/audio-word-cues.json"),json("data/pattern-audio-index.json")]);
  rememberSource(base[0],true);rememberSource(base[1]);
  const indexes=await Promise.all(NAMES.map(n=>json("data/group-"+n+"-audio-index.json")));
  indexes.forEach((data,i)=>{groupIndexes[NAMES[i]]=data?.items||{}});
  const dual=await Promise.all(NAMES.map(n=>json("data/group-"+n+"-dual-audio-index.json",true)));
  dual.forEach((data,i)=>{pairIndexes[NAMES[i]]=data?.items||{}});
  index=Math.min(index,units.length-1);
  loaded=true;
  renderSelectors();render();
 })().catch(e=>{error=e;status("تعذر تحميل المسار: "+e.message);throw e}).finally(()=>{loading=null});
 return loading;
}
function choice(u){
 const pair=pairIndexes[u.group]?.[u.clip];
 if(hasCues(pair?.female,u.text)&&hasCues(pair?.male,u.text)){
  const voice=turn++%2===0?"female":"male";
  save();
  return pair[voice];
 }
 const original=sourceRows.get(u.text);
 if(original&&hasCues(original,u.text))return original;
 const row=groupIndexes[u.group]?.[u.clip];
 return hasCues(row,u.text)?row:null;
}
function highlighted(i){
 if(!$("mlSentence"))return;
 const words=selected().text.trim().split(/\s+/);
 $("mlSentence").innerHTML=words.map((w,j)=>'<span class="mlWord'+(i===j?" mlActive":"")+'">'+esc(w)+'</span>').join(" ");
}
function wordAt(cues,t){
 let lo=0,hi=cues.length-1,found=-1;
 while(lo<=hi){const mid=(lo+hi)>>1;if(cues[mid][1]<=t){found=mid;lo=mid+1}else hi=mid-1}
 return found>=0&&t<cues[found][2]?cues[found][0]:-1;
}
let activeRow=null;
function stopPlayback(reset=false){
 seq++;playing=false;if(frame)cancelAnimationFrame(frame);frame=0;
 player.pause();player.removeAttribute("src");player.load();
 if(utter){utter.onend=null;utter.onerror=null;utter=null}
 if("speechSynthesis" in window)speechSynthesis.cancel();
 if(reset){seconds=0;activeRow=null}else if(Number.isFinite(player.currentTime)&&player.currentTime>0){seconds=player.currentTime}
 highlighted(-1);save();updateButtons();
}
function tick(token){
 if(token!==seq||!playing)return;
 if(activeRow&&Number.isFinite(player.currentTime)){
  seconds=player.currentTime;
  const word=wordAt(activeRow.cues,seconds*1000);
  if(word!==lastWord){lastWord=word;highlighted(word)}
  save();
 }
 frame=requestAnimationFrame(()=>tick(token));
}
function next(auto=false){
 if(!units.length)return;
 stopPlayback(true);
 if(index>=units.length-1){status("أكملت جميع الدروس والمشاهد! يمكنك البدء من البداية.");render();return}
 index++;seconds=0;save();render();if(auto)start();
}
function previous(){if(!units.length)return;stopPlayback(true);index=Math.max(0,index-1);seconds=0;save();render()}
function pause(){
 if(!playing)return;
 const position=Number.isFinite(player.currentTime)&&player.currentTime>0?player.currentTime:seconds;
 stopPlayback(false);seconds=position;save();status("متوقف مؤقتاً — اضغط متابعة للاستكمال من نفس الموضع");updateButtons();
}
function browserFallback(u,token){
 if(!("speechSynthesis" in window)){playing=false;status("التسجيل غير متوفر ولا يدعم الجهاز النطق الاحتياطي");return}
 status("تنبيه: تسجيل MP3 غير متاح، يجري استخدام نطق الجهاز مؤقتاً");
 const x=new SpeechSynthesisUtterance(u.text);utter=x;x.lang="en-US";x.rate=rate;
 x.onboundary=e=>{
  if(seq!==token)return;
  const w=[...u.text.matchAll(/\S+/g)],hit=w.findIndex((p,i)=>e.charIndex>=p.index&&(i===w.length-1||e.charIndex<w[i+1].index));
  if(hit>=0)highlighted(hit);
 };
 x.onend=()=>{if(token!==seq)return;seconds=0;next(true)};
 x.onerror=()=>{if(token!==seq)return;pause();status("تعذر تشغيل التسجيل ونطق الجهاز؛ يمكن الانتقال يدوياً")};
 speechSynthesis.speak(x);
}
async function start(){
 if(!loaded){try{await load()}catch(e){return}}
 if(playing)return;
 const u=selected();if(!u)return;
 stopPlayback(false);const token=seq;
 playing=true;lastWord=-2;updateButtons();status("تحضير النطق المسجل…");highlighted(-1);
 const row=choice(u);activeRow=row;
 if(!row){seconds=0;browserFallback(u,token);return}
 player.src=row.path;player.playbackRate=rate;
 player.onloadedmetadata=()=>{
  if(token!==seq)return;
  const currentDuration=player.duration;
  if(Number.isFinite(currentDuration)&&Math.abs(currentDuration*1000-row.duration_ms)>700){
   activeRow=null;status("اختلاف مدة التسجيل عن التوقيتات؛ إيقاف التلوين");}
  if(seconds>0&&seconds<currentDuration-0.25){try{player.currentTime=seconds}catch(e){}}
 };
 player.onplaying=()=>{if(token!==seq)return;status("MP3 مسجل · "+(row.voice==="af_bella"?"Bella (أنثى)":row.voice==="am_adam"?"Adam (ذكر)":row.voice||"الصوت الأصلي")+" · مزامنة الكلمات");tick(token)};
 player.onended=()=>{if(token!==seq)return;seconds=0;next(true)};
 player.onerror=()=>{if(token!==seq)return;player.pause();activeRow=null;browserFallback(u,token)};
 try{await player.play()}catch(e){if(token===seq){activeRow=null;browserFallback(u,token)}}
}
function saveScroll(){
 const el=$("mlPanel");if(el&&el.getBoundingClientRect().top<0)el.scrollIntoView({behavior:"smooth",block:"start"});
}
function renderSelectors(){
 const g=$("mlGroupJump");if(!g)return;
 g.innerHTML=NAMES.map((n,i)=>'<option value="'+i+'">المجموعة '+LABELS[i]+'</option>').join("");
 g.addEventListener("change",()=>renderPatternSelector());
 renderPatternSelector();
}
function renderPatternSelector(){
 const g=$("mlGroupJump"),p=$("mlPatternJump");if(!g||!p)return;
 const num=Number(g.value)||0;
 p.innerHTML=groupData[num].items.map((x,i)=>'<option value="'+(i+1)+'">'+(i+1)+". "+esc(x.title)+'</option>').join("");
}
function render(){
 if(!loaded)return;
 const u=selected();if(!u)return;
 const gi=NAMES.indexOf(u.group);
 const labels={intro:"شرح النمط",scene:"المشهد",story:"جملة من القصة",dialogue:"الحوار",chapter:"الفصل القصصي"};
 $("mlGroup").textContent="المجموعة "+LABELS[gi];
 $("mlPattern").textContent=u.patternTitle;
 $("mlKind").textContent=labels[u.kind]||"التعلم";
 $("mlCounter").textContent="الوحدة "+(index+1)+" / "+units.length;
 $("mlPercent").textContent=((index+1)/units.length*100).toFixed(1)+"%";
 $("mlProgress").value=index+1;$("mlProgress").max=units.length;
 $("mlArabic").textContent=u.ar;
 $("mlContext").textContent=u.context;
 $("mlArt").textContent=u.icon;
 highlighted(-1);
 const g=$("mlGroupJump");
 if(g){g.value=String(gi);renderPatternSelector();$("mlPatternJump").value=String(u.pattern)}
 updateButtons();
}
function updateButtons(){
 if(!$("mlPlay"))return;
 $("mlPlay").disabled=!loaded||playing;
 $("mlPause").disabled=!playing;
 $("mlPlay").textContent=seconds>0||index>0?"▶ متابعة من حيث توقفت":"▶ ابدأ من البداية";
 $("mlPrev").disabled=!loaded||index===0;
 $("mlNext").disabled=!loaded||index===units.length-1;
 $("mlRate").value=String(rate);
}
async function open(){
 status("تحميل المجموعات والأصوات الأصلية…");
 try{await load();render();if(!playing)status(index===0?"جاهز لبدء المسار الكامل":"يمكنك متابعة الدراسة من آخر موضع محفوظ")}catch(e){}
}
function onNavigateAway(){if(playing)pause()}
function setup(){
 if(!$("mlPlay"))return;
 $("mlPlay").onclick=()=>start();
 $("mlPause").onclick=pause;
 $("mlPrev").onclick=()=>previous();
 $("mlNext").onclick=()=>next(false);
 $("mlRestart").onclick=()=>{stopPlayback(true);index=0;seconds=0;turn=0;save();render();status("أُعيد المسار للبداية. اضغط ابدأ لتشغيله")};
 $("mlRate").onchange=()=>{rate=Number($("mlRate").value)||1;player.playbackRate=rate;save()};
 $("mlJump").onclick=()=>{
  if(!loaded)return;
  const gn=NAMES[Number($("mlGroupJump").value)||0],pn=Number($("mlPatternJump").value)||1;
  const target=units.findIndex(x=>x.group===gn&&x.pattern===pn&&x.kind==="intro");
  if(target<0)return;
  stopPlayback(true);index=target;seconds=0;save();render();status("انتقلت إلى النمط المحدد. اضغط متابعة لتشغيله");saveScroll();
 };
 document.addEventListener("visibilitychange",()=>{if(document.hidden&&playing)pause()});
 window.addEventListener("pagehide",()=>{if(playing)pause()});
 window.addEventListener("beforeunload",()=>save());
 updateButtons();
}
setup();
window.PATTERN_MARATHON={open,onNavigateAway,getStatus:()=>({total:units.length,index,playing,seconds})};
})(window,document);
