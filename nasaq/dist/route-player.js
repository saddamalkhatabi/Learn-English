/* Nasaq sequencer: alternate BETWEEN distinct sentences; recordings remain independent. */
(function(root){
'use strict';
class NasaqRoutePlayer{
 constructor({data,audio,storage,onchange=()=>{},now=()=>Date.now(),setTimer=setTimeout,clearTimer=clearTimeout}){
  this.data=data;this.audio=audio;this.storage=storage;this.onchange=onchange;this.now=now;this.setTimer=setTimer.bind(root);this.clearTimer=clearTimer.bind(root);this.timer=null;this.running=false;this.error='';this.boundary=null;this.lastSave=0;this.generation=0;
  let previous;try{previous=JSON.parse(storage.getItem('nasaq-route-v2'))}catch{}
  this.session={schema:2,ids:[],cursor:0,phase:'sentence',offset:0,voice:'male',voiceMode:'alternate',rate:1,mode:'listen',completed:[],autoNextPattern:true,...previous};
  this.session.ids=this.session.ids.filter(id=>data.sentences.some(s=>s.id===id));
  const oldPilot=this.session.ids.length===36&&this.session.ids.every(id=>/^(want|need|have)-/.test(id));
  if(oldPilot&&data.sentences.length>36&&!this.session.filters?.routeId&&!this.session.expandedFromPilot){this.session.ids=data.pattern_order.flatMap(pid=>data.sentences.filter(s=>s.pattern_id===pid).map(s=>s.id));if(this.session.phase==='finished'){this.session.cursor=36;this.session.phase='sentence';this.session.offset=0;this.session.voice='male'}this.session.expandedFromPilot=true;this.save()}
  if(!this.session.ids.length)this.configure({patternIds:data.pattern_order});
  this.session.cursor=Math.min(Math.max(0,this.session.cursor),Math.max(0,this.session.ids.length-1));
  audio.addEventListener('timeupdate',()=>{if(this.session.phase!=='sentence')return;this.session.offset=Number.isFinite(audio.currentTime)?audio.currentTime:0;if(this.now()-this.lastSave>250){this.save();this.lastSave=this.now()}this.emit()});
  audio.addEventListener('ended',()=>{if(this.running&&this.session.phase==='sentence')this.finishSentence()});
  audio.addEventListener('error',()=>{this.error='تعذر تحميل التسجيل. لم نتجاوز الجملة؛ يمكنك المحاولة مجددًا.';this.running=false;this.emit()});
  root.addEventListener?.('pagehide',()=>this.pause());
 }
 configure({patternIds=this.data.pattern_order,stage=0,cefr='',mode='listen',voiceMode='alternate',rate=1,autoNextPattern=true,routeId=''}={}){
  this.pause();const ids=[];for(const pid of [...new Set(patternIds)].filter(id=>this.data.pattern_order.includes(id))){for(const s of this.data.sentences.filter(s=>s.pattern_id===pid&&(!stage||s.difficulty.stage===+stage)&&(!cefr||s.difficulty.cefr===cefr)))ids.push(s.id)}
  this.session={schema:2,ids,cursor:0,phase:'sentence',offset:0,voice:voiceMode==='female'?'female':'male',voiceMode,mode,rate:+rate,completed:[],autoNextPattern,filters:{patternIds,stage:+stage,cefr,routeId}};this.save();this.emit();return ids.length;
 }
 get sentence(){return this.data.sentences.find(s=>s.id===this.session.ids[this.session.cursor])}
 get pattern(){return this.data.patterns.find(p=>p.id===this.sentence?.pattern_id)}
 get recording(){return this.sentence?.recordings[this.session.voice]}
 get progress(){if(this.session.phase==='finished')return 100;return this.session.ids.length?100*(this.session.cursor+(['comparison','exercise'].includes(this.session.phase)?1:(this.recording?.duration_ms?Math.min(1,this.session.offset*1000/this.recording.duration_ms):0)))/this.session.ids.length:0}
 get wordIndex(){const ms=this.session.offset*1000;return this.recording?.words.findIndex(w=>w.start_ms<=ms&&ms<w.end_ms)??-1}
 save(){try{this.storage.setItem('nasaq-route-v2',JSON.stringify(this.session))}catch{this.error='تعذر حفظ موضعك على هذا المتصفح.'}}
 emit(){this.onchange(this)}
 async play(){
  if(!this.sentence){this.error='اختر مسارًا يحتوي جملًا أولًا.';this.emit();return}
  if(this.session.phase==='finished'){this.running=false;this.emit();return}
  this.error='';this.running=true;
  if(this.session.phase==='comparison'){if(this.session.autoNextPattern)this.scheduleComparison();else{this.continueAfterComparison()}this.emit();return}
  if(this.session.phase==='exercise'){this.running=false;this.emit();return}
  const r=this.recording;if(!r||!r.sha256||!r.words?.length||!['structurally_verified','auditory_sample_reviewed'].includes(r.status)){this.running=false;this.error='هذا التسجيل لم يُنتج ويُتحقق منه بعد. لم نستخدم صوتًا بديلًا أو توقيتًا تقديريًا.';this.emit();return}
  const g=++this.generation;const offset=this.session.offset;
  const seek=()=>{if(g!==this.generation)return;try{this.audio.currentTime=Math.max(0,Math.min(offset,(r.duration_ms-10)/1000))}catch{}};
  if(this.audio.getAttribute('src')!==r.path){this.audio.setAttribute('src',r.path);this.audio.load();if(this.audio.readyState>=1)seek();else this.audio.addEventListener('loadedmetadata',seek,{once:true})}else seek();
  this.audio.playbackRate=this.session.rate;
  try{await this.audio.play();if(g!==this.generation||!this.running){this.audio.pause();return}this.emit()}catch(e){if(g!==this.generation)return;this.running=false;this.error='اضغط تشغيل للسماح بالصوت في متصفحك. سيبقى موضع الاستكمال محفوظًا.';this.emit()}
 }
 pause(){this.generation++;this.running=false;if(this.audio){if(this.session?.phase==='sentence'&&this.audio.getAttribute('src')&&Number.isFinite(this.audio.currentTime))this.session.offset=this.audio.currentTime;this.audio.pause()}if(this.timer)this.clearTimer(this.timer);this.timer=null;if(this.session){this.save();this.emit()}}
 finishSentence(){const sid=this.sentence.id;if(!this.session.completed.includes(sid))this.session.completed.push(sid);if(this.session.mode==='interactive'){this.audio.pause();this.session.phase='exercise';this.running=false;this.save();this.emit();return}this.advance()}
 advance(){
  const next=this.data.sentences.find(s=>s.id===this.session.ids[this.session.cursor+1]);
  if(next?.pattern_id!==this.sentence?.pattern_id){this.audio.pause();this.session.phase='comparison';this.session.offset=0;this.save();if(this.running&&this.session.autoNextPattern)this.scheduleComparison();else this.running=false;this.emit();return}
  this.moveCursor();
 }
 scheduleComparison(){if(this.timer)this.clearTimer(this.timer);this.timer=this.setTimer(()=>{this.timer=null;if(this.running)this.continueAfterComparison()},7000)}
 continueAfterComparison(){if(this.timer)this.clearTimer(this.timer);this.timer=null;this.moveCursor()}
 continueAfterExercise(){this.session.phase='sentence';this.running=true;this.advance()}
 moveCursor(){const keepPlaying=this.running;this.generation++;this.audio.pause();if(this.session.cursor+1>=this.session.ids.length){this.session.phase='finished';this.running=false;this.session.offset=0;this.save();this.emit();return}this.session.cursor++;this.session.phase='sentence';this.session.offset=0;this.session.voice=this.session.voiceMode==='alternate'?(this.session.cursor%2?'female':'male'):this.session.voiceMode;this.audio.removeAttribute('src');this.audio.load();this.save();this.emit();if(keepPlaying)this.play()}
 jumpTo(id){const idx=this.session.ids.indexOf(id);if(idx<0)return false;this.pause();this.session.cursor=idx;this.session.phase='sentence';this.session.offset=0;this.session.voice=this.session.voiceMode==='alternate'?(idx%2?'female':'male'):this.session.voiceMode;this.audio.removeAttribute('src');this.audio.load();this.save();this.emit();return true}
 otherVoice(){const was=this.running;this.pause();this.session.voice=this.session.voice==='male'?'female':'male';this.session.offset=0;this.session.phase='sentence';this.audio.removeAttribute('src');this.audio.load();this.save();this.emit();if(was)this.play()}
 setRate(rate){this.session.rate=+rate;this.audio.playbackRate=+rate;this.save();this.emit()}
 seek(seconds){if(this.session.phase!=='sentence')return;const max=(this.recording?.duration_ms||0)/1000;this.session.offset=Math.max(0,Math.min(+seconds,max));if(this.audio.getAttribute('src')===this.recording?.path)this.audio.currentTime=this.session.offset;this.save();this.emit()}
}
if(typeof module!=='undefined')module.exports=NasaqRoutePlayer;else root.NasaqRoutePlayer=NasaqRoutePlayer;
})(typeof window!=='undefined'?window:globalThis);
