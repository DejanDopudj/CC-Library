from sqlalchemy.orm import Session

from models import User, Item
from schemas import UserCreate, ItemCreate
import uuid


def get_user(db: Session, user_id: str):
    return db.query(User).filter(User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate):
    db_user = User(
        id=user.id,
        name=user.name,
        surname=user.surname,
        address=user.address
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_item(db: Session, id: str):
    return db.query(Item).filter(Item.id == id).first()


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Item).offset(skip).limit(limit).all()

def return_item(db: Session, item_id: str):
    db.query(Item).filter(Item.id == item_id).update({"returned": True})
    db.commit()

def check_items(db: Session, user_id:str):
    items = db.query(Item).filter(Item.owner_id == user_id, Item.returned == False).count()
    return items >= 3

def create_user_item(db: Session, item: ItemCreate):
    db_item = Item(
        id=uuid.uuid4(),
        returned=False,
        owner_id=item.owner_id
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item