"""Expand the existing 13 authored patterns to 12 varied sentences each. Preserve all valid assets."""
import json,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
BLOCKS={
3:('like',"I'd like to + verb",'الطلب المهذب',"""
I'd like to book a room.|أود حجز غرفة.|استقبال الفندق|Guest booking a room at a hotel reception
I'd like to order lunch.|أود طلب الغداء.|طلب الطعام|Customer politely ordering lunch from a waiter
I'd like to ask a question.|أود طرح سؤال.|التعلم والمشاركة|Adult learner politely raising a hand in a class
I'd like to try this jacket on.|أود تجربة هذه السترة.|التسوق|Customer asking a shop assistant to try on a jacket
I'd like to change my appointment.|أود تغيير موعدي.|تنظيم المواعيد|Person discussing a calendar appointment at a reception desk
I'd like to open a bank account.|أود فتح حساب مصرفي.|خدمة العملاء|Customer meeting a bank employee across a desk
I'd like to speak to the manager.|أود التحدث إلى المدير.|حل مشكلة|Customer calmly asking a receptionist for the manager
I'd like to learn how to cook.|أود تعلّم الطهو.|تعلّم مهارة|Adult joining a cooking class with a chef
I'd like to invite you to dinner.|أود دعوتك إلى العشاء.|دعوة اجتماعية|Friends discussing a dinner invitation in a warm home
I'd like to know more about this course.|أود معرفة المزيد عن هذه الدورة.|اختيار دورة|Student asking an adviser about a course brochure
I'd like to help with the project.|أود المساعدة في المشروع.|العمل الجماعي|Colleague volunteering help at a project planning table
I'd like to spend the weekend by the sea.|أود قضاء عطلة نهاية الأسبوع قرب البحر.|التخطيط للراحة|Person planning a seaside weekend with a small travel bag and sea view
"""),
4:('can','Can I + verb?','الاستئذان وطلب الخدمة',"""
Can I ask a question?|هل يمكنني طرح سؤال؟|داخل الصف|Adult learner raising a hand to ask a teacher a question
Can I sit here?|هل يمكنني الجلوس هنا؟|مقعد في مقهى|Customer asking another person before sitting at a cafe table
Can I pay by card?|هل يمكنني الدفع بالبطاقة؟|الدفع في متجر|Customer holding a bank card near a payment terminal
Can I borrow your pen?|هل يمكنني استعارة قلمك؟|استعارة غرض|Colleague politely asking to borrow a pen across a desk
Can I try these shoes on?|هل يمكنني تجربة هذا الحذاء؟|اختيار مقاس|Customer asking a shoe-shop assistant to try on shoes
Can I open the window?|هل يمكنني فتح النافذة؟|الراحة في المكتب|Office worker gesturing toward a closed window
Can I take a photo here?|هل يمكنني التقاط صورة هنا؟|زيارة متحف|Visitor holding a camera and asking a museum attendant permission
Can I use your phone for a moment?|هل يمكنني استخدام هاتفك للحظة؟|طلب مساعدة|Traveler asking a friend to use their phone briefly
Can I leave a message?|هل يمكنني ترك رسالة؟|الاتصال بالهاتف|Person speaking politely on a phone beside a notepad
Can I change my seat?|هل يمكنني تغيير مقعدي؟|السفر بالحافلة|Passenger asking a bus attendant about an empty seat
Can I bring a friend to the meeting?|هل يمكنني اصطحاب صديق إلى اللقاء؟|تنظيم لقاء|Person checking with a host about bringing a friend to a gathering
Can I get a glass of water, please?|هل يمكنني الحصول على كوب ماء، من فضلك؟|طلب مهذب|Guest politely requesting a glass of water from a host
"""),
5:('this','This is + noun','التعريف والإشارة',"""
This is my house.|هذا منزلي.|التعريف بالمنزل|Person proudly showing a friend their modest house
This is my friend.|هذا صديقي.|تقديم صديق|Person introducing a friend to another person
This is a good idea.|هذه فكرة جيدة.|مناقشة فكرة|Team smiling around a small creative project sketch
This is my new phone.|هذا هاتفي الجديد.|عرض غرض جديد|Person showing a new smartphone to a friend
This is our classroom.|هذا صفّنا الدراسي.|جولة في مدرسة|Teacher showing an adult learner a bright classroom
This is the bus to the city centre.|هذه الحافلة المتجهة إلى وسط المدينة.|التعرّف إلى الحافلة|Traveler pointing out a city bus at a station
This is my favourite book.|هذا كتابي المفضل.|الحديث عن كتاب|Person holding a treasured book and talking about it
This is the key to your room.|هذا مفتاح غرفتك.|استقبال الفندق|Hotel receptionist handing a room key to a guest
This is a difficult decision.|هذا قرار صعب.|اتخاذ قرار|Person thoughtfully comparing two options with a colleague
This is the first time I've been here.|هذه أول مرة آتي فيها إلى هنا.|زيارة مكان جديد|Visitor looking around an unfamiliar beautiful museum with a guide
This is what I was looking for.|هذا ما كنت أبحث عنه.|العثور على غرض|Relieved person finding a missing small notebook on a shelf
This is the person who helped me.|هذا الشخص الذي ساعدني.|تقدير المساعدة|Person introducing the helpful stranger who assisted them
"""),
6:('lets',"Let's + verb",'الاقتراح والتعاون',"""
Let's go to the park.|هيا نذهب إلى الحديقة.|اقتراح نزهة|Friends preparing to walk into a green park
Let's take a break.|هيا نأخذ استراحة.|الراحة من العمل|Colleagues standing up from their desks for a short break
Let's try again.|هيا نحاول مجددًا.|المثابرة|Two adults trying a small puzzle again after a failed attempt
Let's cook dinner together.|هيا نعدّ العشاء معًا.|التعاون في المنزل|Family members preparing dinner together in a kitchen
Let's check the map.|هيا نراجع الخريطة.|تحديد الاتجاه|Two travelers checking a paper city map together
Let's start with an easy question.|لنبدأ بسؤال سهل.|التعلم التدريجي|Teacher gently beginning an adult class discussion
Let's meet outside the library.|لنلتقِ خارج المكتبة.|ترتيب لقاء|Friends meeting by the entrance of a library
Let's save some money for the trip.|لندّخر بعض المال للرحلة.|التخطيط المالي|Couple putting savings into a travel jar beside a map
Let's ask someone for directions.|لنسأل أحدًا عن الطريق.|طلب الإرشاد|Travelers politely asking a local person for directions
Let's talk about what happened.|لنتحدث عما حدث.|فهم موقف|Two colleagues calmly discussing a minor mishap at a desk
Let's not make the same mistake again.|دعنا لا نكرر الخطأ نفسه.|التعلم من الخطأ|Team reviewing a corrected project plan thoughtfully
Let's find a solution that works for everyone.|لنجد حلًا يناسب الجميع.|التفاوض|Diverse colleagues working together on a shared solution
"""),
7:('feel','I feel like + verb-ing','التعبير عن الرغبة والمزاج',"""
I feel like going for a walk.|أشعر برغبة في التنزه.|وقت هادئ|Person putting on walking shoes by an open door
I feel like reading a book.|أشعر برغبة في قراءة كتاب.|القراءة|Person choosing a book from a shelf beside a cosy chair
I feel like staying home.|أشعر برغبة في البقاء في المنزل.|الراحة المنزلية|Person relaxing contentedly on a sofa at home
I feel like making some soup.|أشعر برغبة في إعداد بعض الحساء.|الطهو|Person preparing fresh vegetables for soup in a kitchen
I feel like calling an old friend.|أشعر برغبة في الاتصال بصديق قديم.|التواصل|Person smiling while phoning an old friend beside an old photograph
I feel like watching a film tonight.|أشعر برغبة في مشاهدة فيلم الليلة.|وقت الفراغ|Person settling in with a remote control for a movie evening
I feel like learning something new.|أشعر برغبة في تعلّم شيء جديد.|الفضول|Adult choosing a new craft activity at a workshop
I feel like taking a different route today.|أشعر برغبة في سلوك طريق مختلف اليوم.|تغيير الروتين|Walker considering a different path at a park junction
I feel like spending some time alone.|أشعر برغبة في قضاء بعض الوقت بمفردي.|مساحة شخصية|Person enjoying quiet reflection on a peaceful balcony
I feel like doing something creative.|أشعر برغبة في القيام بشيء إبداعي.|الإبداع|Person painting a simple canvas at a bright desk
I don't feel like going out in this rain.|لا أشعر برغبة في الخروج تحت هذا المطر.|التعبير عن عدم الرغبة|Person looking at heavy rain through a home window
Do you feel like joining us for lunch?|هل تود الانضمام إلينا على الغداء؟|دعوة طبيعية|Friends inviting another person to join their lunch table
"""),
8:('used','I used to + verb','العادات والحالات السابقة',"""
I used to live near the sea.|كنت أعيش بالقرب من البحر.|مكان سابق|Person looking thoughtfully at a former seaside home
I used to walk to school.|كنت أذهب إلى المدرسة مشيًا.|ذكريات المدرسة|Adult remembering a quiet walking path leading to a school
I used to play football.|كنت ألعب كرة القدم.|رياضة سابقة|Adult holding an old football beside a family photo album
I used to work in a small shop.|كنت أعمل في متجر صغير.|خبرة سابقة|Adult revisiting a small neighbourhood shop with its owner
I used to read before bed.|كنت أقرأ قبل النوم.|عادة قديمة|Person recalling bedtime reading with an old book and bedside lamp
I used to drink coffee every morning.|كنت أشرب القهوة كل صباح.|تغير عادة|Person looking at an old coffee cup while drinking water now
I used to visit my grandparents every week.|كنت أزور جدّي وجدّتي كل أسبوع.|ذكريات الأسرة|Adult looking through a family album with grandparents
We used to spend summers in the countryside.|كنا نقضي الصيف في الريف.|عطلة قديمة|Family looking at an old countryside holiday photograph
There used to be a bakery on this corner.|كان يوجد مخبز عند هذه الزاوية.|تغير المكان|Two neighbours pointing at a shop corner that has changed
Did you use to take this bus?|هل كنت تستقل هذه الحافلة سابقًا؟|سؤال عن الماضي|Two old friends discussing a familiar bus at a station
I didn't use to enjoy cooking.|لم أكن أستمتع بالطهو سابقًا.|تغير الاهتمام|Adult happily cooking while an old unused cookbook lies nearby
I'm used to getting up early now.|أنا معتاد الآن على الاستيقاظ مبكرًا.|مقارنة مهمة|Person calmly starting a sunrise morning routine beside an alarm clock
"""),
9:('managed','I managed to + verb','النجاح بعد جهد',"""
I managed to finish on time.|تمكنت من الانتهاء في الوقت المحدد.|إنجاز موعد نهائي|Relieved worker finishing a report just before a deadline
I managed to find my keys.|تمكنت من العثور على مفاتيحي.|حل مشكلة يومية|Person happily finding keys under a sofa cushion
I managed to solve the problem.|تمكنت من حل المشكلة.|التفكير|Learner smiling after solving a difficult puzzle
I managed to catch the last train.|تمكنت من اللحاق بآخر قطار.|السفر|Relieved traveler boarding the last train at dusk
I managed to repair the chair.|تمكنت من إصلاح الكرسي.|مهارة عملية|Person proudly testing a chair they repaired with tools nearby
I managed to save enough money.|تمكنت من ادخار ما يكفي من المال.|تحقيق هدف|Person counting carefully saved money beside a savings jar
We managed to reach the village before dark.|تمكّنا من الوصول إلى القرية قبل الظلام.|الوصول بعد مشقة|Travelers reaching a village as evening light fades
She managed to explain the idea clearly.|تمكنت من شرح الفكرة بوضوح.|التواصل|Woman explaining a project sketch to attentive colleagues
They managed to organise the event in one week.|تمكنوا من تنظيم الفعالية في أسبوع واحد.|العمل الجماعي|Team celebrating a successfully prepared community event
Did you manage to speak to the doctor?|هل تمكنت من التحدث إلى الطبيب؟|سؤال عن إنجاز|Friend asking another person about a completed doctor visit
I didn't manage to book a ticket.|لم أتمكن من حجز تذكرة.|عدم النجاح|Traveler disappointed at an unavailable ticket booking screen
We tried to fix it, but we didn't manage to.|حاولنا إصلاحه، لكننا لم نتمكن من ذلك.|مقارنة المحاولة والإنجاز|Two adults beside a bicycle they could not fully repair
"""),
10:('takes','It takes + time + to + verb','الوقت والجهد',"""
It takes ten minutes to get there.|يستغرق الوصول إلى هناك عشر دقائق.|رحلة قصيرة|Person checking a short route on a map beside a clock
It takes time to learn a language.|يستغرق تعلّم لغة وقتًا.|التعلم المستمر|Adult studying language notebooks across a calendar of practice
It takes an hour to cook dinner.|يستغرق إعداد العشاء ساعة.|إعداد الطعام|Person cooking dinner with a kitchen timer nearby
It takes me twenty minutes to walk to work.|يستغرق ذهابي إلى العمل مشيًا عشرين دقيقة.|التنقل اليومي|Office worker walking toward work with a watch visible
It takes two people to move this table.|يتطلب نقل هذه الطاولة شخصين.|التعاون|Two adults safely carrying a table together
It takes patience to teach a child.|يتطلب تعليم طفل صبرًا.|التعليم|Patient parent helping a child learn a simple task
How long does it take to charge this battery?|كم يستغرق شحن هذه البطارية؟|سؤال عن المدة|Person asking a technician about a charging battery
It took us three hours to finish the job.|استغرق إنجاز العمل منا ثلاث ساعات.|مدة في الماضي|Team looking satisfied at a completed repair job and clock
It will take a few days to repair the car.|سيستغرق إصلاح السيارة بضعة أيام.|مدة متوقعة|Mechanic explaining a repair timeline to a car owner
It doesn't take long to make this meal.|لا يستغرق إعداد هذه الوجبة وقتًا طويلًا.|وجبة سريعة|Person preparing a simple quick salad in a kitchen
It took longer than I expected to find the address.|استغرق العثور على العنوان وقتًا أطول مما توقعت.|تجربة بحث|Traveler finally locating an address after checking a map
Learning this skill takes practice.|يتطلب تعلّم هذه المهارة ممارسة.|صياغة بديلة|Adult practising a new craft skill repeatedly at a workbench
"""),
11:('worth',"It's worth + verb-ing",'القيمة والاختيارات',"""
It's worth trying again.|الأمر يستحق المحاولة مرة أخرى.|المثابرة|Person making another thoughtful attempt at a challenging puzzle
It's worth visiting the museum.|المتحف يستحق الزيارة.|زيارة مفيدة|Visitors admiring a beautiful museum exhibit
It's worth thinking about.|الأمر يستحق التفكير فيه.|تقييم فكرة|Person considering a useful idea with a notebook
It's worth checking the details.|الأمر يستحق التحقق من التفاصيل.|التحقق|Colleague carefully reviewing a document with a magnifier
It's worth learning a few local words.|من المفيد تعلّم بضع كلمات محلية.|الاستعداد للسفر|Traveler learning phrases from a local person before a trip
It's worth spending time with your family.|قضاء الوقت مع أسرتك يستحق الاهتمام.|العلاقات|Family enjoying a warm shared afternoon activity
It's worth asking for a second opinion.|الأمر يستحق طلب رأي ثانٍ.|اتخاذ قرار|Person consulting a second knowledgeable adviser
It's worth booking in advance.|الحجز مسبقًا أمر يستحق العناء.|التخطيط|Traveler booking a future trip calmly with a calendar
Is it worth taking a taxi?|هل يستحق الأمر استئجار سيارة أجرة؟|مقارنة وسائل النقل|Traveler weighing a taxi against a nearby bus at a station
It isn't worth arguing about.|الأمر لا يستحق الجدال حوله.|تهدئة خلاف|Friends calmly putting aside a small disagreement
This book is worth reading twice.|هذا الكتاب يستحق أن يُقرأ مرتين.|توسيع الصيغة|Person returning enthusiastically to a well-loved book
The view was well worth the long walk.|كان المنظر يستحق عناء المشي الطويل.|قيمة التجربة|Hikers enjoying a stunning view after a long walk
"""),
12:('know','Do you know where + subject + verb?','الأسئلة غير المباشرة',"""
Do you know where the station is?|هل تعرف أين تقع المحطة؟|طلب اتجاه|Traveler asking a local person about the railway station
Do you know where she works?|هل تعرف أين تعمل؟|معرفة مكان عمل|Colleagues discussing where a woman works in an office building
Do you know where I can buy a ticket?|هل تعرف أين يمكنني شراء تذكرة؟|شراء تذكرة|Traveler asking an attendant where to purchase a ticket
Do you know where my keys are?|هل تعرف أين مفاتيحي؟|البحث في المنزل|Person asking a family member about missing keys at home
Do you know where the meeting will be?|هل تعرف أين سيكون الاجتماع؟|تنظيم عمل|Coworkers looking for a meeting room in an office corridor
Do you know when the shop closes?|هل تعرف متى يغلق المتجر؟|سؤال عن الوقت|Customer asking another person about a shop closing time
Do you know how much this costs?|هل تعرف كم يبلغ ثمن هذا؟|سؤال عن السعر|Shopper asking a shop assistant about the price of an item
Do you know why the bus is late?|هل تعرف لماذا تأخرت الحافلة؟|سؤال عن السبب|Passengers discussing a delayed bus at a stop
Do you know if the library is open?|هل تعرف إن كانت المكتبة مفتوحة؟|سؤال بنعم أو لا|Visitor asking a person outside a library about opening
Could you tell me where the nearest pharmacy is?|هل يمكنك إخباري أين تقع أقرب صيدلية؟|طلب أكثر تهذيبًا|Traveler politely asking a local person for the nearest pharmacy
I don't know where he went.|لا أعرف أين ذهب.|سؤال مضمن في خبر|Person shrugging gently when asked where a colleague went
Do you know what happened?|هل تعرف ما الذي حدث؟|سؤال تكون أداته فاعلًا|Two people calmly discussing a minor unexpected bicycle mishap
""")}
LEVELS=['فهم النمط','توسيع النمط','المقارنة في موقف','الاستخدام الحقيقي','الترابط والتوسّع','الاسترجاع والطلاقة']
p=ROOT/'dist/pilot.json';d=json.loads(p.read_text());old={s['id']:s for s in d['sentences']};old_patterns={p['id']:p for p in d['patterns']}
for pid,(key,form,title,block) in BLOCKS.items():
 rows=[line.split('|') for line in block.strip().splitlines()];assert len(rows)==12
 ids=[]
 for i,(en,ar,context,scene) in enumerate(rows):
  sid=f'{key}-{i+1:02d}';ids.append(sid)
  if sid in old:
   assert old[sid]['en']==en;continue
  item={'id':sid,'pattern_id':pid,'group_id':'g02' if pid<=6 else 'g03' if pid<=9 else 'g04','en':en,'ar':ar,'context':context,'scene_description':scene,'image':{'id':'scene-'+sid,'atlas':f'assets/scenes/{key}-atlas.webp','cell':i,'columns':3,'rows':4,'status':'pending_visual_review','origin':'generated_photorealistic'},'difficulty':{'cefr':('A1' if pid<=6 else 'A2' if pid<=10 else 'B1') if i<9 else ('A2' if pid<=6 else 'B1'),'stage':i//2+1,'stage_label':LEVELS[i//2]},'related_pattern_ids':{'like':[1,13,2,4],'can':[3,12],'this':[12],'lets':[4,3],'feel':[1,3],'used':[10,9],'managed':[8,2],'takes':[2,9],'worth':[1,10],'know':[4,3]}[key],'vocabulary':[w.lower().strip('.,?!') for w in en.split() if len(w.strip('.,?!'))>3],'exercise_ids':[sid+'-transfer'],'recordings':{v:{'voice_id':voice,'path':f'assets/audio/{sid}-{v}.mp3','status':'pending','words':[]}for v,voice in [('male','am_adam'),('female','af_bella')]}}
  d['sentences'].append(item)
 if pid not in old_patterns:d['patterns'].append({'id':pid,'key':key,'form':form,'title':title,'sentence_ids':ids,'group_id':item['group_id'],'level':'A1–B1','comparison':{'ar':'لاحظ تركيب النمط، وراجع الشرح المقارن في الدرس.','en':form},'transfer':{'prompt':'استخدم النمط للتعبير عن فكرة جديدة في موقف من حياتك، دون نسخ مثال.','unseen':True}})
d['pattern_order']=[1,13,2,3,4,5,6,7,8,9,10,11,12];d['patterns'].sort(key=lambda p:d['pattern_order'].index(p['id']));d['sentences'].sort(key=lambda s:(d['pattern_order'].index(s['pattern_id']),int(s['id'].split('-')[-1])))
d['groups']=[{'id':'g01','title':'الرغبة والحاجة والالتزام'},{'id':'g02','title':'تواصل كل يوم'},{'id':'g03','title':'المشاعر والتجارب'},{'id':'g04','title':'أفكار مترابطة'}];d['title']='منهج نسق: 13 نمطًا، 12 جملة لكل نمط';d['revision']='full-media-exams-20261102'
p.write_text(json.dumps(d,ensure_ascii=False,indent=2));print(len(d['patterns']),'patterns',len(d['sentences']),'sentences')
