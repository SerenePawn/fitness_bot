from datetime import datetime
from typing import Optional

from core.models.base.common import (
    BaseCommonModel
)


class UserModel(BaseCommonModel):
    weight_wished: int
    status: str
    lang_code: str
    ctime: Optional[datetime]


class WeighingModel(BaseCommonModel):
    id: Optional[int]
    user_id: int
    weight: int
    ctime: datetime


class UserSearchUpdateModel(BaseCommonModel):
    id: Optional[int]
    weight_wished: Optional[int]
    status: Optional[str]
    lang_code: Optional[str]
    ctime: Optional[datetime]


class WeighingSearchUpdateModel(BaseCommonModel):
    id: Optional[int]
    user_id: Optional[int]
    weight: Optional[int]
    ctime: Optional[datetime]
