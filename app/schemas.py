from pydantic import BaseModel, EmailStr
from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

class Config:
    from_attributes = True
class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    price: int
    category: str


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str | None
    price: int
    category: str

class Config:
    from_attributes = True

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)


class OrderCreate(BaseModel):
    user_id: int
    items: list[OrderItemCreate] = Field(min_length=1)

class OrderItemResponse(BaseModel):
    id: int
    order_id: int
    product_id: int
    quantity: int
    price: int

class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    id: int
    user_id: int
    total_amount: int
    status: str

class Config:
        from_attributes = True