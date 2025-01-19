# Исключения для всей части, касающейся взаимодействия с API приложения
class APIException(Exception):
    pass

# Исключения для всей части, касающейся взаимодействия с веб-интерфейсом приложения
class PageException(Exception):
    pass

# Исключение, возникающее при нарушении логики работа приложения
class LogicError(Exception):
    pass


class NoSelectedObjects(APIException):
    pass

class NonEditFieldsWereTouched(APIException):
    pass

class NestedObjectsDontExist(APIException):
    pass

class NoDatesGiven(APIException):
    pass

class TogetherConditionViolation(APIException):
    pass

