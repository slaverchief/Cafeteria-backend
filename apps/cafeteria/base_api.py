from rest_framework.response import Response
from rest_framework.views import APIView
from apps.cafeteria.exceptions import NonEditFieldsWereTouched

# Базовый класс для APIView кафетерия
class BaseCafeteriaApiView(APIView):
    _Serializer = None
    _Model = None
    _NON_EDIT_FIELDS = ['id', 'pk']

    # Проверка, содержит ли список полей поля, которые нельзя редактировать
    def _is_valid_input(self, fields):
        for field in fields:
            if field in self._NON_EDIT_FIELDS:
                raise NonEditFieldsWereTouched()

    # Отвечает на GET методы. На вход принимает значения, по которым фильтруются объекты модели
    def get(self, request):
        serializers = self._Serializer( self._Model.objects.filter(**request.data), many=True)
        return Response(serializers.data)

    # Удаляет объекты, значения которых соответствуют переданным в DELETE запросез
    def delete(self, request):
        [obj.delete() for obj in self._Model.objects.filter(**request.data)]
        return Response()