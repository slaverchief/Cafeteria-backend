from django.http import HttpResponse
from rest_framework.response import Response
from apps.cafeteria.exceptions import *



class CustomExceptionsHandler:
    EXCEPTION_MESSAGES = {
        NoSelectedObjects: (404, "Не найдены выбранные объекты")
    }

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if type(exception) in CustomExceptionsHandler.EXCEPTION_MESSAGES.keys():
            return HttpResponse(status=CustomExceptionsHandler.EXCEPTION_MESSAGES[type(exception)][0], content={CustomExceptionsHandler.EXCEPTION_MESSAGES[type(exception)][1]})