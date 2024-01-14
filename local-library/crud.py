from sqlalchemy.orm import Session

from datetime import date
from models import Book, Loan
from schemas import BookCreate, LoanCreate
import uuid

def create_book(db: Session, book_data: BookCreate):
    db_book = Book(id=uuid.uuid4(), title=book_data.title, author=book_data.author)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def create_loan(db: Session, loan_data: LoanCreate, id: str):
    db_loan = Loan(
        id = id.decode("utf-8").replace("\"", ""),
        book_id=loan_data.book_id,
        date_took=date.today(),
        date_returned=None
    )
    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)
    return db_loan

def return_loan(loan_id: str):
    db.query(Loan).filter(Loan.id == loan_id).update({"date_returned": date.now()})
    db.commit()

def get_book(db: Session, book_id: str):
    return db.query(Book).filter(Book.id == book_id).first()

def get_loan(db: Session, loan_id: str):
    return db.query(Loan).filter(Loan.id == loan_id).first()