from apps.cafeteria.exceptions import NonEditFieldsWereTouched
# from apps.orders.services import update_orders
from apps.cafeteria.base_api import BaseCafeteriaApiView
from serializers.orders import OrderSerializer
from apps.orders.models import Order

class OrderApiView(BaseCafeteriaApiView):
    Serializer = OrderSerializer
    Model = Order
    NON_EDIT_FIELDS = ['id', 'pk']

    # @staticmethod
    # def is_valid_input(fields):
    #     for field in fields:
    #         if field in OrderApiView.NON_EDIT_FIELDS:
    #             raise NonEditFieldsWereTouched()

    # def put(self, request):
    #     select_values, update_values = request.data.get('select'), request.data.get('update')
    #     OrderApiView.is_valid_input(update_values)
    #     if select_values is None or update_values is None:
    #         return Response(status=400)
    #     update_orders(select_values, update_values)
    #     return Response()

