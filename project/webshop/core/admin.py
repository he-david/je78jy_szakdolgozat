from django.contrib import admin

from .models import Address, Contact, FAQTopic, FAQ, CustomUser
from .forms import CustomUserChangeForm, CustomUserCreationForm

class CustomUserAdmin(admin.ModelAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ['username', 'email']

admin.site.register(FAQTopic)
admin.site.register(FAQ)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Address)
admin.site.register(Contact)

