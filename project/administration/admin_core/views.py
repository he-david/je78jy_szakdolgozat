from django.views import generic

from webshop.core.models import CustomUser
from django.db.models import Q
from administration.invoice.models import Invoice
from .mixins import StaffUserMixin

import math

class HomeView(StaffUserMixin, generic.TemplateView):
    template_name = 'admin_core/index.html'

class PartnerListView(StaffUserMixin, generic.ListView):
    template_name = 'admin_core/partner_list.html'
    context_object_name = 'partners'

    def get_queryset(self):
        return CustomUser.objects.all()
