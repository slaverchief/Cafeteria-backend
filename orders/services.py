from datetime import datetime

from django.db.models import QuerySet
from django.http import QueryDict

from .models import Order

# Подсчитывает сумму выручки от и до определенных дат
def calculate_cash_sum(from_date: datetime, to_date: datetime):
    return sum([int(n.total_price(as_int=True)) for n in Order.objects.filter(status__lte=2,
                                                              paid_date__gte=from_date,
                                                              paid_date__lte=to_date)])

# Задает дату оплаты или стирает дату оплаты в зависимости от того какой статус был до этого
def set_paid_date(status_before: int, status_after: int, order: Order):
    print(type(order))
    if status_before == status_after:
        return
    elif status_before == 3:
        order.paid_date = datetime.datetime.now()
        order.save()
    elif status_before in (1, 2) and status_after == 3:
        order.paid_date = None
        order.save()

# Возвращает список объектов, отфильтрованных по переданным в GET запросе значениям
def get_filtered_orders(data: QueryDict):
    status = data.get('status')
    tn = data.get('tn')
    if tn:
        if not tn.isdigit():
            return
        return Order.objects.filter(table_number=tn)
    if status:
        if not status.isdigit():
            return
        return Order.objects.filter(status=status)
    if tn or status:
        return QuerySet([])