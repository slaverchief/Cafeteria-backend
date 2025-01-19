import datetime
from view_tools.serializers.orders import OrderSerializer
from orders.models import Order, Dish
from cafeteria.exceptions import NoSelectedObjects, LogicError
from .get_services import get_orders_using_items, get_dishes_by_id


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

# Обновляет значения заказов
def update_orders(select: dict, update: dict):
    if 'items' in select and len(select['items']) != 0: # такая же логика как и в POST запроса для retrieve операций при наличии значения items в фильтре
        queryset = get_orders_using_items(select) # если выборка ведется по полю items, вызывается отдельная функция
    else:
        queryset = Order.objects.filter(**select) # берём все объекты модели Order, которые соответствуют выборке в словаре select
    if not queryset:
        raise NoSelectedObjects()
    for obj in queryset:
        for field in update:
            if field == 'items':
                obj.items.set(update['items']) # для поля items полностью меняем все связи
            else:
                setattr(obj, field, update[field]) # для всех остальных полей просто присваиваем значения из словаря update
        if obj.status == 1 and not obj.paid_date:
            raise LogicError("при статусе 'оплачено' обязательно должна быть указана дата оплаты")
        if not obj.items.all():
            raise LogicError("в заказе должно быть выбрано хотя бы 1 блюдо")
        obj.save()

# Создает заказ
def create_order(create_data):
    if 'items' not in create_data or not create_data['items']:
        raise LogicError("в заказе должно быть выбрано хотя бы 1 блюдо")
    s = OrderSerializer(data=create_data)
    s.is_valid(raise_exception=True)
    if s.validated_data.get('status') == 1 and not s.validated_data.get('paid_date'):
        raise LogicError("при статусе 'оплачено' обязательно должна быть указана дата оплаты")
    s = s.save()
    s.items.set(get_dishes_by_id(create_data['items']))
    s.save()