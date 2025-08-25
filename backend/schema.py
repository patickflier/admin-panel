from pydantic import BaseModel, EmailStr
from typing import Optional


class BookingCreateDto(BaseModel):
    email: EmailStr
    fullname: str
    first: Optional[str] = None
    infix: Optional[str] = None
    last: Optional[str] = None
    location_id: Optional[int] = None
    activity_id: Optional[int] = None
    package_id: Optional[int] = None
