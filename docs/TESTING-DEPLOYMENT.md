# اختبار التطبيق ونشره — GitHub Actions / Pages

## نسخة الاختبار المتاحة الآن

المشروع مخزن في \`saddamalkhatabi/Learn-English\`، والملفات الصوتية من تشغيل Kokoro الأول موجودة على الفرع \`main\`.

رابط تشغيل GitHub Actions الذي **نجح** في فحص التطبيق وتوليد 15 تسجيل MP3 وإنشاء حزمة الاختبار:
https://github.com/saddamalkhatabi/Learn-English/actions/runs/41244514987

افتح الرابط بعد تسجيل الدخول إلى GitHub، ثم نزّل Artifact المسمّى \`learn-english-preview-with-audio\` من قسم Artifacts.

لفتح الملف محليًا بشكل صحيح، فك ضغط الحزمة في مجلد، ثم من ذلك المجلد شغّل:

\`\`\`powershell
py -m http.server 8000
\`\`\`

ثم افتح: http://localhost:8000/

لا تفتح \`index.html\` مباشرة بصيغة \`file://\`؛ لأن المتصفح سيمنع طلبات JSON من الملفات المجاورة في بعض المتصفحات.

## تفعيل موقع مباشر عبر GitHub Pages

حاليًا كشف GitHub Action أن Pages لم تُفعَّل بعد للمستودع؛ سجل التشغيل يظهر الخطأ \`Get Pages site failed ... Not Found\`. لذلك لا يوجد رابط موقع مباشر مؤكد حتى تفعيل الخدمة.

خطوات التفعيل (مرة واحدة إن كانت الخطة تدعمه):
1. افتح المستودع على GitHub.
2. ادخل إلى **Settings → Pages**.
3. في **Build and deployment** اختر **Source = GitHub Actions**.
4. افتح **Actions → Learn English — Preview, Kokoro Audio & Pages** وأعد تشغيل Workflow عبر زر **Run workflow**؛ أو ادفع تعديلًا جديدًا إلى main.
5. عند نجاح خطوة **Deploy GitHub Pages preview**، يظهر عنوان الموقع في ملخص التشغيل.

**ملاحظة مهمة:** بالنسبة للمستودعات الخاصة، GitHub Pages يتطلب خطة GitHub تدعم Pages للمستودعات الخاصة (مثل GitHub Pro أو Team). مع GitHub Free تكون Pages متاحة للمستودعات العامة، ولكن لا تغيّر خصوصية المستودع لمجرد تشغيل تجربة دون موافقة مالكه.

## مراجعة الأصوات

- \`assets/audio/this/intro.mp3\`
- \`assets/audio/have/intro.mp3\`
- \`assets/audio/got/intro.mp3\`
- أربع جمل أساسية لكل درس بالاسم \`scene-1-1.mp3\` ... \`scene-1-4.mp3\`

المجموع الحالي: **15 ملف MP3 مسجلًا من Kokoro**.

لتوليد أصوات جميع المستويات: تشغيل Workflow يدويًا وتفعيل خيار \`full_voice_library\`. يولّد عندها أصوات جميع مشاهد التجربة (39 ملفًا شاملًا 3 شروح) ثم يحفظ الأصول على main عند نجاح رفع الملفات.

## إخفاق الصوت والنشر

- خطأ في تثبيت أو توليد Kokoro: تبقى نسخة HTML قابلة للاختبار، ويستخدم التطبيق صوت المتصفح بديلًا مؤقتًا؛ تحقق من رسالة المصدر في شاشة الدرس.
- Pages غير مفعلة: يبقى Artifact قابلًا للتنزيل، وليس رابط استضافة عامة.
- يجب اختبار الملف MP3 بالعقل البشري قبل اعتماده كمادة نهائية: الوقفات، النبر، contractions، والتطابق اللفظي.
- قد تتكرر تشغيلات Actions بعد تعديل الكود؛ عندما تكون ملفات Kokoro الجاهزة موجودة، يتجاوز Workflow توليدها مرة أخرى لتوفير الموارد.

مرجع إعداد GitHub Pages: https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site
