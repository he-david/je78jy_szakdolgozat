from django.contrib import admin

from .models import Action, PackageType, Category, Product

admin.site.register(Action)
admin.site.register(PackageType)
admin.site.register(Category)
admin.site.register(Product)
