from pydantic import BaseModel


class StaffModel(BaseModel):
    id: int
    user_id: int
    is_stuff: bool
    is_superadmin: bool
