"""Author the 36 sentence pilot. Stable IDs and asset keys are independent of display order."""
import json,pathlib,re
ROOT=pathlib.Path(__file__).resolve().parents[1]
DATA=[
(1,'want','I want to + verb','أعبّر عن رغبتي',[
('I want to learn English.','أريد تعلّم الإنجليزية.','التعلّم في المنزل','شخص يدرس الإنجليزية بدفتر وحاسوب'),
('I want to go home.','أريد الذهاب إلى المنزل.','العودة إلى البيت','شخص يعود إلى منزله بعد يوم طويل'),
('I want to buy a new phone.','أريد شراء هاتف جديد.','متجر إلكترونيات','متسوق يقارن الهواتف في متجر'),
('I want to visit my friend.','أريد زيارة صديقي.','لقاء صديق','زيارة صديق عند باب بيته'),
('I want to ask you something.','أريد أن أسألك عن شيء.','حديث مع زميل','زميل يطلب دورًا في الحديث ليطرح سؤالًا'),
('I want to improve my pronunciation.','أريد تحسين نطقي.','التدرّب على النطق','متعلّمة تتدرّب بسماعات وميكروفون'),
('I want to understand this lesson.','أريد فهم هذا الدرس.','طلب التوضيح','متعلّم يركز في درس مع معلم'),
('I want to travel next year.','أريد السفر العام المقبل.','التخطيط للسفر','مسافر يخطط لرحلة بجوار حقيبة وتقويم'),
('I want to make a difference.','أريد إحداث فرق.','العمل التطوعي','متطوع يقدّم مستلزمات لأسرة في مركز مجتمعي'),
('I want to become more confident.','أريد أن أصبح أكثر ثقة.','الاستعداد للتقديم','شخص يتدرّب على تقديم عرض بثقة'),
('I want to know what happened.','أريد معرفة ما حدث.','فهم موقف غير متوقع','شخصان يناقشان ما حدث بجانب دراجة معطلة'),
('I want to spend more time with my family.','أريد قضاء وقت أطول مع أسرتي.','وقت العائلة','أسرة تقضي وقتًا دافئًا معًا في غرفة المعيشة')]),
(13,'need','I need to + verb','أعبّر عما أحتاج إلى فعله',[
('I need to drink some water.','أحتاج إلى شرب بعض الماء.','الاحتياجات الأساسية','متنزه عطشان يشرب الماء'),
('I need to catch the bus.','أحتاج إلى اللحاق بالحافلة.','الانتقال في المدينة','مسافر يتحقق من الوقت ويستعجل إلى محطة الحافلة'),
('I need to finish this report.','أحتاج إلى إنهاء هذا التقرير.','إنجاز مهمة','موظف ينهي تقريرًا على حاسوبه'),
('I need to see a doctor.','أحتاج إلى زيارة طبيب.','طلب الرعاية','شخص مريض يتصل لحجز موعد طبي'),
('I need to charge my phone.','أحتاج إلى شحن هاتفي.','الاستعداد للخروج','شخص يوصل هاتفًا منخفض البطارية بالشاحن'),
('I need to get some fuel.','أحتاج إلى التزوّد ببعض الوقود.','محطة الوقود','سائق يملأ سيارته بالوقود'),
('I need to buy some bread.','أحتاج إلى شراء بعض الخبز.','التسوق اليومي','متسوق يشتري خبزًا طازجًا من مخبز'),
('I need to ask for help.','أحتاج إلى طلب المساعدة.','حل مشكلة','طالب يطلب مساعدة معلم في واجبه'),
('I need to find my hotel.','أحتاج إلى العثور على فندقي.','مدينة جديدة','مسافر يراجع خريطة للوصول إلى الفندق'),
('I need to take a break.','أحتاج إلى أخذ استراحة.','الراحة بعد الجهد','شخص متعب يستريح على مقعد في حديقة'),
('I need to fix the kitchen tap.','أحتاج إلى إصلاح صنبور المطبخ.','صيانة المنزل','شخص يصلح صنبورًا يسرّب الماء'),
('I need to talk to my team before we decide.','أحتاج إلى التحدث مع فريقي قبل أن نتخذ قرارًا.','اتخاذ قرار مشترك','زملاء يتحاورون حول قرار في اجتماع')]),
(2,'have','I have to + verb','أعبّر عن الالتزام والضرورة',[
('I have to finish my work.','عليّ أن أنهي عملي.','موعد نهائي للعمل','موظف ينهي تقريرًا قبل الموعد المحدد'),
('I have to catch the bus.','عليّ أن ألحق بالحافلة.','موعد المغادرة','مسافر يستعجل باتجاه الحافلة'),
('I have to leave now.','عليّ أن أغادر الآن.','المغادرة في الوقت المحدد','زميل يرتدي سترته ويغادر المكتب'),
('I have to study for my exam.','عليّ أن أدرس لامتحاني.','الاستعداد للامتحان','طالب يدرس بتركيز بين كتبه'),
('I have to pick up my child from school.','عليّ أن أصطحب طفلي من المدرسة.','مسؤولية أسرية','أحد الوالدين يستقبل طفله عند المدرسة'),
('I have to pay the electricity bill.','عليّ أن أدفع فاتورة الكهرباء.','التزام منزلي','شخص يسدد فاتورة كهرباء عند مكتبه'),
('I have to clean the kitchen.','عليّ أن أنظّف المطبخ.','الترتيب بعد الطهو','شخص يرتب مطبخًا بعد إعداد الطعام'),
('I have to show my passport.','عليّ أن أبرز جواز سفري.','إجراءات السفر','مسافر يبرز جوازه في المطار'),
('I have to wait for my appointment.','عليّ أن أنتظر موعدي.','الانتظار في العيادة','شخص ينتظر في غرفة انتظار عيادة'),
('I have to wear a helmet on this site.','عليّ أن أرتدي خوذة في هذا الموقع.','قواعد السلامة','عامل يرتدي خوذة واقية في موقع بناء'),
('I have to return this book today.','عليّ أن أعيد هذا الكتاب اليوم.','موعد إعادة كتاب','شخص يعيد كتابًا عند مكتب المكتبة'),
('I have to get up early tomorrow.','عليّ أن أستيقظ مبكرًا غدًا.','الاستعداد ليوم جديد','شخص يستيقظ عند الفجر وبجانبه منبّه')])]
LEVELS=['فهم النمط','توسيع النمط','المقارنة في موقف','الاستخدام الحقيقي','ترابط الأفكار','الإنتاج والطلاقة']
result={'schema':2,'revision':'rich-patterns-20261102','title':'المجموعة الأولى: الرغبة والحاجة والالتزام','philosophy':'تكرار النمط عبر جمل متنوعة، لا تكرار الجملة نفسها بصوتين.','pattern_order':[1,13,2],'sentences':[],'patterns':[],'provenance':{'source_repo':'saddamalkhatabi/Learn-English','source_commit':'3915ab51e5fd6c0af85ad57539c64895d18c0dbf','alignment':'Wav2Vec2 CTC on each exact encoded MP3; no estimated word timing'}}
for pid,key,form,title,rows in DATA:
 ids=[]
 for i,(en,ar,context,scene) in enumerate(rows):
  sid=f'{key}-{i+1:02d}';ids.append(sid)
  result['sentences'].append({'id':sid,'pattern_id':pid,'group_id':'g01','en':en,'ar':ar,'context':context,'scene_description':scene,'image':{'id':'scene-'+sid,'atlas':f'assets/scenes/{key}-atlas.webp','cell':i,'columns':3,'rows':4,'status':'pending_visual_review','origin':'generated_photorealistic'},'difficulty':{'cefr':'A1' if i<6 else 'A2','stage':i//2+1,'stage_label':LEVELS[i//2]},'related_pattern_ids':[x for x in [1,13,2,3] if x!=pid],'vocabulary':[w.lower().strip('.,?') for w in en.split() if len(w.strip('.,?'))>3],'exercise_ids':[sid+'-transfer'],'recordings':{v:{'voice_id':voice,'path':f'assets/audio/{sid}-{v}.mp3','status':'pending','words':[]} for v,voice in [('male','am_adam'),('female','af_bella')]}})
 result['patterns'].append({'id':pid,'key':key,'form':form,'title':title,'sentence_ids':ids,'group_id':'g01','level':'A1–A2','comparison':{'ar':{'want':'want to رغبة؛ need to حاجة؛ have to التزام أو ضرورة؛ I’d like to طلب ألطف.','need':'need to يركز على الحاجة؛ have to على الالتزام أو الضرورة، وقد يصح التعبيران في الموقف نفسه.','have':'have to التزام أو ضرورة؛ don’t have to يعني عدم الضرورة، وليس المنع.'}[key],'en':{'want':'I want to go home, but I have to finish my work.','need':'I need to rest, but I have to attend the meeting.','have':"I have to work today, but I don't have to work tomorrow."}[key]},'transfer':{'prompt':{'want':'أنت في مكتبة جديدة. عبّر عن رغبتك في استعارة كتاب عن الفضاء؛ ثم غيّر فكرتك إلى تعلّم مهارة جديدة.','need':'أنت على وشك دخول اجتماع عبر الإنترنت، لكن الاتصال ضعيف. عبّر عن حاجتك إلى العثور على مكان آخر.','have':'أخبر صديقك بالتزام مختلف لديك مساء اليوم، ثم أخبره بشيء لست مضطرًا إلى فعله.'}[key],'unseen':True}})
out=ROOT/'dist/pilot.json'
if out.exists():
 old=json.loads(out.read_text())
 if len(old.get('patterns',[]))>3:raise SystemExit('Foundation builder will not replace the expanded curriculum. Use expand_curriculum.py and finalize_curriculum.py.')
 byid={s['id']:s for s in old['sentences']}
 for s in result['sentences']:
  prev=byid.get(s['id'])
  if prev and prev['en']==s['en']:
   s['recordings']=prev['recordings'];s['image']=prev['image']
out.write_text(json.dumps(result,ensure_ascii=False,indent=2))
print('Authored',len(result['patterns']),'patterns /',len(result['sentences']),'distinct sentences')
