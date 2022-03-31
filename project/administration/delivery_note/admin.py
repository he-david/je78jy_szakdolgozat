from django.contrib import admin

from .models import DeliveryNote, DeliveryNoteItem

admin.site.register(DeliveryNote)
admin.site.register(DeliveryNoteItem)