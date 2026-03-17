from pydantic import BaseModel
from typing import Optional, List, Union
from enum import Enum

class UserSchema(BaseModel):
    name: str
    email: str
    password: str
    active: Optional[bool]
    admin: Optional[bool]

    class Config:
        from_attributes = True 

class OrderSchema(BaseModel): 
    user_id: int
    class Config:
        from_attributes = True

class LoginSchema(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes = True

class ItemSchema(BaseModel):
    quantity: int
    size: str
    flavor: str
    unit_price: float

    class Config:
        from_attributes = True

class StatusSchema(str, Enum):
    PENDING = "PENDING"
    CANCELED = "CANCELED"
    COMPLETED = "COMPLETED"

class ResponseOrderSchema(BaseModel):
    id: int
    status: str
    total_price: float
    user_id: int
    itens: List[ItemSchema]
       
    class Config:
        from_attributes = True

class UserInfoSchema(BaseModel):
    name: str
    email: str
    active: bool
    orders: Union[List[ResponseOrderSchema], str] = [] 

    class Config:
        from_attributes = True