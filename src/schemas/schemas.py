from typing import Optional, List
from datetime import date

from pydantic import BaseModel, EmailStr, Field


class ContactSchema(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    phone_number: str
    birthday: date
    additional_data: str


class ContactUpdateSchema(ContactSchema):
    pass
    # first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    # last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    # email: Optional[EmailStr] = None
    # phone_number: Optional[str] = None
    # birthday: Optional[date] = None
    # additional_data: Optional[str] = None


class ContactResponse(ContactSchema):
    id: int
    # first_name: str
    # last_name: str
    # email: EmailStr
    # phone_number: str
    # birthday: date
    # additional_data: str

    class Config:
        from_attributes = True


# Добавляем схему для ответа с информацией о контакте с днем рождения в ближайшие 7 дней
class ContactBirthdayResponse(ContactResponse):
    pass
    # id: int
    # first_name: str
    # last_name: str
    # email: EmailStr
    # phone_number: str
    # birthday: date
    # additional_data: str

    class Config:
        from_attributes = True


class UpcomingBirthdaysResponse(BaseModel):
    upcoming_birthdays: List[ContactBirthdayResponse]
