import os
import shutil
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_ecommerse.settings')
django.setup()

from store.models import slider, product

artifact_dir = r'C:\Users\HP\.gemini\antigravity\brain\8a7d3b6e-c7bc-482f-8a2f-7b894cdb687a'

# Background sliders
s1 = os.path.join(artifact_dir, 'slider_code_bg_1775539629389.png')
s2 = os.path.join(artifact_dir, 'slider_learning_1775539645376.png')
s3 = os.path.join(artifact_dir, 'slider_expert_1775539662848.png')

# Book covers
book_files = {
    'webdev': os.path.join(artifact_dir, 'book_webdev_1775539687050.png'),
    'python': os.path.join(artifact_dir, 'book_python_1775539704066.png'),
    'ai': os.path.join(artifact_dir, 'book_ai_1775539722548.png'),
    'security': os.path.join(artifact_dir, 'book_security_1775540693574.png'),
    'mobile': os.path.join(artifact_dir, 'book_mobile_1775540706865.png'),
    'database': os.path.join(artifact_dir, 'book_database_1775540721016.png'),
    'data': os.path.join(artifact_dir, 'book_data_1775540736039.png'),
}

media_slider = r'c:\Users\HP\Desktop\gjango-store\media\slider_images'
media_product = r'c:\Users\HP\Desktop\gjango-store\media\product_images'

os.makedirs(media_slider, exist_ok=True)
os.makedirs(media_product, exist_ok=True)

# Copy sliders
if os.path.exists(s1): shutil.copy(s1, os.path.join(media_slider, 'slider1.png'))
if os.path.exists(s2): shutil.copy(s2, os.path.join(media_slider, 'slider2.png'))
if os.path.exists(s3): shutil.copy(s3, os.path.join(media_slider, 'slider3.png'))

# Copy books
for key, path in book_files.items():
    if os.path.exists(path):
        shutil.copy(path, os.path.join(media_product, f'{key}.png'))

# Update sliders
sliders = list(slider.objects.all().order_by('order'))
if len(sliders) >= 3:
    sliders[0].image = 'slider_images/slider1.png'
    sliders[0].save()
    sliders[1].image = 'slider_images/slider2.png'
    sliders[1].save()
    sliders[2].image = 'slider_images/slider3.png'
    sliders[2].save()

# Update products
for p in product.objects.all():
    cat_name = p.category.name if p.category else ''
    
    if 'أمن' in cat_name:
        p.image = 'product_images/security.png'
    elif 'الموبايل' in cat_name:
        p.image = 'product_images/mobile.png'
    elif 'قواعد' in cat_name:
        p.image = 'product_images/database.png'
    elif 'علم البيانات' in cat_name:
        p.image = 'product_images/data.png'
    elif 'صطناعي' in cat_name:
        p.image = 'product_images/ai.png'
    elif 'بايثون' in cat_name:
        p.image = 'product_images/python.png'
    else:  # 'ويب', 'JavaScript', 'HTML' etc.
        p.image = 'product_images/webdev.png'
    p.save()

print('Data updated successfully mapping specific covers for all categories!')
