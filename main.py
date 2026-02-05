from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List, Optional

from database import engine, get_db, Base
from models import Product, Transaction
import models
import ai_logic

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Allow CORS for React Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, set this to the frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Seed data if empty
def seed_db():
    db = next(get_db())
    if db.query(Product).count() == 0:
        products = [
            Product(name="Wireless Mouse", sku="WM-001", category="Electronics", stock_level=50, reorder_point=10, supplier_name="TechSupplies Inc"),
            Product(name="Mechanical Keyboard", sku="MK-002", category="Electronics", stock_level=15, reorder_point=5, supplier_name="KeyMaster"),
            Product(name="Office Chair", sku="OC-101", category="Furniture", stock_level=5, reorder_point=8, supplier_name="ComfySeats"),
            Product(name="Monitor 27in", sku="MN-202", category="Electronics", stock_level=20, reorder_point=5, supplier_name="VisualsCo"),
            Product(name="Ballpoint Pen Box", sku="BP-303", category="Stationery", stock_level=100, reorder_point=20, supplier_name="OfficeDepot"),
        ]
        db.add_all(products)
        db.commit()
    db.close()

seed_db()

class ChatRequest(BaseModel):
    query: str

class ProductResponse(BaseModel):
    product_id: int
    name: str
    sku: str
    category: str
    stock_level: int
    reorder_point: int
    supplier_name: str

    class Config:
        orm_mode = True

@app.get("/")
def read_root():
    return {"message": "Smart Inventory Agent API is running"}

@app.get("/api/products", response_model=List[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

@app.post("/api/ask")
async def ask_inventory(request: ChatRequest, db: Session = Depends(get_db)):
    try:
        # Call the logic from ai_logic.py
        result = ai_logic.chat_with_inventory(request.query, db)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
