from django.views import generic

from webshop.product.models import Category, Product

class ProductListView(generic.ListView):
    template_name = 'product/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        qs = Product.objects.all()
        return qs

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context.update({
            'categories': Category.objects.values('name')
        })
        return context

class ProductDetailView(generic.DeleteView):
    template_name='product/product_detail.html'
    queryset = Product.objects.all()
    context_object_name = 'product'
