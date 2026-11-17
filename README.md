# 📚 متجر كتب - Django Bookstore & E-Commerce

متجر إلكتروني متكامل ومتطور مبني باستخدام إطار العمل **Django**، مخصص لبيع الكتب والدورات التقنية مع دعم الدفع الإلكتروني عبر **Stripe**، وسلة مشتريات تفاعلية، ولوحة تحكم متطورة، وتصميم متجاوب بالكامل.

🌐 **الرابط المباشر (Live Demo):** [https://django-bookstore-teal.vercel.app/](https://django-bookstore-teal.vercel.app/)

---

## ✨ المميزات الرئيسية (Features)

- 🛍️ **سلة تسوق تفاعلية**: إمكانية زيادة وإنقاص وحذف الكميات مباشرة وسلاسة مزامنة الجلسات (Sessions).
- 💳 **بوابة دفع Stripe**: دعم كامل لـ Stripe Checkout (بطاقات الائتمان، الفيزا، الماستركارد) مع معالجة وضع الاختبار (Sandbox Test Mode).
- 🚚 **خيارات دفع متعددة**: دعم الدفع الإلكتروني أو الدفع عند الاستلام (Cash on Delivery).
- 🏷️ **تصنيفات ومؤلفون**: تصفية المنتجات حسب الأقسام والمؤلفين والبحث المتقدم بالاسم والوصف.
- ✉️ **إشعارات بريد إلكتروني تفاعلية**: إرسال إيصال وتفاصيل الطلب تلقائياً بتصميم HTML متجاوب.
- 🛡️ **لوحة تحكم احترافية**: إدارة شاملة للطلبات والمنتجات والأقسام والشرائح مع دعم `Inlines` وفلاتر ذكية.
- 🧪 **مجموعة اختبارات مؤتمتة (Unit & Integration Tests)**: تغطية شاملة للمسارات، النماذج، سلة المشتريات، والتحقق من النماذج.
- 🔒 **حماية وأمان**: فصل الإعدادات والمفاتيح السرية باستخدام متغيرات البيئة (`.env`).
- ⚡ **جاهز للنشر السحابي (Serverless Ready)**: مهيأ بالكامل للعمل على Vercel و WhiteNoise و SQLite/PostgreSQL.

---

## 🛠️ متطلبات التشغيل (Tech Stack)

- **Python** 3.11+ / 3.12+
- **Django** 6.x
- **Pillow** (لمعالجة الصور)
- **WhiteNoise** (لتقديم الملفات الثابتة)
- **Stripe** (لبوابة الدفع)
- **python-dotenv** (لإدارة المفاتيح السرية)

---

## 🚀 التثبيت والتشغيل المحلي (Local Setup)

1. **استنساخ المستودع (Clone the repository):**
   ```bash
   git clone https://github.com/shaker15s/django-bookstore.git
   cd django-bookstore
   ```

2. **إنشاء بيئة افتراضية وتفعيلها:**
   ```bash
   python -m venv .venv
   # على Windows:
   .venv\Scripts\activate
   # على Linux/Mac:
   source .venv/bin/activate
   ```

3. **تثبيت الحزم المطلوبة:**
   ```bash
   pip install -r requirements.txt
   ```

4. **إعداد ملف البيئة `.env`:**
   قم بنسخ ملف `.env.example` إلى `.env`:
   ```bash
   copy .env.example .env
   ```
   ثم أضف مفاتيح Stripe الخاصة بك (يمكنك استخدام مفاتيح الاختبار المجانية من [Stripe Dashboard](https://dashboard.stripe.com/test/apikeys)).

5. **تطبيق قواعد البيانات وتوليد البيانات الأولية:**
   ```bash
   python manage.py migrate
   python manage.py seed_data   # اختياري لتوليد كتب وتصنيفات تجريبية
   ```

6. **تشغيل السيرفر:**
   ```bash
   python manage.py runserver
   ```
   افتح المتصفح على: `http://127.0.0.1:8000/`

7. **تشغيل الاختبارات المؤتمتة (Run Tests):**
   ```bash
   python manage.py test store
   ```
   يحتوي المشروع على اختبارات تغطي:
   - صحة تمثيل النماذج (`__str__` والعلاقات)
   - استجابة الصفحات والتوجيهات (`200 OK`, `404 Not Found`)
   - عمليات السلة الكاملة (إضافة، تعديل، حذف، وتفريغ)
   - التحقق من بيانات الدفع (Validation) والدفع عند الاستلام وبوابة Stripe.

---

## ☁️ النشر على منصة Vercel (Deployment)

تم تهيئة المشروع بملف `vercel.json` ليعمل كـ Serverless Application باستخدام WSGI:
- يتم تقديم الملفات الثابتة عبر **WhiteNoise** بسرعة فائقة.
- تدعم إعدادات قاعدة البيانات بيئة القراءة فقط (Read-only Serverless) عبر توجيه SQLite إلى المجلد التلقائي المؤقت `/tmp/db.sqlite3`.
- يمكن ربطه بأي قاعدة بيانات PostgreSQL خارجية (مثل Supabase أو Neon) بمجرد تمرير متغير `DATABASE_URL`.

---

## 💳 إعداد بوابة Stripe المجانية (Test Mode)

1. سجل حساباً مجانياً على [Stripe](https://stripe.com).
2. فعّل وضع **Test Mode** من الشريط العلوي.
3. انسخ المفاتيح التجريبية من **Developers -> API keys**:
   - `STRIPE_PUBLISHABLE_KEY`: يبدأ بـ `pk_test_...`
   - `STRIPE_SECRET_KEY`: يبدأ بـ `sk_test_...`
4. ضع المفاتيح في ملف `.env`.
5. لتجربة الشراء، استخدم بطاقات الاختبار الرسمية من Stripe:
   - رقم البطاقة: `4242 4242 4242 4242`
   - تاريخ الانتهاء: أي تاريخ مستقبلي (مثلاً `12/28`)
   - CVC: أي 3 أرقام (مثلاً `123`)

---

## 📄 الترخيص (License)
هذا المشروع مفتوح المصدر ومتاح للاستخدام والتطوير.
