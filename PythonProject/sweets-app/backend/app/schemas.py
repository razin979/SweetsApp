from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=1, max_length=200)
    is_admin: bool = False

class Token(BaseModel):
    access_token: str
    token_type: str

class LoginCredentials(BaseModel):
    email: str
    password: str = Field(..., min_length=1, max_length=200)

class SweetBase(BaseModel):
    name: str
    category: str
    price: float
    quantity: int

class SweetCreate(SweetBase):
    pass

class SweetOut(SweetBase):
    id: str
