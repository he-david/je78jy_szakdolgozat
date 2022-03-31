from django.contrib import admin

from .models import ProductReceipt, ProductReceiptItem

admin.site.register(ProductReceipt)
admin.site.register(ProductReceiptItem)
