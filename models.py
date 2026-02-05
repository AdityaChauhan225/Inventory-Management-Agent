from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from database import Base
import enum
from datetime import datetime

class TransactionType(enum.Enum):
    IN = "IN"
    OUT = "OUT"

class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    sku = Column(String, unique=True, index=True)
    category = Column(String, index=True)
    stock_level = Column(Integer, default=0)
    reorder_point = Column(Integer, default=10)
    supplier_name = Column(String)

    transactions = relationship("Transaction", back_populates="product")

class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.product_id"))
    type = Column(String) # Storing as string for simplicity with SQLite
    quantity = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)

    product = relationship("Product", back_populates="transactions")
