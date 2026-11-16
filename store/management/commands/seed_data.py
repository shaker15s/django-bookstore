"""
Management command to seed the database with rich, realistic data.
Creates categories, authors, products (books), and sliders.
"""
from django.core.management.base import BaseCommand
from store.models import category, Author, product, slider


class Command(BaseCommand):
    help = 'Seeds the database with categories, authors, books, and sliders'

    def handle(self, *args, **options):
        self.stdout.write('Clearing old data...')
        product.objects.all().delete()
        slider.objects.all().delete()
        Author.objects.all().delete()
        category.objects.all().delete()

        self.stdout.write('Creating categories...')
        cats = {}
        cat_data = [
            ('تطوير الويب', True, 1),
            ('بايثون', True, 2),
            ('الذكاء الاصطناعي', True, 3),
            ('قواعد البيانات', False, 4),
            ('أمن المعلومات', False, 5),
            ('تطوير الموبايل', False, 6),
            ('علم البيانات', False, 7),
        ]
        for name, featured, order_num in cat_data:
            cats[name] = category.objects.create(
                name=name, featured=featured, order=order_num
            )

        self.stdout.write('Creating authors...')
        authors = {}
        author_data = [
            (
                'أحمد ناصر',
                'مهندس برمجيات ومؤلف متخصص في تطوير تطبيقات الويب '
                'باستخدام Django و React. يعمل في مجال البرمجة منذ '
                'أكثر من 10 سنوات ودرّب مئات المبرمجين.',
            ),
            (
                'سارة الحسيني',
                'باحثة في الذكاء الاصطناعي وتعلم الآلة، حاصلة على '
                'ماجستير من جامعة القاهرة. مؤلفة لعدة كتب تقنية '
                'مترجمة إلى 5 لغات.',
            ),
            (
                'محمد العتيبي',
                'خبير أمن معلومات ومستشار تقني. عمل في شركات تقنية '
                'كبرى مثل Microsoft و IBM. متخصص في اختبار الاختراق '
                'والحماية السيبرانية.',
            ),
            (
                'ياسمين فؤاد',
                'مطورة تطبيقات موبايل ومبرمجة Full Stack. ساهمت في '
                'بناء أكثر من 30 تطبيق ناجح على متجري Google Play '
                'و App Store.',
            ),
            (
                'عمر خالد',
                'محلل بيانات ومتخصص في علم البيانات والإحصاء '
                'التطبيقي. يقدم دورات تدريبية متقدمة في تحليل '
                'البيانات باستخدام Python و R.',
            ),
            (
                'Shaker Abdallah',
                'مبرمج ومطور مواقع ويب. شغوف بتقنيات الويب الحديثة '
                'و Django و Python. يسعى لبناء تجارب رقمية مميزة.',
            ),
        ]
        for name, bio in author_data:
            authors[name] = Author.objects.create(name=name, bio=bio)

        self.stdout.write('Creating books...')
        books_data = [
            # ── تطوير الويب ──
            {
                'name': 'احتراف Django من الصفر إلى الاحتراف',
                'short_description': (
                    'دليل شامل لبناء تطبيقات ويب قوية وآمنة '
                    'باستخدام إطار عمل Django مع مشاريع عملية.'
                ),
                'description': (
                    'يغطي هذا الكتاب كل ما تحتاجه لتصبح محترفاً '
                    'في Django بدءاً من الأساسيات وحتى المواضيع '
                    'المتقدمة مثل REST APIs، المصادقة، النشر على '
                    'السحابة، وأنماط التصميم المعمارية. يتضمن ٨ '
                    'مشاريع عملية كاملة مع شرح مفصل لكل خطوة.'
                ),
                'price': 29.99,
                'featured': True,
                'stock': 50,
                'category': cats['تطوير الويب'],
                'author': authors['Shaker Abdallah'],
            },
            {
                'name': 'تعلم HTML5 و CSS3 الحديث',
                'short_description': (
                    'أساسيات بناء صفحات ويب تفاعلية وجذابة باستخدام '
                    'أحدث تقنيات HTML و CSS.'
                ),
                'description': (
                    'كتاب عملي يشرح بالتفصيل كيفية بناء مواقع ويب '
                    'متجاوبة مع جميع الشاشات، مع التركيز على '
                    'Flexbox, Grid, Animations وأحدث ممارسات '
                    'التصميم في 2024. يتضمن 15 تمريناً عملياً.'
                ),
                'price': 19.99,
                'featured': True,
                'stock': 75,
                'category': cats['تطوير الويب'],
                'author': authors['أحمد ناصر'],
            },
            {
                'name': 'JavaScript المتقدم: أنماط ومعمارية',
                'short_description': (
                    'تعمق في JavaScript مع أنماط التصميم، '
                    'البرمجة الوظيفية، و Async/Await.'
                ),
                'description': (
                    'هذا الكتاب لمن يريد الانتقال من مستوى '
                    'مبتدئ/متوسط إلى مستوى متقدم في JavaScript. '
                    'يشمل الأنماط التصميمية، إدارة الحالة، '
                    'التعامل مع APIs، الاختبارات الآلية، وبناء '
                    'مكتبات قابلة لإعادة الاستخدام.'
                ),
                'price': 34.99,
                'featured': False,
                'stock': 30,
                'category': cats['تطوير الويب'],
                'author': authors['أحمد ناصر'],
            },
            # ── بايثون ──
            {
                'name': 'البرمجة بلغة بايثون للمبتدئين',
                'short_description': (
                    'أفضل نقطة بداية لتعلم البرمجة بلغة Python '
                    'من الصفر مع أمثلة تفاعلية.'
                ),
                'description': (
                    'يبدأ هذا الكتاب من أبسط المفاهيم مثل '
                    'المتغيرات والحلقات وصولاً إلى البرمجة '
                    'الكائنية والتعامل مع الملفات وقواعد '
                    'البيانات. مصمم خصيصاً للمبتدئين الذين ليس '
                    'لديهم أي خلفية برمجية سابقة.'
                ),
                'price': 14.99,
                'featured': True,
                'stock': 100,
                'category': cats['بايثون'],
                'author': authors['Shaker Abdallah'],
            },
            {
                'name': 'أتمتة المهام المملة عبر بايثون',
                'short_description': (
                    'وفّر ساعات من العمل اليدوي بأتمتة المهام '
                    'الروتينية باستخدام سكربتات Python.'
                ),
                'description': (
                    'تعلم كيف تكتب سكربتات Python لأتمتة مهام '
                    'مثل التعامل مع Excel، إرسال الإيميلات، '
                    'web scraping، التعامل مع الملفات، والمزيد. '
                    'كل فصل يركز على مشروع عملي مستقل.'
                ),
                'price': 24.99,
                'featured': True,
                'stock': 60,
                'category': cats['بايثون'],
                'author': authors['عمر خالد'],
            },
            {
                'name': 'هياكل البيانات والخوارزميات ببايثون',
                'short_description': (
                    'إتقان هياكل البيانات والخوارزميات اللازمة '
                    'لاجتياز مقابلات العمل البرمجية.'
                ),
                'description': (
                    'يشمل الكتاب شرحاً تفصيلياً لـ Arrays, '
                    'Linked Lists, Trees, Graphs, Dynamic '
                    'Programming, Sorting والبحث. مع أكثر من '
                    '150 تمرين محلول من مقابلات Google و Meta.'
                ),
                'price': 39.99,
                'featured': False,
                'stock': 25,
                'category': cats['بايثون'],
                'author': authors['أحمد ناصر'],
            },
            # ── الذكاء الاصطناعي ──
            {
                'name': 'مقدمة في تعلم الآلة والذكاء الاصطناعي',
                'short_description': (
                    'فهم أساسيات الـ Machine Learning و Deep '
                    'Learning مع تطبيقات عملية بـ Python.'
                ),
                'description': (
                    'يقدم هذا الكتاب نظرة شاملة عن عالم الذكاء '
                    'الاصطناعي من المفاهيم الرياضية الأساسية '
                    'وحتى بناء نماذج عملية باستخدام TensorFlow '
                    'و PyTorch. يتضمن مشاريع في التعرف على '
                    'الصور، معالجة اللغة الطبيعية، والروبوتات.'
                ),
                'price': 44.99,
                'featured': True,
                'stock': 40,
                'category': cats['الذكاء الاصطناعي'],
                'author': authors['سارة الحسيني'],
            },
            {
                'name': 'معالجة اللغة الطبيعية العربية (NLP)',
                'short_description': (
                    'أول كتاب عربي متخصص في معالجة النصوص '
                    'العربية باستخدام تقنيات NLP الحديثة.'
                ),
                'description': (
                    'يتناول هذا الكتاب تحديات وحلول معالجة '
                    'اللغة العربية الطبيعية من التشكيل والتصريف '
                    'وحتى بناء Chatbots ذكية، تحليل المشاعر، '
                    'والترجمة الآلية. مع أمثلة عملية بمكتبات '
                    'CAMeL Tools و AraBERT.'
                ),
                'price': 49.99,
                'featured': False,
                'stock': 15,
                'category': cats['الذكاء الاصطناعي'],
                'author': authors['سارة الحسيني'],
            },
            # ── قواعد البيانات ──
            {
                'name': 'إتقان SQL و PostgreSQL',
                'short_description': (
                    'دليل عملي لتعلم SQL من الصفر وإتقان '
                    'PostgreSQL لإدارة قواعد بيانات ضخمة.'
                ),
                'description': (
                    'من SELECT البسيطة إلى الاستعلامات المعقدة '
                    'والـ Window Functions والأداء والفهرسة '
                    'والنسخ الاحتياطي. يتضمن تمارين عملية على '
                    'قواعد بيانات حقيقية وسيناريوهات من الواقع.'
                ),
                'price': 27.99,
                'featured': False,
                'stock': 45,
                'category': cats['قواعد البيانات'],
                'author': authors['عمر خالد'],
            },
            {
                'name': 'MongoDB للمحترفين',
                'short_description': (
                    'تعلم قواعد البيانات غير العلائقية NoSQL '
                    'باستخدام MongoDB مع Node.js.'
                ),
                'description': (
                    'كتاب متقدم يغطي تصميم المخططات، '
                    'Aggregation Pipeline، الفهرسة المتقدمة، '
                    'Sharding، Replication، وأفضل الممارسات '
                    'لبناء تطبيقات عالية الأداء مع MongoDB Atlas.'
                ),
                'price': 32.99,
                'featured': False,
                'stock': 20,
                'category': cats['قواعد البيانات'],
                'author': authors['أحمد ناصر'],
            },
            # ── أمن المعلومات ──
            {
                'name': 'اختبار الاختراق الأخلاقي',
                'short_description': (
                    'تعلم كيف تفكر كهاكر أخلاقي وتحمي الأنظمة '
                    'من الاختراقات والثغرات الأمنية.'
                ),
                'description': (
                    'يشمل هذا الكتاب أساسيات أمن الشبكات، '
                    'اختبار الاختراق باستخدام Kali Linux، '
                    'استغلال الثغرات، الهندسة الاجتماعية، '
                    'وحماية تطبيقات الويب من OWASP Top 10. '
                    'مع مختبرات عملية قابلة للتطبيق فوراً.'
                ),
                'price': 37.99,
                'featured': True,
                'stock': 35,
                'category': cats['أمن المعلومات'],
                'author': authors['محمد العتيبي'],
            },
            {
                'name': 'التشفير وأمن البيانات',
                'short_description': (
                    'فهم خوارزميات التشفير وتأمين البيانات '
                    'الحساسة في التطبيقات الحديثة.'
                ),
                'description': (
                    'من التشفير المتماثل إلى RSA و AES '
                    'والتوقيعات الرقمية وبروتوكولات SSL/TLS. '
                    'يقدم أمثلة عملية بلغة Python لتطبيق '
                    'التشفير في مشاريعك الحقيقية.'
                ),
                'price': 29.99,
                'featured': False,
                'stock': 28,
                'category': cats['أمن المعلومات'],
                'author': authors['محمد العتيبي'],
            },
            # ── تطوير الموبايل ──
            {
                'name': 'تطبيقات Flutter من الصفر',
                'short_description': (
                    'بناء تطبيقات Android و iOS بكود واحد '
                    'باستخدام Flutter و Dart.'
                ),
                'description': (
                    'يبدأ من تثبيت البيئة وأساسيات Dart ثم '
                    'يتعمق في Widgets، إدارة الحالة مع '
                    'Provider و Riverpod، التعامل مع APIs، '
                    'Firebase، والنشر على المتاجر. يتضمن 5 '
                    'تطبيقات كاملة جاهزة للنشر.'
                ),
                'price': 34.99,
                'featured': True,
                'stock': 55,
                'category': cats['تطوير الموبايل'],
                'author': authors['ياسمين فؤاد'],
            },
            {
                'name': 'React Native: تطبيقات الجوال العصرية',
                'short_description': (
                    'استخدم خبرتك في React لبناء تطبيقات '
                    'جوال أصلية عالية الأداء.'
                ),
                'description': (
                    'كتاب عملي يركز على بناء تطبيقات حقيقية '
                    'باستخدام React Native مع التنقل، '
                    'التخزين المحلي، الإشعارات، الخرائط، '
                    'والكاميرا. مناسب لمطوري الويب الراغبين '
                    'في دخول عالم الموبايل.'
                ),
                'price': 31.99,
                'featured': False,
                'stock': 38,
                'category': cats['تطوير الموبايل'],
                'author': authors['ياسمين فؤاد'],
            },
            # ── علم البيانات ──
            {
                'name': 'تحليل البيانات باستخدام Pandas',
                'short_description': (
                    'إتقان مكتبة Pandas لتحليل ومعالجة '
                    'البيانات بكفاءة واحترافية.'
                ),
                'description': (
                    'يغطي الكتاب كل ما تحتاجه من DataFrame '
                    'operations، التنظيف، التحويل، التجميع، '
                    'والتصور البياني مع Matplotlib و Seaborn. '
                    'يتضمن 10 مشاريع تحليل بيانات حقيقية.'
                ),
                'price': 26.99,
                'featured': False,
                'stock': 42,
                'category': cats['علم البيانات'],
                'author': authors['عمر خالد'],
            },
            {
                'name': 'التصور البياني للبيانات مع Python',
                'short_description': (
                    'تحويل البيانات الجافة إلى قصص بصرية '
                    'مؤثرة باستخدام أدوات Python.'
                ),
                'description': (
                    'تعلم إنشاء رسومات بيانية تفاعلية '
                    'واحترافية باستخدام Matplotlib، Seaborn، '
                    'Plotly، و Bokeh. يركز على أفضل ممارسات '
                    'تصميم المخططات ورواية القصص بالبيانات.'
                ),
                'price': 22.99,
                'featured': False,
                'stock': 33,
                'category': cats['علم البيانات'],
                'author': authors['عمر خالد'],
            },
        ]

        for book_data in books_data:
            product.objects.create(**book_data)

        self.stdout.write('Creating sliders...')
        sliders_data = [
            {
                'title': 'اكتشف عالم البرمجة',
                'subtitle': (
                    'مكتبة شاملة من الكتب التقنية العربية '
                    'لتعلم البرمجة من الصفر حتى الاحتراف. '
                    'ابدأ رحلتك اليوم!'
                ),
                'order': 1,
            },
            {
                'title': 'كتب جديدة كل أسبوع',
                'subtitle': (
                    'نضيف كتباً حصرية ومحدثة باستمرار في '
                    'مجالات الذكاء الاصطناعي، تطوير الويب، '
                    'أمن المعلومات والمزيد.'
                ),
                'order': 2,
            },
            {
                'title': 'تعلّم من الخبراء',
                'subtitle': (
                    'كتب مؤلفة من مهندسين وباحثين عرب '
                    'يعملون في أكبر شركات التقنية العالمية. '
                    'محتوى عملي وتطبيقي ١٠٠٪'
                ),
                'order': 3,
            },
        ]
        for sl_data in sliders_data:
            slider.objects.create(**sl_data)

        total_books = product.objects.count()
        total_cats = category.objects.count()
        total_authors = Author.objects.count()
        total_sliders = slider.objects.count()

        self.stdout.write(self.style.SUCCESS(
            f'Done! Created {total_cats} categories, '
            f'{total_authors} authors, {total_books} books, '
            f'{total_sliders} sliders.'
        ))
