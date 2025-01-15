from django.shortcuts import render
from django.views.generic import ListView
from .models import *

class OrdersListView(ListView):
    model = Order
    context_object_name = 'orders'
    template_name = 'orders/list_orders.html'
    extra_context = {'title': 'Список заказов'}

