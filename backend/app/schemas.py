from pydantic import BaseModel, Field
from pydantic import EmailStr

phoneDefault = str | None
subjectDefault = str | None


class ClientCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str = phoneDefault
    subject: str = subjectDefault
    hourly_rate: float = Field(..., ge=0.0)


class ClientOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone: str = phoneDefault
    subject: str = subjectDefault
    hourly_rate: float = Field(..., ge=0.0)