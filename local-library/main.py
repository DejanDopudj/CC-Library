from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from crud import *
from models import Base
from schemas import BookCreate, LoanCreate,Book, Loan
from database import SessionLocal, engine
import os
import requests

Base.metadata.create_all(bind=engine)

app = FastAPI(openapi_prefix=f"/{os.getenv('LOCAL_DATABASE')}")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint to create a book
@app.post("/books/", response_model=Book)
def create_book_api(book_data: BookCreate, db: Session = Depends(get_db)):
    return create_book(db, book_data)

# Endpoint to get a book by ID
@app.get("/books/{book_id}", response_model=Book)
def get_book_api(book_id: str, db: Session = Depends(get_db)):
    db_book = get_book(db, book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

# Endpoint to create a loan
@app.post("/loans/", response_model=Loan)
def create_loan_api(loan_data: LoanCreate, db: Session = Depends(get_db)):
    response = requests.get(url=f"http://central-library:81/central/check_items/{loan_data.user_id}").text
    if response.replace("\"", "").strip() == "eligible":  
        id = requests.post(url=f"http://central-library:81/central/users/items/", json={"owner_id": f"{loan_data.user_id}"}).content
        return create_loan(db, loan_data, id)
    else:
        raise HTTPException(status_code=404, detail="User not eligible")

# Endpoint to get a loan by ID
@app.get("/loans/{loan_id}", response_model=Loan)
def read_loan_api(loan_id: str, db: Session = Depends(get_db)):
    db_loan = get_loan(db, loan_id)
    if db_loan is None:
        raise HTTPException(status_code=404, detail="Loan not found")
    return db_loan