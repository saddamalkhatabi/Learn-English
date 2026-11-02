"""Materialize every exercise reference and provide unseen transfer situations."""
import json,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
CONTEXTS={
'want':['الاشتراك في دورة تصوير','استعارة كتاب عن الفضاء من مكتبة','مساعدة جار مسن في حمل أكياسه','بدء مشروع صغير','تغيير موعد لقاء إلى الغد','تعلّم السباحة','المشاركة في تنظيف شاطئ','كتابة رسالة شكر لمعلمك','زيارة متحف علوم','تقليل وقت استخدام الهاتف','إعداد وجبة صحية','تعلّم ركوب الدراجة'],
'need':['حفظ نسخة احتياطية من ملفاتك قبل التحديث','استبدال كابل تالف قبل العرض','طباعة بطاقة دعوة','تأكيد عنوان قبل توصيل هدية','شراء تذكرة لمتحف','فهم كلمة مجهولة قبل ترجمة جملة','جدولة مهام الغد','تحضير شرائح عرض','طلب مقاس أكبر في متجر','إغلاق النافذة بسبب المطر','تحديث الخريطة قبل الرحلة','مراجعة ميزانية رحلة'],
'have':['تسليم طرد قبل إغلاق المكتب','مراعاة الهدوء في مكتبة','وضع حزام الأمان في السيارة','انتظار دورك في الطابور','الوصول إلى مقابلة في الوقت المحدد','إطعام الحيوان الذي ترعاه','إعادة أداة استعرتها','الالتزام بموعد عمل تطوعي','اتباع تعليمات المختبر','إطفاء الأضواء قبل المغادرة','الرد على دعوة قبل الغد','تسجيل اسمك قبل المشاركة']}
p=ROOT/'dist/pilot.json';d=json.loads(p.read_text());previous={e['id']:e for e in d.get('exercises',[])};d['exercises']=[]
for s in d['sentences']:
 key,n=s['id'].split('-')
 if s['id']+'-transfer' in previous:
  d['exercises'].append(previous[s['id']+'-transfer']);continue
 if key not in CONTEXTS:
  d['exercises'].append({'id':s['id']+'-transfer','type':'unseen_production','sentence_id':s['id'],'pattern_id':s['pattern_id'],'prompt':'عبّر عن فكرة جديدة في سياق مختلف عن '+s['context'],'unseen':True});continue
 context=CONTEXTS[key][int(n)-1];target={'want':'رغبتك في','need':'حاجتك إلى','have':'التزامك بـ'}[key]
 d['exercises'].append({'id':s['id']+'-transfer','type':'unseen_production','sentence_id':s['id'],'pattern_id':s['pattern_id'],'prompt':f'في موقف جديد، عبّر عن {target} {context}. ثم أضف سببًا أو بديلًا بكلماتك أنت.','unseen':True,'grading':'self-assessment; reject exact copies of taught sentences; no fluency score'})
d['provenance']['kokoro_model_revision']='f3ff3571791e39611d31c381e3a41a3af07b4987'
p.write_text(json.dumps(d,ensure_ascii=False,indent=2))
