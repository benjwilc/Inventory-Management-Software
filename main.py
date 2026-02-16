from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String, Text, DECIMAL, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

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

#Create FastAPI app
app = FastAPI()

@app.get("/api/items")
def get_items():
    db = sessionLocal()
    items = db.query(Item).all()
    db.close()
    return {"items": items}