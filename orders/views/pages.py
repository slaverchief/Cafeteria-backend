import json
from orders.models import Order
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, FormView, UpdateView
from orders.forms import *
from orders.services import calculate_cash_sum, set_paid_date, get_filtered_orders

# Класс-представление для страницы отображения всех заказов
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
        queryset = get_filtered_orders(self.request.GET) # проводит фильтрацию по переданным в GET параметрах данных
        if queryset is not None:
            return queryset
        return super().get_queryset()

# Класс-представление для страницы создания заказа
class CreateOrderView(FormView):
    form_class = OrderCreateForm
    fields = "__all__"
    template_name = "orders/create_order.html"
    extra_context = {"title": "Создание заказа"}
    success_url = reverse_lazy('create')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

# Класс-представление для страницы редактирования заказа
class UpdateOrderView(UpdateView):
    model = Order
    fields = ['status', 'items']
    template_name = 'orders/edit_order.html'
    extra_context = {"title": "Редактирование заказа"}
    success_url = reverse_lazy("list")

    def post(self, request, *args, **kwargs):
        status_before = self.get_object().status
        res = super().post(request, *args, **kwargs)
        status_after = self.object.status
        set_paid_date(status_before, status_after, self.object) # вычисление статусов до и после внесения изменений, введенных пользователем и передача функции set_paid_date
        return res

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['pk'] = self.object.pk
        return context

    # Изменение стандартной формы для редактирования модели
    def get_form_class(self):
        return OrderEditForm

# Возвращает страницу для получения расчёта прибыли
def calc_cash(request):
    return render(request, template_name="orders/calc.html", context={'title': "Расчёт выручки"})

# Удаляет заказ
def delete_order(request, pk):
    Order.objects.get(pk=pk).delete()
    return HttpResponse()

# Реализует API для получения выручки через Ajax запросд
@csrf_exempt
def get_cash(request):
    data = json.loads(request.body)
    from_date, to_date = data.get('from'), data.get('to') # извлечение даты начала и конца отсчёта и передаем функции calculate_cash_sum
    return HttpResponse(calculate_cash_sum(from_date, to_date))

