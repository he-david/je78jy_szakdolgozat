from django.http import Http404
from django.views import generic

from .models import Category, Product
from .utils import get_all_children

class ProductListView(generic.ListView):
    template_name = 'product/product_list.html'
    context_object_name = 'products'

    # Overrided methods
    def get_queryset(self):
        qs = Product.objects.all()

        try:
            category_id = self.request.GET.get('category', None)

            if category_id != None:
                category_id = (int)(category_id)
        except:
            raise Http404("Invalid category")

        if category_id:
            qs = qs.filter(category_id__in=get_all_children(category_id, True))
        return qs

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)

        try:
            category_id = self.request.GET.get('category', None)

            if category_id != None:
                category_id = (int)(category_id)
        except:
            raise Http404("Invalid category")

        if category_id:
            context.update({
                'categories': Category.objects.filter(id__in=get_all_children(category_id, False)).values()
            })
        else:
            context.update({
                'categories': Category.objects.values()
            })
        return context

class ProductDetailView(generic.DeleteView):
    template_name='product/product_detail.html'
    queryset = Product.objects.all()
    context_object_name = 'product'
