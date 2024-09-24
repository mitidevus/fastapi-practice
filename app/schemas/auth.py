from pydantic import BaseModel, EmailStr
from typing import Optional

class LoginPayload(BaseModel):
    email: EmailStr
    password: str