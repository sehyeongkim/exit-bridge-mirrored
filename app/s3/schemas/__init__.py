from .s3 import *


class ExceptionResponseSchema(BaseModel):
    error: str
