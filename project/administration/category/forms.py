from django import forms

from webshop.product.models import Category
from webshop.product import utils as product_utils

class CategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['parent_id'].queryset = Category.objects.exclude(id__in=product_utils.get_all_children(self.instance.id, True))

    class Meta:
        model = Category
        fields = ('name', 'parent_id')
        labels = {
            'name': 'Név',
            'parent_id': 'Szülő kategória'
        }

class CategoryCreateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'parent_id')
        labels = {
            'name': 'Név',
            'parent_id': 'Szülő kategória'
        }