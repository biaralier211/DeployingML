#!/usr/bin/env python3
"""
Test script for KMart ML API deployment
"""

import requests
import json
import time

def test_api_endpoints(base_url):
    """Test all API endpoints"""
    print(f"Testing API at: {base_url}")
    
    # Test 1: Health check
    print("\n1. Testing health check...")
    try:
        response = requests.get(f"{base_url}/")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 2: Get recommendations
    print("\n2. Testing recommendations...")
    try:
        data = {"user_id": "test_user", "num_recommendations": 3}
        response = requests.post(f"{base_url}/recommendations", json=data)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            recommendations = response.json()
            print(f"   Found {len(recommendations)} recommendations")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 3: Search products
    print("\n3. Testing search...")
    try:
        data = {"query": "headphones", "num_results": 3}
        response = requests.post(f"{base_url}/search", json=data)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            results = response.json()
            print(f"   Found {len(results)} search results")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 4: Get trending products
    print("\n4. Testing trending products...")
    try:
        response = requests.get(f"{base_url}/trending?days=7&limit=3")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            trending = response.json()
            print(f"   Found {len(trending)} trending products")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 5: Get product details
    print("\n5. Testing product details...")
    try:
        response = requests.get(f"{base_url}/products/prod_001")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            product = response.json()
            print(f"   Product: {product.get('name', 'Unknown')}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 6: Track interaction
    print("\n6. Testing interaction tracking...")
    try:
        data = {
            "user_id": "test_user",
            "product_id": "prod_001",
            "interaction_type": "product_view",
            "timestamp": "2024-01-01T12:00:00Z"
        }
        response = requests.post(f"{base_url}/interactions/product-view", json=data)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   Interaction tracked: {result.get('message', 'Success')}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")

if __name__ == "__main__":
    # Test local deployment
    print("Testing local deployment...")
    test_api_endpoints("http://localhost:8000")
    
    # Uncomment and update with your Render URL when deployed
    # print("\n" + "="*50)
    # print("Testing Render deployment...")
    # test_api_endpoints("https://your-service-name.onrender.com") 