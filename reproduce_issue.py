import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, SessionLocal
from models import Product
import ai_logic

def debug_chat():
    db = SessionLocal()
    try:
        # Seed if empty (just to be sure, though main.py does it)
        if db.query(Product).count() == 0:
            print("Database empty, seeding...")
            products = [
                Product(name="Wireless Mouse", sku="WM-001", category="Electronics", stock_level=50, reorder_point=10, supplier_name="TechSupplies Inc"),
                Product(name="Mechanical Keyboard", sku="MK-002", category="Electronics", stock_level=15, reorder_point=5, supplier_name="KeyMaster"),
                Product(name="Office Chair", sku="OC-101", category="Furniture", stock_level=5, reorder_point=8, supplier_name="ComfySeats"),
                Product(name="Monitor 27in", sku="MN-202", category="Electronics", stock_level=20, reorder_point=5, supplier_name="VisualsCo"),
                Product(name="Ballpoint Pen Box", sku="BP-303", category="Stationery", stock_level=100, reorder_point=20, supplier_name="OfficeDepot"),
            ]
            db.add_all(products)
            db.commit()

        query = "What items are low on stock?"
        print(f"Query: {query}")
        result = ai_logic.chat_with_inventory(query, db)
        
        print("\n--- Result Answer ---")
        print(result["answer"])
        print("\n--- Metrics ---")
        print(result["metrics"])
        print("\n--- Optimized Context (First 500 chars) ---")
        print(result["optimized_context"][:500])
        
    finally:
        db.close()

if __name__ == "__main__":
    debug_chat()
