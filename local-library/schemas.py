from pydantic import BaseModel

class BookBase(BaseModel):
    title: str
    author: str

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: str

    class Config:
        orm_mode = True

class LoanBase(BaseModel):
    book_id: str

class LoanCreate(LoanBase):
    user_id: str

class Loan(LoanBase):
    id: str

    class Config:
        orm_mode = True
