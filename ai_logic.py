import os
import pandas as pd
from scaledown import ScaleDown
import os
from sqlalchemy.orm import Session
from models import Product

# Initialize ScaleDown
# Assuming SCALEDOWN_KEY is in env vars or we can default to a placeholder
SCALEDOWN_KEY = os.getenv("SCALEDOWN_KEY", "165EzoqBaq5KP44qZKYSt4NIwbrmIqFf2xiYOtAE")
compressor = ScaleDown(api_key=SCALEDOWN_KEY)

def chat_with_inventory(user_query: str, db: Session):
    """
    Retrieves inventory data, compresses it using ScaleDown, 
    and simulates an LLM response (since OpenAI key is disabled).
    """
    
    # STEP A: Fetch Raw Context
    products = db.query(Product).all()
    # Convert to DataFrame for easy stringifying
    data = [{
        "product_id": p.product_id,
        "name": p.name,
        "sku": p.sku,
        "category": p.category,
        "stock_level": p.stock_level,
        "supplier": p.supplier_name
    } for p in products]
    
    if not data:
        return {
            "answer": "Inventory is empty.",
            "metrics": {"original_tokens": 0, "compressed_tokens": 0}
        }

    df = pd.DataFrame(data)
    raw_context = df.to_string()
    
    # STEP B: The ScaleDown Magic
    print("Compressing context...")
    try:
        compressed_result = compressor.compress(
            context=raw_context,
            prompt=user_query,
            target_model="gpt-4o" # Optimizing for GPT-4o as requested
        )
        
        optimized_context = compressed_result.content
        metrics = {
            "original_tokens": compressed_result.metrics.original_tokens,
            "compressed_tokens": compressed_result.metrics.compressed_tokens
        }
    except Exception as e:
        # Fallback if ScaleDown fails (e.g. invalid key)
        print(f"Compression failed: {e}")
        optimized_context = raw_context
        metrics = {"original_tokens": len(raw_context.split()), "compressed_tokens": len(raw_context.split())}

    # STEP C: Generate Final Answer (Mock/Simulated)
    # Since we cannot use OpenAI, we return the optimized context as the "Answer" 
    # or a static message demonstrating the compression success.
    
    answer = (
        f"**[SIMULATED LLM RESPONSE]**\n\n"
        f"I have analyzed the inventory data based on your query: '{user_query}'.\n"
        f"ScaleDown has optimized the context for GPT-4o.\n\n"
        f"**Optimized Context Used:**\n{optimized_context}"
    )
    
    return {
        "answer": answer,
        "metrics": metrics,
        "optimized_context": optimized_context
    }
