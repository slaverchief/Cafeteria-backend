import datetime
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http import QueryDict
from django.db import transaction
from orders.models import Order, Dish
from cafeteria.exceptions import NestedObjectsDontExist


# Подсчитывает сумму выручки от и до определенных дат
def calculate_cash_sum(from_date: datetime.datetime, to_date: datetime.datetime):
    try:
        return sum([int(n.total_price(as_int=True)) for n in Order.objects.filter(status__lte=2,
                                                              paid_date__gte=from_date,
                                                              paid_date__lte=to_date)])
    except TypeError:
        raise ValidationError("Передан недопустимый тип для поля")

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

# Возвращает объекты блюд с ID из данного списка
def get_dishes_by_id(items: list):
    try:
        return [Dish.objects.get(pk=pk) for pk in items]
    except ObjectDoesNotExist:
        raise NestedObjectsDontExist()

# Возвращает заказы, в которых есть параметр items
def get_orders_using_items(data: dict):
    get_dishes_by_id(data['items']) # Проверка, есть ли блюда в базе данных или нет
    data['items'].append(-1)
    raw_query = "SELECT DISTINCT oo.id FROM orders_order as oo JOIN orders_order_items as ooi ON oo.id = ooi.order_id " \
                f"WHERE ooi.dish_id IN {tuple(data['items'])}"
    del data['items']
    for field in data:
        raw_query += f" AND oo.{field}={data[field]}"
    with transaction.atomic():
        objs = Order.objects.raw(raw_query+' GROUP BY oo.id;')
    return objs
