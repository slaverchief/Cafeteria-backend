from rest_framework.response import Response
from rest_framework.views import APIView
from apps.cafeteria.exceptions import NonEditFieldsWereTouched

class BaseReadCafeteriaApiView(APIView):
    _Serializer = None
    _Model = None

    # Возвращает все объекты переданной модели
    def get(self, request):
        serialized = self._Serializer(self._Model.objects.all(), many=True)
        return Response(serialized.data)

    # Отвечает на POST методы. На вход принимает значения, по которым фильтруются и возвращаются объекты модели
    def post(self, request):
        serialized = self._Serializer(self._Model.objects.filter(**request.data), many=True)
        if not serialized.data:
            return Response(status=404)
        return Response(serialized.data)


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

    # Удаляет объекты, значения которых соответствуют переданным в DELETE запросез
    def delete(self, request):
        [obj.delete() for obj in self._Model.objects.filter(**request.data)]
        return Response()