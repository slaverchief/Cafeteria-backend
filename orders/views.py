
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, FormView

from .forms import OrderCreateForm
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
        tn = self.request.GET.get('tn')
        if tn:
            return Order.objects.filter(table_number=tn)
        if status:
            return Order.objects.filter(status=status)
        return super().get_queryset()




class CreateOrderView(FormView):
    form_class = OrderCreateForm
    fields = "__all__"
    template_name = "orders/create_order.html"
    extra_context = {"title": "Создание заказа"}
    success_url = reverse_lazy('create')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
