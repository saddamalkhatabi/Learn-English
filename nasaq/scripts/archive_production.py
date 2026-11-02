"""Create an auditable, self-contained media/production archive. No credentials or model weights."""
import datetime,hashlib,json,pathlib,zipfile
ROOT=pathlib.Path(__file__).resolve().parents[1];dist=ROOT/'dist';core=json.loads((dist/'pilot.json').read_text());extra=json.loads((dist/'supplement.json').read_text());records=[];assets=set()
for scope,data in [('curriculum',core),('supplement',extra)]:
 for s in data['sentences']:
  for gender,r in s['recordings'].items():
   f=dist/r['path'];assert f.is_file() and hashlib.sha256(f.read_bytes()).hexdigest()==r['sha256']
   assets.add(r['path']);records.append({'sentence_id':s['id'],'scope':scope,'text':s['en'],'gender':gender,'voice_id':r['voice_id'],'path':r['path'],'sha256':r['sha256'],'duration_ms':r['duration_ms'],'alignment':r['alignment'],'words':r['words'],'produced_at':r.get('produced_at'),'auditory_review':r.get('auditory_review','pending')})
  if scope=='curriculum':assets.add(s['image']['atlas'])
index={'schema':1,'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'site_project_id':'appgprj_6ae7c48ef1b481919c4655e4e52d4159','revision':core['revision'],'storage':'Sites versioned source repository and this downloadable archive; no GitHub Actions execution claimed','core_patterns':len(core['patterns']),'core_sentences':len(core['sentences']),'core_recordings':sum(r['scope']=='curriculum' for r in records),'supplement_sentences':len(extra['sentences']),'supplement_recordings':sum(r['scope']=='supplement' for r in records),'distinct_voice_files':len(records),'scene_atlases':len({s['image']['atlas'] for s in core['sentences']}),'records':records,'files':{a:hashlib.sha256((dist/a).read_bytes()).hexdigest()for a in sorted(assets)}}
(dist/'generation-index.json').write_text(json.dumps(index,ensure_ascii=False,indent=2))
out=dist/'downloads/nasaq-media-library-20261102.zip';out.parent.mkdir(exist_ok=True)
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for rel in sorted(assets):z.write(dist/rel,'dist/'+rel)
 for name in ['pilot.json','supplement.json','curriculum.json','pilot-audit.json','qa-report.json','generation-index.json','index.html','app.js','data.js','style.css','sw.js','manifest.json','icon.svg','source.json','route-player.js','pilot-ui.js','learning.js','enhancements.js']:z.write(dist/name,'dist/'+name)
 for base in ['scripts','tests','.github/workflows','docs']:
  for f in (ROOT/base).rglob('*'):
   if f.is_file() and '__pycache__' not in str(f) and f.suffix in ['.py','.txt','.md','.yml','.cjs','.json']:z.write(f,str(f.relative_to(ROOT)))
 for name in ['README.md','verify.mjs']:z.write(ROOT/name,name)
 z.writestr('ARCHIVE-README.txt','Nasaq full curriculum media archive. Preserve sentence IDs, exact text, voice IDs, SHA-256 and independent word timings together. Source hosting: Sites. GitHub Actions workflow is supplied but was not executed for this release. No API keys or model weights are included. See README.md and generation-index.json. A null produced_at means no per-file generation timestamp was recorded. The archive creation timestamp is not a substitute for the original generation time; none is fabricated.')
print(json.dumps({'archive':str(out),'bytes':out.stat().st_size,'core_recordings':index['core_recordings'],'supplement_recordings':index['supplement_recordings'],'atlases':index['scene_atlases']}))
