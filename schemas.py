from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class UserCreate(BaseModel):
    username: str
    password: str
    is_admin: bool = False

class SweetCreate(BaseModel):
    name: str
    category: str
    price: float
    quantity: int

class SweetRead(SweetCreate):
    id: int