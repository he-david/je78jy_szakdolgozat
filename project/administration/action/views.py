from django.views import generic
from django.shortcuts import get_object_or_404, reverse

from administration.admin_core.mixins import UserAccessMixin
from webshop.product.models import Action
from .forms import ActionForm
from administration.admin_core import utils as admin_utils

class ActionListView(UserAccessMixin, generic.ListView):
    permission_required = 'product.view_action'
    template_name = 'action/action_list.html'
    paginate_by = 25
    ORDER_LIST = [
        'name', '-name',
        'percent', '-percent',
        'from_date', '-from_date'
        'to_date', '-to_date'
    ]

    def get_queryset(self):
        order_by_attr = self.request.GET.get('order_by', 'name')
        return Action.objects.all().order_by(admin_utils.get_order_attr(order_by_attr, 'name', self.ORDER_LIST))

    def get_context_data(self, **kwargs):
        context = super(ActionListView, self).get_context_data(**kwargs)
        order_attr = self.request.GET.get('order_by', 'name')
        return admin_utils.order_by_context_fill(context, order_attr, self.ORDER_LIST)

class ActionDetailView(UserAccessMixin, generic.UpdateView):
    permission_required = 'product.change_action'
    template_name = 'action/action_detail.html'
    context_object_name = 'action'
    form_class = ActionForm

    def get_object(self):
        return get_object_or_404(Action, id=self.kwargs['id'])

    def get_success_url(self):
        return reverse('admin_core:admin_action:action-list')

class ActionCreateView(UserAccessMixin, generic.CreateView):
    permission_required = 'product.add_action'
    template_name = 'action/action_create.html'
    form_class = ActionForm

    def get_success_url(self):
        return reverse('admin_core:admin_action:action-list')

class ActionDeleteView(UserAccessMixin, generic.DeleteView):
    permission_required = 'product.delete_action'
    template_name = 'action/action_delete.html'
    context_object_name = 'action'

    def get_object(self):
        return get_object_or_404(Action, id=self.kwargs['id'])
    
    def get_success_url(self):
        return reverse('admin_core:admin_action:action-list')