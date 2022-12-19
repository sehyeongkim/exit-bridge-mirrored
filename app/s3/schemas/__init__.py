from .s3 import *


class ExceptionResponseSchema(BaseModel):
    code: str
    error_code: str
    message: str

class RequestValidationExceptionResponseSchema(BaseModel):
    code: str
    error_code: str
    message: str