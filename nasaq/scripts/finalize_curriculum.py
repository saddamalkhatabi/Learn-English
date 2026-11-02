import json,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
p=ROOT/'dist/pilot.json';d=json.loads(p.read_text());c=json.loads((ROOT/'dist/curriculum.json').read_text());meta={p['id']:p for p in c['patterns']};known={e['id']:e for e in d.get('exercises',[])}
for pattern in d['patterns']:
 m=meta[pattern['id']];pattern['keywords']=m['keywords'];pattern['comparison']={'ar':m['comparison_ar'],'en':m['comparison_en']};pattern['group_id']='g01' if pattern['id'] in [1,13,2,3] else 'g02' if pattern['id']<=6 else 'g03' if pattern['id']<=9 else 'g04'
for s in d['sentences']:
 pp=next(p for p in d['patterns'] if p['id']==s['pattern_id']);s['group_id']=pp['group_id']
 eid=s['exercise_ids'][0]
 if eid not in known:known[eid]={'id':eid,'type':'unseen_production','sentence_id':s['id'],'pattern_id':s['pattern_id'],'prompt':f'تخيل موقفًا جديدًا مختلفًا عن «{s["context"]}». استخدم {pp["form"]} بفعل أو فاعل أو مكان لم يظهر في المثال؛ ثم أضف سببًا.','unseen':True,'grading':'self-assessment; exact copies of taught examples rejected'}
 known[eid]['prompt_en']='Express a new idea with the pattern. Change the person, action, or place; do not copy a sentence you have already seen.'
d['exercises']=[known[s['exercise_ids'][0]] for s in d['sentences']];p.write_text(json.dumps(d,ensure_ascii=False,indent=2));print('Finalized',len(d['exercises']),'linked production challenges')
