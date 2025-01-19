from rest_framework.response import Response
from rest_framework.views import APIView
from cafeteria.exceptions import NonEditFieldsWereTouched, TogetherConditionViolation
from typing import Optional

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
    _NON_EDIT_FIELDS: Optional[list] = ['id', 'pk'] # Поля, которые нельзя изменять
    _FIELDS_TOGETHER: Optional[list] = None # Список, который задает поля со следующим условием: "если хотя бы 1 поле присутствует в запросе, то все остальные поля в наборе полей должны быть указаны".

    # Метод, возвращающий очищенные от лишних полей данные
    def __clean_data(self, data):
        all_fields = dict(self._Serializer().fields).keys()  # Получение всех полей, которые есть в сериализаторе
        for key in list(data.keys()):
            if key not in all_fields:
                del data[key]
        return data


    # Проверка, содержит ли список полей поля, которые нельзя редактировать
    def _validate_input(self, fields):
        for field in fields:
            if field in self._NON_EDIT_FIELDS:
                raise NonEditFieldsWereTouched()

        if self._FIELDS_TOGETHER:
            for fields_set in self._FIELDS_TOGETHER:
                in_count = 0 # количество полей, которые совпадают у данных запроса и набора полей в FIELDS_TOGETHER
                for field in fields:
                    if field in fields_set:
                        in_count += 1
                if in_count != 0 and in_count != len(fields_set):
                    raise TogetherConditionViolation(fields_set)

    def post(self, request):
        self.__clean_data(request.data)
        self._validate_input(request.data)

    def put(self, request):
        self.select_values, self.update_values = request.data.get('select'), request.data.get(
            'update')  # получение значений для выборки и значений, на которые будут заменяться значения объектов
        if self.select_values is None or self.update_values is None:
            return Response(status=400)
        self.__clean_data(self.select_values)
        self.__clean_data(self.update_values)
        self._validate_input(self.update_values)

    # Удаляет объекты, значения которых соответствуют переданным в DELETE запросез
    def delete(self, request):
        [obj.delete() for obj in self._Model.objects.filter(**request.data)]
        return Response()