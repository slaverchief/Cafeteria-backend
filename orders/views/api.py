from cafeteria.exceptions import NoDatesGiven
from orders.services import *
from view_tools.serializers.orders import OrderSerializer
from orders.models import Order
from cafeteria.base_api import *

# Нужен для подсчёта выручки за определенное время
class OrdersCashApiView(APIView):

    def post(self, request):
        from_date, to_date = request.data.get("from"), request.data.get('to')
        if not from_date or not to_date:
            raise NoDatesGiven()
        return Response(calculate_cash_sum(from_date, to_date))

# Нужен для получения данных из базы данных
class ReadOrderApiView(BaseReadCafeteriaApiView):
    _Model = Order
    _Serializer = OrderSerializer

    def post(self, request):
        if 'items' not in request.data or len(request.data['items']) == 0:
            return super().post(request)
        else:
            serialized = OrderSerializer(get_orders_using_items(request.data), many=True)
            if not serialized.data:
                return Response(status=404)
            return Response(serialized.data)

# Нужен для произведения действий по изменениям базы данных
class OrderApiView(BaseCafeteriaApiView):
    _Serializer = OrderSerializer
    _Model = Order
    _FIELDS_TOGETHER = [('status', 'paid_date')]

    def post(self, request):
        super().post(request)
        create_order(request.data)
        return Response()

    # Обработка PUT методов
    def put(self, request):
        super().put(request)
        # предполагается, что в словаре передаются ID блюд, задача - конвертировать ID в объекты модели Dish
        if "items" in self.update_values:
            items = get_dishes_by_id(self.update_values['items'])

            self.update_values['items'] = items
        update_orders(self.select_values, self.update_values)
        return Response()

    # Переписанный, подобно методу POST из ReadOrderApiView представления, метод DELETE
    def delete(self, request):
        if 'items' not in request.data or len(request.data['items']) == 0:
            return super().delete(request)
        else:
            [obj.delete() for obj in get_orders_using_items(request.data)]
            return Response()