from uuid import UUID, uuid4
from database import Base
from sqlalchemy import Column, String, Date, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from datetime import date


class Book(Base):
    __tablename__ = "book"
    id = Column(String(160), primary_key=True, default=uuid4)
    title = Column(String(160))
    author = Column(String(160))


class Loan(Base):
    __tablename__ = "loan"
    id = Column(String(160), primary_key=True, default=uuid4)
    book_id = Column(String(160), ForeignKey("book.id"))
    date_took = Column(Date, default=date.today())
    date_returned = Column(Date, default=None)