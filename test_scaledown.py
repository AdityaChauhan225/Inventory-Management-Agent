"""
Test ScaleDown API directly to debug the issue
"""
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Get API key from environment
api_key = os.getenv('SCALEDOWN_API_KEY')

print(f"API Key loaded: {'Yes' if api_key else 'No'}")
if api_key:
    print(f"API Key (first 10 chars): {api_key[:10]}...")

# Test payload - exact format from documentation
url = "https://api.scaledown.xyz/compress/raw/"

headers = {
    'x-api-key': api_key,
    'Content-Type': 'application/json'
}

# Simple test payload
payload = {
    "context": "You are analyzing inventory data for a retail store.",
    "prompt": "Product A has 50 units in stock, selling 10 units per day. Product B has 20 units in stock, selling 5 units per day. Which product needs restocking first?",
    "scaledown": {
        "rate": "auto"
    }
}

print("\n" + "="*50)
print("Testing ScaleDown API...")
print("="*50)
print(f"\nURL: {url}")
print(f"\nPayload:")
print(json.dumps(payload, indent=2))

try:
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    
    print(f"\nResponse Status: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    print(f"\nResponse Body:")
    print(json.dumps(response.json(), indent=2))
    
except Exception as e:
    print(f"\nError: {str(e)}")
    if hasattr(e, 'response'):
        print(f"Response text: {e.response.text}")
