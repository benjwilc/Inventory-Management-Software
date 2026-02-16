from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Text, DECIMAL, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from pydantic import BaseModel


#Database connection
DATABASE_URL = "postgresql://benwilcox@localhost:5432/inventory_db"
engine = create_engine(DATABASE_URL)
sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

#class that matches database table
class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    quantity = Column(Integer, nullable=False, default=0)
    price = Column(DECIMAL(10, 2))
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow)

class ItemCreate(BaseModel):
    name: str
    description: str = None
    quantity: int = 0
    price: float = None

#Create FastAPI app
app = FastAPI()

@app.get("/api/items")
def get_items():
    db = sessionLocal()
    items = db.query(Item).all()
    db.close()
    return {"items": items}

@app.post("/api/items")
def add_item(item: ItemCreate):
    db = sessionLocal()
    new_item = Item(
        name = item.name,
        description = item.description,
        quantity = item.quantity,
        price = item.price
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    db.close()
    return new_item

@app.get("/api/items/{item_id}")
def get_item(item_id: int):
    db = sessionLocal()
    item = db.query(Item).filter(Item.id == item_id).first()
    db.close()
    if item:
        return item
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@app.delete("/api/items/{item_id}")
def delete_item(item_id: int):
    db = sessionLocal()
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        db.close()
        raise HTTPException(status_code=404, detail = "Item not found")
    db.delete(item)
    db.commit()
    db.close()
    return {"message": "Item deleted successfully", "item": item}

