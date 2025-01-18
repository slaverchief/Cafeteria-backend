
from rest_framework.response import Response
from apps.orders.services import *
from apps.cafeteria.base_api import BaseCafeteriaApiView
from serializers.orders import OrderSerializer
from apps.orders.models import Order


class OrderApiView(BaseCafeteriaApiView):
    _Serializer = OrderSerializer
    _Model = Order

    def post(self, request):
        create_order(request.data)
        return Response()

    def get(self, request):
        if 'items' not in request.data:
            return super().get(request)
        return Response(self._Serializer(get_orders(request.data), many=True).data)

    # Обработка PUT методов
    def put(self, request):
        select_values, update_values = request.data.get('select'), request.data.get('update') # получение значений для выборки и значений, на которые будут заменяться значения объектов
        self._is_valid_input(update_values)
        if select_values is None or update_values is None:
            return Response(status=400)
        # предполагается, что в словаре передаются ID блюд, задача - конвертировать ID в объекты модели Dish
        if "items" in update_values:
            items = get_dishes_by_id(update_values['items'])

            update_values['items'] = items
        update_orders(select_values, update_values)
        return Response()

