from .post import *
from .union import *


class ExceptionResponseSchema(BaseModel):
    error: str
