import datetime
from django.http import QueryDict

from .models import Order

# Подсчитывает сумму выручки от и до определенных дат
def calculate_cash_sum(from_date: datetime.datetime, to_date: datetime.datetime):
    return sum([int(n.total_price(as_int=True)) for n in Order.objects.filter(status__lte=2,
                                                              paid_date__gte=from_date,
                                                              paid_date__lte=to_date)])

# Задает дату оплаты или стирает дату оплаты в зависимости от того какой статус был до этого
def set_paid_date(status_before: int, status_after: int, order: Order):
    if status_before == status_after: # если статусы до и после изменений - одинаковы, не производим больше никаких действий
        return
    elif status_after == 1: # если статусы неодинаковы и при этом после изменений статус стал "Оплачено", задается дата оплаты
        order.paid_date = datetime.datetime.now()
        order.save()
    elif status_before == 1: # если статусы неодинаковы и при этом статус до изменений был "Оплачено", дата оплаты стирается
        order.paid_date = None
        order.save()

# Возвращает список объектов, отфильтрованных по переданным в GET запросе значениям
def get_filtered_orders(data: QueryDict):
    status = data.get('status') # статус, заказы с которым надо вернуть пользователю
    tn = data.get('tn') # номер стола, получаемый из строки поиска по номеру стола

    # если хотя бы один из параметров был передан, но он не был валидный, возвращается ответ такой, будто бы параметры не был переданы вообще
    if tn:
        if not tn.isdigit():
            return
        return Order.objects.filter(table_number=tn)
    elif status:
        if not status.isdigit():
            return
        return Order.objects.filter(status=status)
