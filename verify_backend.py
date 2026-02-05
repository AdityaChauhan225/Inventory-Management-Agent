import requests
import time
import sys
import subprocess

def test_backend():
    print("Testing Backend API...")
    try:
        # Check if root endpoint works
        response = requests.get("http://localhost:8000/")
        if response.status_code == 200:
            print("✅ Backend is running and reachable.")
        else:
            print(f"❌ Backend returned status {response.status_code}")
            return False

        # Check products info
        response = requests.get("http://localhost:8000/api/products")
        if response.status_code == 200:
            products = response.json()
            print(f"✅ Product Endpoint working. Found {len(products)} products.")
        else:
            print("❌ Failed to fetch products")
            return False

        # Check Chat (this triggers ScaleDown logic)
        payload = {"query": "What items are low on stock?"}
        print("Testing AI/Compression endpoint (Simulated mode)...")
        response = requests.post("http://localhost:8000/api/ask", json=payload)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Chat Endpoint working.")
            print(f"   Answer: {data.get('answer')[:50]}...")
            metrics = data.get('metrics', {})
            print(f"   Metrics: Original={metrics.get('original_tokens')}, Compressed={metrics.get('compressed_tokens')}")
        else:
            print(f"❌ Chat Endpoint Failed: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to localhost:8000. Is the server running?")
        return False

    return True

if __name__ == "__main__":
    if not test_backend():
        sys.exit(1)
