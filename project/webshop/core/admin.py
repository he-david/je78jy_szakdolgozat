from django.contrib import admin

from webshop.product.models import Action, PackageType, Category, Product
from webshop.core.models import FAQTopic, FAQ

admin.site.register(Action)
admin.site.register(PackageType)
admin.site.register(Category)
admin.site.register(Product)

admin.site.register(FAQTopic)
admin.site.register(FAQ)

