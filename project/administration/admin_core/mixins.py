from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect

class StaffUserMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('webshop_core:login')
        if not request.user.is_staff:
            return redirect('webshop_core:home')
        return super(StaffUserMixin, self).dispatch(request, *args, **kwargs)
    
class UserAccessMixin(PermissionRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('webshop_core:login')
        if not request.user.is_staff:
            return redirect('webshop_core:home')
        if not self.has_permission():
            return redirect('admin_core:permission-denied')
        return super(UserAccessMixin, self).dispatch(request, *args, **kwargs)