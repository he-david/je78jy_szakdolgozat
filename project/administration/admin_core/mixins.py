from django.shortcuts import redirect

class StaffUserMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_staff:
            return redirect('webshop_core:home')
        return super(StaffUserMixin, self).dispatch(request, *args, **kwargs)
    