from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from crud import *
from models import Base
from schemas import BookCreate, LoanCreate,Book, Loan, UserCreate
from database import SessionLocal, engine
import os
import requests

Base.metadata.create_all(bind=engine)

app = FastAPI(openapi_prefix=f"/{os.getenv('LOCAL_DATABASE')}")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/books/", response_model=Book)
def create_book_api(book_data: BookCreate, db: Session = Depends(get_db)):
    if check_book_isbn(db, book_data.isbn) is not None:
        raise HTTPException(status_code=404, detail="Book with isbn already exists")
    return create_book(db, book_data)

@app.get("/books/{book_id}", response_model=Book)
def get_book_api(book_id: str, db: Session = Depends(get_db)):
    db_book = get_book(db, book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@app.post("/loans/", response_model=Loan)
def create_loan_api(loan_data: LoanCreate, db: Session = Depends(get_db)):
    response = requests.get(url=f"http://central-library:81/central/check_items/{loan_data.user_id}").text
    user_existent = requests.get(url=f"http://central-library:81/central/users/{loan_data.user_id}").status_code
    if user_existent == 200:
        if get_book(db, loan_data.book_id) is not None:
            if response.replace("\"", "").strip() == "eligible":  
                id = requests.post(url=f"http://central-library:81/central/users/items/", json={"owner_id": f"{loan_data.user_id}"}).content
                return create_loan(db, loan_data, id)
            else:
                raise HTTPException(status_code=404, detail="User not eligible")
        else:
            raise HTTPException(status_code=404, detail="Book not found")
    else:
        raise HTTPException(status_code=404, detail="User not existent")


@app.put("/return_loans/{item_id}", response_model=None)
def return_item_api(item_id: str, db: Session = Depends(get_db)):
    loan = get_loan(db, item_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    response = requests.put(url=f"http://central-library:81/central/return_item/{item_id}").status_code
    if response == 200:
        return_loan(db, item_id)
        return True
    else:
        raise HTTPException(status_code=404, detail="Loan not found")

@app.get("/loans/{loan_id}", response_model=Loan)
def read_loan_api(loan_id: str, db: Session = Depends(get_db)):
    db_loan = get_loan(db, loan_id)
    if db_loan is None:
        raise HTTPException(status_code=404, detail="Loan not found")
    return db_loan


@app.post("/users/", response_model=bool)
def create_user_api(user: UserCreate, db: Session = Depends(get_db)):
    response = requests.post(url=f"http://central-library:81/central/users/", json={"id": user.id, "name": user.name, "surname": user.surname, "address": user.address}).status_code
    if response != 200:
        raise HTTPException(status_code=400, detail="User with this ID already exists")
    return True