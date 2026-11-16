from .models import category

def categories(request):
    return {
        'categories': category.objects.order_by('order'),
    }