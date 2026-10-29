from pydantic import BaseModel, EmailStr, Field
from typing import Optional
class SignupIn(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
class LoginIn(BaseModel):
    email: EmailStr
    password: str
class TicketIn(BaseModel):
    subject: str = Field(min_length=3, max_length=300)
    description: str = Field(min_length=3)
    customer_email: str = ""
    category: str = "General"
    priority: str = "medium"
class TicketUpdate(BaseModel):
    subject: Optional[str] = None
    description: Optional[str] = None
    customer_email: Optional[str] = None
    category: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    ai_draft: Optional[str] = None
class DraftIn(BaseModel): additional_context: str = ""
class ApproveIn(BaseModel): edited_reply: str = Field(min_length=1)
