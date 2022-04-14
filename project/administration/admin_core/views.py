from django.views import generic

from .mixins import StaffUserMixin

class HomeView(StaffUserMixin, generic.TemplateView):
    template_name = 'admin_core/index.html'

class PermissionDeniedView(StaffUserMixin, generic.TemplateView):
    template_name = 'admin_core/permission_denied.html'