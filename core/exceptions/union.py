from core.exceptions import CustomException


class UnionNameDuplicatedException(CustomException):
    code = 409
    error_code = "UNION__DUPLICATE_UNION_NAME_ERROR"
    message = "union name is duplicated"
