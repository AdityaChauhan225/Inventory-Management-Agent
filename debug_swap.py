"""
Diagnostic script - Test if Context is what gets compressed
"""
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('SCALEDOWN_API_KEY')
url = "https://api.scaledown.xyz/compress/raw/"
headers = {
    'x-api-key': api_key,
    'Content-Type': 'application/json'
}

# SWAPPED: Big data in context, query in prompt
payload = {
    "context": "Item 1: Widget A, Stock: 100\nItem 2: Widget B, Stock: 5\nItem 3: Widget C, Stock: 200",
    "prompt": "Which items need restocking?",
    "scaledown": {
        "rate": "auto"
    }
}

try:
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    
    with open('response_debug_swap.txt', 'w') as f:
        f.write(f"Status: {response.status_code}\n")
        f.write("\n--- RAW RESPONSE ---\n")
        f.write(response.text)
        
    print("Response written to response_debug_swap.txt")

except Exception as e:
    print(f"Exception: {e}")
