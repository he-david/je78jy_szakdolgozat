from django.views import generic

from webshop.core.models import CustomUser
from .mixins import UserAccessMixin, StaffUserMixin


class HomeView(StaffUserMixin, generic.TemplateView):
    template_name = 'admin_core/index.html'

class PartnerListView(UserAccessMixin, generic.ListView):
    permission_required = 'core.view_customuser'
    template_name = 'admin_core/partner_list.html'
    context_object_name = 'partners'

    def get_queryset(self):
        return CustomUser.objects.filter(is_staff=False)

class PermissionDeniedView(StaffUserMixin, generic.TemplateView):
    template_name = 'admin_core/permission_denied.html'