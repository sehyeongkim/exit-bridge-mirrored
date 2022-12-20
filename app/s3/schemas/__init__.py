from .s3 import *


class ExceptionResponseSchema(BaseModel):
    error_code: str
    message: str

class RequestValidationExceptionResponseSchema(BaseModel):
    error_code: str
    message: str