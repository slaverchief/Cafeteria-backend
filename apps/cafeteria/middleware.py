from django.db import IntegrityError
from django.http import HttpResponse
from apps.cafeteria.exceptions import *



class CustomExceptionsHandler:
    EXCEPTION_MESSAGES = {
        NoSelectedObjects: (404, "Не найдены выбранные объекты"),
        NonEditFieldsWereTouched: (400, "Вы попытались изменить неизменяемое поле")
    }

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if type(exception) in CustomExceptionsHandler.EXCEPTION_MESSAGES.keys():
            return HttpResponse(status=CustomExceptionsHandler.EXCEPTION_MESSAGES[type(exception)][0], content={CustomExceptionsHandler.EXCEPTION_MESSAGES[type(exception)][1]})
        elif type(exception) is IntegrityError:
            return HttpResponse(status=400, content=str(exception).split('\n')[0])