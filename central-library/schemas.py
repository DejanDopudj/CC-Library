from pydantic import BaseModel


class ItemBase(BaseModel):
    pass

class ItemCreate(ItemBase):
    owner_id: str


class Item(ItemBase):
    id: str
    owner_id: str
    returned: bool
    class Config:
        orm_mode = True


class UserBase(BaseModel):
    pass


class UserCreate(UserBase):
    id: str
    name: str
    surname: str
    address: str


class User(UserBase):
    id: str
    name: str
    surname: str
    address: str
    items: list[Item] = []

    class Config:
        orm_mode = True