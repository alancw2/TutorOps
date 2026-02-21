from pydantic import BaseModel, Field
from pydantic import EmailStr

class ClientCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str | None = None
    subject: str | None = None
    hourly_rate: float = Field(..., gt=0.0)


class ClientOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone: str | None = None
    subject: str | None = None
    hourly_rate: float = Field(..., gt=0.0)

class SessionCreate(BaseModel):
    client_id: int
    date: str
    duration_hours: float = Field(..., gt=0.0)
    topic: str | None = None
    notes: str | None = None

class SessionOut(BaseModel):
    id: int
    client_id: int
    date: str
    duration_hours: float = Field(..., gt=0.0)
    topic: str | None = None
    notes: str | None = None
    
class ClientSummaryOut(BaseModel):
    client_id: int
    total_sessions: int
    total_hours: float = Field(..., ge=0.0)
    total_earnings: float = Field (..., ge=0.0)


class GlobalSummaryOut(BaseModel):
    total_clients: int
    total_sessions: int
    total_hours: float = Field(..., ge = 0.0)
    total_earnings: float = Field(..., ge=0.0)





