import datetime

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http import QueryDict

from serializers.orders import OrderSerializer
from .models import Order, Dish
from ..cafeteria.exceptions import NoSelectedObjects, NestedObjectsDontExist


# Подсчитывает сумму выручки от и до определенных дат
def calculate_cash_sum(from_date: datetime.datetime, to_date: datetime.datetime):
    try:
        return sum([int(n.total_price(as_int=True)) for n in Order.objects.filter(status__lte=2,
                                                              paid_date__gte=from_date,
                                                              paid_date__lte=to_date)])
    except TypeError:
        raise ValidationError("Передан недопустимый тип для поля")

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

# Обновляет значения заказов
def update_orders(select: dict, update: dict):
    if 'items' in select and len(select['items']) != 0: # такая же логика как и в POST запроса для retrieve операций при наличии значения items в фильтре
        queryset = get_orders_using_items(select)
    else:
        queryset = Order.objects.filter(**select) # берём все объекты модели Order, которые прописаны в словаре select
    if not queryset:
        raise NoSelectedObjects()
    for obj in queryset:
        for field in update:
            if field == 'items':
                obj.items.set(update['items']) # для поля items полностью меняем все связи
            else:
                setattr(obj, field, update[field]) # для всех остальных полей просто присваиваем значения из словаря update

        obj.save()

# Возвращает объекты блюд с ID из данного списка
def get_dishes_by_id(items: list):
    try:
        return [Dish.objects.get(pk=pk) for pk in items]
    except ObjectDoesNotExist:
        raise NestedObjectsDontExist()

# Возвращает заказы, в которых есть параметр items
def get_orders_using_items(data: dict):
    get_dishes_by_id(data['items'])
    data['items'].append(-1)
    raw_query = "SELECT DISTINCT oo.id FROM orders_order as oo JOIN orders_order_items as ooi ON oo.id = ooi.order_id " \
                f"WHERE ooi.dish_id IN {tuple(data['items'])}"
    del data['items']
    for field in data:
        raw_query += f" AND oo.{field}={data[field]}"
    objs = list(Order.objects.raw(raw_query+' GROUP BY oo.id;'))
    return objs

# Создает заказ
def create_order(create_data):
    s = OrderSerializer(data=create_data)
    s.is_valid(raise_exception=True)
    s = s.save()
    if 'items' in create_data:
        s.items.set(get_dishes_by_id(create_data['items']))
        s.save()