from django.views import generic
from django.shortcuts import get_object_or_404, reverse

from administration.admin_core.mixins import UserAccessMixin
from webshop.product.models import Action
from .forms import ActionForm

class ActionListView(UserAccessMixin, generic.ListView):
    permission_required = 'product.view_product' # TODO HEDA megcsinálni
    template_name = 'action/action_list.html'
    context_object_name = 'actions'

    def get_queryset(self):
        return Action.objects.all()

class ActionDetailView(UserAccessMixin, generic.UpdateView):
    permission_required = 'product.change_product' # TODO HEDA megcsinálni
    template_name = 'action/action_detail.html'
    context_object_name = 'action'
    form_class = ActionForm

    def get_object(self):
        return get_object_or_404(Action, id=self.kwargs['id'])

    def get_success_url(self):
        return reverse('admin_core:admin_action:action-list')

class ActionCreateView(UserAccessMixin, generic.CreateView):
    permission_required = 'product.add_product' # TODO HEDA megcsinálni
    template_name = 'action/action_create.html'
    form_class = ActionForm

    def get_success_url(self):
        return reverse('admin_core:admin_action:action-list')

class ActionDeleteView(UserAccessMixin, generic.DeleteView):
    permission_required = 'product.delete_product' # TODO HEDA megcsinálni
    template_name = 'action/action_delete.html'
    context_object_name = 'action'

    def get_object(self):
        return get_object_or_404(Action, id=self.kwargs['id'])
    
    def get_success_url(self):
        return reverse('admin_core:admin_action:action-list')