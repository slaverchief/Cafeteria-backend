class APIException(Exception):
    pass

class PageException(Exception):
    pass


class NoSelectedObjects(APIException):
    pass