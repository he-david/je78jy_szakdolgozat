from django.http import Http404
from django.shortcuts import get_object_or_404, reverse
from django.views import generic

from webshop.product.models import Category, Product
from administration.admin_core.mixins import UserAccessMixin
from .forms import CategoryForm, CategoryCreateForm

class CategoryListView(UserAccessMixin, generic.ListView):
    permission_required = 'product.view_category'
    template_name = 'category/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.all() # TODO HEDA Valami alapján majd jó lenne rendezni..

class CategoryDetailView(UserAccessMixin, generic.UpdateView):
    permission_required = (
        'product.change_category', 'product.view_product',
        'product.change_product'
    )
    template_name = 'category/category_detail.html'
    context_object_name = 'category'
    form_class = CategoryForm

    def get_object(self):
        return get_object_or_404(Category, id=self.kwargs['id'])

    def get_context_data(self, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        context.update({
            'prod_items': Product.objects.filter(category_id=self.kwargs['id']),
            'cat_items': Category.objects.filter(parent_id=self.kwargs['id'])
        })
        return context

    def get_success_url(self):
        return reverse('admin_core:admin_category:category-list')

class CategoryCreateView(UserAccessMixin, generic.CreateView):
    permission_required = 'product.add_category'
    template_name = 'category/category_create.html'
    form_class = CategoryCreateForm

    def form_valid(self, form):
        form.save()
        return super(CategoryCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('admin_core:admin_category:category-list')

class CategoryDeleteView(UserAccessMixin, generic.DeleteView):
    permission_required = 'product.delete_category'
    template_name = 'category/category_delete.html'
    context_object_name = 'category'

    def get_object(self):
        return get_object_or_404(Category, id=self.kwargs['id'])

    def get_context_data(self, **kwargs):
        context = super(CategoryDeleteView, self).get_context_data(**kwargs)
        context.update({
            'sub_cat_count': Category.objects.filter(parent_id=self.kwargs['id']).count(),
            'cat_prod_count': Product.objects.filter(category_id=self.kwargs['id']).count()
        })
        return context
    
    def get_success_url(self):
        return reverse('admin_core:admin_category:category-list')
        