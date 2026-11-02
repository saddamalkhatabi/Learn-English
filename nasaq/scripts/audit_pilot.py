#!/usr/bin/env python3
"""Verify exact text/audio/image relationships; never equate file count with learning quality."""
import argparse,datetime,hashlib,json,pathlib,re,subprocess,math
ROOT=pathlib.Path(__file__).resolve().parents[1]
def clean(t):return re.sub('[^A-Z ]','',t.upper()).split()
def distance(a,b):
 row=list(range(len(b)+1))
 for i,x in enumerate(a,1):
  new=[i]
  for j,y in enumerate(b,1):new.append(min(new[-1]+1,row[j]+1,row[j-1]+(x!=y)))
  row=new
 return row[-1]
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--require-complete',action='store_true');args=ap.parse_args()
 d=json.loads((ROOT/'dist/pilot.json').read_text());errors=[];notes=[];audio_count=0;cue_count=0;image_count=0;transcripts=[];total_bytes=0
 expected=len(d['patterns'])*12
 assert len(d['patterns'])==13 and len(d['sentences'])==expected
 assert len({s['id'] for s in d['sentences']})==expected
 assert len({s['en'].casefold() for s in d['sentences']})==expected
 exercises={e['id']:e for e in d['exercises']}
 assert len(exercises)==expected and len({e['prompt'] for e in exercises.values()})==expected
 assert all(all(eid in exercises and exercises[eid]['sentence_id']==s['id'] for eid in s['exercise_ids']) for s in d['sentences'])
 all_paths=set();hashes=set()
 for p in d['patterns']:
  rows=[s for s in d['sentences'] if s['pattern_id']==p['id']]
  assert len(rows)==12 and p['sentence_ids']==[s['id'] for s in rows]
 for s in d['sentences']:
  image=s['image'];file=ROOT/'dist'/image['atlas']
  if file.exists() and image.get('sha256')==hashlib.sha256(file.read_bytes()).hexdigest() and image['status']=='visually_reviewed' and 0<=image['cell']<12:image_count+=1
  else:errors.append(s['id']+': image not verified')
  for gender in ['male','female']:
   r=s['recordings'][gender];p=ROOT/'dist'/r['path'];label=s['id']+'/'+gender
   if not p.is_file() or not r.get('sha256'):errors.append(label+': missing audio');continue
   digest=hashlib.sha256(p.read_bytes()).hexdigest()
   if digest!=r['sha256']:errors.append(label+': digest mismatch')
   if r.get('text')!=s['en']:errors.append(label+': text mismatch')
   if r.get('voice_id')!=('am_adam' if gender=='male' else 'af_bella'):errors.append(label+': voice mismatch')
   if r['path'] in all_paths or digest in hashes:errors.append(label+': duplicate audio file')
   all_paths.add(r['path']);hashes.add(digest)
   ms=round(float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1',str(p)],text=True).strip())*1000)
   if abs(ms-r['duration_ms'])>30:errors.append(label+': duration mismatch')
   words=r.get('words',[])
   if len(words)!=len(s['en'].split()):errors.append(label+': missing word cues')
   for i,w in enumerate(words):
    if w['index']!=i or w['text']!=s['en'].split()[i] or not 0<=w['start_ms']<w['end_ms']<=ms+45 or (i and words[i-1]['end_ms']>w['start_ms']):errors.append(label+': invalid cue')
   if r.get('alignment')!='wav2vec2-ctc-exact-mp3':errors.append(label+': unmeasured alignment')
   if words and (words[-1]['end_ms']-words[0]['start_ms']<300):errors.append(label+': implausibly short speech')
   expected_words=clean(s['en']);actual=clean(r.get('ctc_transcript',''));wer=distance(expected_words,actual)/max(1,len(expected_words));transcripts.append({'id':label,'expected':s['en'],'recognized':r.get('ctc_transcript'),'word_error_rate':round(wer,3)})
   if wer>.25:notes.append(label+': ASR mismatch needs listening review')
   audio_count+=1;cue_count+=len(words);total_bytes+=p.stat().st_size
 result={'schema':1,'generated_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'patterns':len(d['patterns']),'sentences':expected,'unique_sentences':expected,'recordings_verified':audio_count,'word_cues_verified':cue_count,'visual_scenes_reviewed':image_count,'audio_bytes':total_bytes,'structural_errors':errors,'review_notes':notes,'ctc_transcripts':transcripts,'validation_status':'pass' if not errors else 'incomplete','auditory_review':'not an independent human sign-off','acoustic_alignment':'Wav2Vec2 CTC measured on each exact MP3','browser_test_report':'qa-report.json'}
 (ROOT/'dist/pilot-audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
 print(json.dumps({k:v for k,v in result.items() if k not in ['ctc_transcripts']},ensure_ascii=False,indent=2))
 if args.require_complete:assert not errors and audio_count==expected*2 and image_count==expected
if __name__=='__main__':main()
