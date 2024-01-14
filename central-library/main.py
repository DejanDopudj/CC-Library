from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from crud import *
from models import Base
from schemas import User, Item, UserCreate, ItemCreate
from database import SessionLocal, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(openapi_prefix="/central")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=User)
def create_user_api(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id=user.id)
    if db_user:
        raise HTTPException(status_code=400, detail="User with this ID already exists")
    return create_user(db=db, user=user)

@app.get("/users/", response_model=list[User])
def read_users_api(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=User)
def read_user_api(user_id: str, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.post("/users/items/", response_model=Item)
def create_item_for_user_api(
    item: ItemCreate, db: Session = Depends(get_db)
):
    return create_user_item(db=db, item=item)

@app.get("/items/", response_model=list[Item])
def read_items_api(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = get_items(db, skip=skip, limit=limit)
    return items

@app.put("/return_item/{item_id}", response_model=None)
def return_item_api(item_id: str, db: Session = Depends(get_db)):
    db_item = get_item(db, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return_item(db=db, item_id=item_id)
    return None

@app.get("/check_items/{user_id}", response_model=bool)
def check_items_api(user_id: str, db: Session = Depends(get_db)):
    return check_items(db=db, user_id=user_id)