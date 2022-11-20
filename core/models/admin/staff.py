from pydantic import BaseModel


class StaffModel(BaseModel):
    user_id: int
    banned: bool
    is_staff: bool
    is_superadmin: bool
