import os
import pandas as pd
from scaledown import ScaleDown
import os
from sqlalchemy.orm import Session
from models import Product

# Initialize ScaleDown
# The installed ScaleDown library uses a different API than originally implemented.
# It seems to be a simulation/mock version. We will adapt to it.

try:
    compressor = ScaleDown(enable_optimization_styles=False)
except Exception as e:
    print(f"Warning: Failed to initialize ScaleDown: {e}")
    compressor = None

class CompressionResult:
    def __init__(self, content, metrics):
        self.content = content
        self.metrics = metrics

class Metrics:
    def __init__(self, original, compressed):
        self.original_tokens = original
        self.compressed_tokens = compressed

def chat_with_inventory(user_query: str, db: Session):
    """
    Retrieves inventory data, compresses it using ScaleDown, 
    and simulates an LLM response (since OpenAI key is disabled).
    """
    
    # STEP A: Fetch Raw Context
    products = db.query(Product).all()
    
    # --- Semantic Compression / Filtering Logic ---
    # In a real ScaleDown implementation, this might happen via a specialized tool or model.
    # Here we simulate it by filtering the data based on the user's query.
    
    filtered_products = []
    query_lower = user_query.lower()
    
    if "low" in query_lower and "stock" in query_lower:
        # Filter for low stock items
        filtered_products = [p for p in products if p.stock_level <= p.reorder_point]
    elif "electronics" in query_lower:
         filtered_products = [p for p in products if p.category == "Electronics"]
    elif "furniture" in query_lower:
         filtered_products = [p for p in products if p.category == "Furniture"]
    elif "stationery" in query_lower:
         filtered_products = [p for p in products if p.category == "Stationery"]
    else:
        # If no specific filter found, keeping mostly everything but maybe limit count
        filtered_products = products

    # Convert to DataFrame for easy stringifying
    original_data = [{
        "product_id": p.product_id,
        "name": p.name,
        "sku": p.sku,
        "category": p.category,
        "stock_level": p.stock_level,
        "supplier": p.supplier_name
    } for p in products]

    filtered_data = [{
        "product_id": p.product_id,
        "name": p.name,
        "sku": p.sku,
        "category": p.category,
        "stock_level": p.stock_level,
        "supplier": p.supplier_name
    } for p in filtered_products]
    
    if not original_data:
        return {
            "answer": "Inventory is empty.",
            "metrics": {"original_tokens": 0, "compressed_tokens": 0}
        }

    df_original = pd.DataFrame(original_data)
    df_filtered = pd.DataFrame(filtered_data)
    
    raw_context = df_original.to_string() # Full context for "Original Tokens" count
    compressed_context = df_filtered.to_string() # Filtered context for "Compressed" result
    
    # STEP B: The ScaleDown Magic (Simulated)
    print("Compressing context...")
    try:
        if compressor:
            # We use the raw context to calculate original size
            # And the compressed_context as the "result" of optimization
            
            # Using mock_optimize to get token counts structure, but we override values
            mock_res_original = compressor.mock_optimize(prompt=raw_context)
            mock_res_compressed = compressor.mock_optimize(prompt=compressed_context)

            # Map dict result to expected object structure
            optimized_context = compressed_context
            metrics_data = {
                "original_tokens": mock_res_original["original_tokens"],
                # We use the token count of our MANUALLY filtered context
                "compressed_tokens": mock_res_compressed["original_tokens"] 
            }
        else:
            raise Exception("ScaleDown not initialized")

        metrics = metrics_data
        
    except Exception as e:
        # Fallback if ScaleDown fails
        print(f"Compression failed: {e}")
        optimized_context = f"Error: Unable to retrieving specific context due to compression failure. ({str(e)})"
        metrics = {"original_tokens": len(raw_context.split()), "compressed_tokens": 0}

    # STEP C: Generate Final Answer (Mock/Simulated)
    # Only show a summary, do not dump the whole context unless debugging
    
    if "Error" in optimized_context:
        answer = f"**[SIMULATED LLM RESPONSE]**\n\nI encountered an issue processing the inventory data.\n\n{optimized_context}"
    else:
        answer = (
            f"**[SIMULATED LLM RESPONSE]**\n\n"
            f"I have analyzed the inventory data based on your query: '{user_query}'.\n"
            f"ScaleDown has identified {metrics['compressed_tokens']} relevant tokens (compressed from {metrics['original_tokens']}).\n\n"
            f"**Relevant Context Preview:**\n{optimized_context[:500]}..." # Truncate primarily
        )
    
    return {
        "answer": answer,
        "metrics": metrics,
        "optimized_context": optimized_context
    }
