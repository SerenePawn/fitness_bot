from pydantic import BaseModel
from typing import (
    Optional,
    List,
    TypeVar
)

T = TypeVar('T')


class BaseCommonModel(BaseModel):
    id: int
