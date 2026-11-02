#!/usr/bin/env python3
"""Produce two independent Kokoro MP3s per sentence and acoustically align each encoded file.
Adapted from Learn-English render_dual_kokoro.py at 3915ab51. Never times words by length.
Writes verified rows atomically after every recording, and preserves reusable validated assets.
"""
import argparse,hashlib,json,pathlib,subprocess,sys,tempfile,os
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts/upstream'))
from acoustic_pattern_fallback import ForcedAligner
from generate_audio import write_clip
import generate_audio
generate_audio.ROOT=ROOT
from kokoro import KPipeline
import torch

MANIFEST=ROOT/'dist/pilot.json'
def save(data):
 p=MANIFEST;tmp=p.with_suffix('.tmp');tmp.write_text(json.dumps(data,ensure_ascii=False,indent=2));tmp.replace(p)
def duration(p):
 return round(float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1',str(p)],text=True).strip())*1000)
def valid(r,p,text):
 return r.get('text')==text and p.is_file() and r.get('sha256')==hashlib.sha256(p.read_bytes()).hexdigest() and len(r.get('words',[]))==len(text.split()) and all(0<=w['start_ms']<w['end_ms']<=r['duration_ms']+45 for w in r['words'])
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--limit',type=int,default=0);ap.add_argument('--manifest',default='dist/pilot.json');args=ap.parse_args();global MANIFEST;MANIFEST=ROOT/args.manifest
 torch.set_num_threads(2)
 data=json.loads(MANIFEST.read_text());pipeline=None;aligner=None;count=0
 for s in data['sentences']:
  for gender,r in s['recordings'].items():
   p=ROOT/'dist'/r['path'];text=s['en']
   if valid(r,p,text):continue
   if pipeline is None:pipeline=KPipeline(lang_code='a',repo_id='hexgrad/Kokoro-82M')
   # Existing files without matching verified metadata are never silently accepted.
   if p.exists():
    backup=ROOT/'production-backups'/p.name;backup.parent.mkdir(exist_ok=True);p.replace(backup)
   write_clip(pipeline,r['voice_id'],text,p)
   if aligner is None:aligner=ForcedAligner()
   cues=aligner.align(p,text);ms=duration(p)
   r.update({'text':text,'duration_ms':ms,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'words':[{'index':i,'text':text.split()[i],'start_ms':a,'end_ms':b} for i,a,b in cues],'alignment':'wav2vec2-ctc-exact-mp3','status':'structurally_verified','auditory_review':'pending','ctc_transcript':aligner.last_transcript,'produced_at':__import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat()})
   assert valid(r,p,text);save(data);count+=1
   print(f'VERIFIED {s["id"]}/{gender} {ms}ms {len(cues)} words',flush=True)
   if args.limit and count>=args.limit:return
 print('PASS',sum(valid(r,ROOT/'dist'/r['path'],s['en']) for s in data['sentences'] for r in s['recordings'].values()),'verified audio assets',flush=True)
if __name__=='__main__':main()
