from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import HttpResponse
from apps.cafeteria.exceptions import *


# Middleware для обработки пользовательских исключений
class CustomExceptionsHandler:
    EXCEPTION_MESSAGES = {
        NoSelectedObjects: (404, "Не найдены выбранные объекты"),
        NonEditFieldsWereTouched: (400, "Вы попытались изменить неизменяемое поле"),
        NestedObjectsDontExist: (404, "Вы ввели несуществующие вложенные объекты"),
        ValidationError: (400, 'Данные введены в недопустимом формате')
    } # определяет текст сообщений, которые отправляются пользователю в случае вызова какого-либо исключения

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if type(exception) in CustomExceptionsHandler.EXCEPTION_MESSAGES.keys():
            return HttpResponse(status=CustomExceptionsHandler.EXCEPTION_MESSAGES[type(exception)][0], content={CustomExceptionsHandler.EXCEPTION_MESSAGES[type(exception)][1]})
        elif type(exception) is IntegrityError:
            return HttpResponse(status=400, content=str(exception).split('\n')[0]) # если исключение касается нарушений ограничений базы данных, возвращается информативная часть исключения, говорящая о том, какое ограничение нарушено