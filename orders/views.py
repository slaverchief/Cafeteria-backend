from django.shortcuts import render
from django.views.generic import ListView
from .models import *

class OrdersListView(ListView):
    model = Order
    context_object_name = 'orders'
    template_name = 'orders/list_orders.html'
    extra_context = {'title': 'Список заказов'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        status = self.request.GET.get('status')
        if status:
            context['status_filter'] = status
        return context

    def get_queryset(self):
        status = self.request.GET.get('status')
        if not status:
            return super().get_queryset()
        return Order.objects.filter(status=status)
