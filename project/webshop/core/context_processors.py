from webshop.product.models import Category

def base_categories(request):
    return {'base_categories': Category.objects.filter(parent_id=None)}