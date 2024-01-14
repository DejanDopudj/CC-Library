from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from datetime import date
from database import Base


class User(Base):
    __tablename__ = "member"

    id = Column(String(160), primary_key=True)
    name = Column(String(160),  index=True)
    surname = Column(String(160), index=True)
    address = Column(String(160),  index=True)
    

    items = relationship("Item", back_populates="owner")


class Item(Base):
    __tablename__ = "book"

    id = Column(String(160), primary_key=True)
    owner_id = Column(String(160), ForeignKey("member.id"))
    returned = Column(Boolean)

    owner = relationship("User", back_populates="items")