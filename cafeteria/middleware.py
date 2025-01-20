from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import HttpResponse
from cafeteria.exceptions import *


# Middleware для обработки пользовательских исключений
class CustomExceptionsHandler:
    EXCEPTION_MESSAGES = {
        NoSelectedObjects: (404, "Не найдены выбранные объекты"),
        NonEditFieldsWereTouched: (400, "Вы попытались изменить неизменяемое поле"),
        NestedObjectsDontExist: (404, "Вы ввели несуществующие вложенные объекты"),
        NoDatesGiven: (400, 'В запросе не указаны все необходимые даты')
    } # определяет текст сообщений, которые отправляются пользователю в случае вызова какого-либо ПРОСТОГО исключения

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if type(exception) in CustomExceptionsHandler.EXCEPTION_MESSAGES.keys():
            return HttpResponse(status=CustomExceptionsHandler.EXCEPTION_MESSAGES[type(exception)][0], content={CustomExceptionsHandler.EXCEPTION_MESSAGES[type(exception)][1]})
        # elif type(exception) is IntegrityError:
        #     return HttpResponse(status=400, content=str(exception).split('\n')[0]) # если исключение касается нарушений ограничений базы данных, возвращается информативная часть исключения, говорящая о том, какое ограничение нарушено
        elif type(exception) is TogetherConditionViolation:
            return HttpResponse(status=400, content=f'Следующие поля должны присутствовать в запросе вместе или вообще отсутствовать: {exception}')
        elif type(exception) is LogicError:
            return HttpResponse(status=400, content=f'Нарушена логика: {exception}')
        elif type(exception) is ValidationError:
            return HttpResponse(status=400, content=f'Ошибка при валидации введенных значений: {exception}')