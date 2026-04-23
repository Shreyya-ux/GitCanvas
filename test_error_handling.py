#!/usr/bin/env python3
"""
Test script to verify proper error handling in API endpoints.

This script tests:
1. Non-existent user returns error SVG with 502 status
2. Invalid data handling returns proper error messages
3. Actions endpoint requires authentication
4. Error responses are properly cached
"""

import requests
import json
from datetime import datetime

# API base URL
API_BASE = "http://localhost:8000"

def test_nonexistent_user():
    """Test API response for non-existent username"""
    print("\n" + "="*60)
    print("TEST 1: Non-existent User Handling")
    print("="*60)
    
    username = "nonexistentuser_" + datetime.now().strftime("%Y%m%d%H%M%S")
    endpoints = [
        "/api/stats",
        "/api/languages",
        "/api/contributions",
        "/api/trophy",
        "/api/streak",
        "/api/repos"
    ]
    
    for endpoint in endpoints:
        try:
            url = f"{API_BASE}{endpoint}?username={username}"
            response = requests.get(url, timeout=10)
            
            # Check status code
            if response.status_code == 502:
                print(f"✓ {endpoint}: Correctly returns 502 Bad Gateway")
                # Check for error header
                if response.headers.get("X-Error"):
                    print(f"  ✓ Error header present: {response.headers.get('X-Error')}")
                # Check content type is SVG
                if "image/svg+xml" in response.headers.get("Content-Type", ""):
                    print(f"  ✓ Returns SVG error card")
                else:
                    print(f"  ✗ Wrong content type: {response.headers.get('Content-Type')}")
            elif response.status_code == 200:
                print(f"✗ {endpoint}: Returns 200 (should be 502) - FALLBACK TO MOCK DATA DETECTED")
            else:
                print(f"? {endpoint}: Returns {response.status_code}")
                
        except Exception as e:
            print(f"✗ {endpoint}: Error - {e}")


def test_actions_without_auth():
    """Test Actions endpoint requires authentication"""
    print("\n" + "="*60)
    print("TEST 2: GitHub Actions Authentication")
    print("="*60)
    
    url = f"{API_BASE}/api/actions?username=torvalds"
    
    try:
        # Without token
        response = requests.get(url, timeout=10)
        
        if response.status_code == 401:
            print(f"✓ Actions endpoint correctly returns 401 without token")
            if "Unauthorized" in response.text or "authentication" in response.text.lower():
                print(f"  ✓ Error message mentions authentication")
        elif response.status_code == 200:
            print(f"✗ Actions endpoint returns 200 (should require auth) - MOCK DATA RETURNED")
        else:
            print(f"? Actions endpoint returns {response.status_code}")
            
    except Exception as e:
        print(f"✗ Error: {e}")


def test_actions_with_auth():
    """Test Actions endpoint with authentication"""
    print("\n" + "="*60)
    print("TEST 3: GitHub Actions with Authentication")
    print("="*60)
    
    # Using a non-existent user with token to test error handling
    url = f"{API_BASE}/api/actions?username=nonexistentuser_test"
    
    # Use a fake token to test
    headers = {"Authorization": "Bearer fake_token_for_testing"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 502:
            print(f"✓ Actions endpoint with invalid user returns 502")
            if response.headers.get("X-Error"):
                print(f"  ✓ Error header present: {response.headers.get('X-Error')}")
        elif response.status_code == 200:
            print(f"✗ Actions endpoint returns 200 (should return error for nonexistent user)")
        else:
            print(f"? Actions endpoint returns {response.status_code}")
            
    except Exception as e:
        print(f"✗ Error: {e}")


def test_error_response_format():
    """Test that error responses are valid SVG"""
    print("\n" + "="*60)
    print("TEST 4: Error Response Format")
    print("="*60)
    
    url = f"{API_BASE}/api/stats?username=invalid_user_12345"
    
    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code == 502 and "image/svg+xml" in response.headers.get("Content-Type", ""):
            content = response.text
            
            # Check if it's valid SVG
            if content.startswith("<svg") and "</svg>" in content:
                print(f"✓ Error response is valid SVG")
                
                # Check for error indicators
                if "Error" in content or "error" in content.lower():
                    print(f"  ✓ SVG contains error message")
                if "!" in content or "exclamation" in content.lower():
                    print(f"  ✓ SVG contains error icon/indicator")
            else:
                print(f"✗ Response is not valid SVG")
                print(f"  First 200 chars: {content[:200]}")
        else:
            print(f"? Status {response.status_code}, Content-Type: {response.headers.get('Content-Type')}")
            
    except Exception as e:
        print(f"✗ Error: {e}")


def test_cache_not_caching_errors():
    """Test that error responses are not cached"""
    print("\n" + "="*60)
    print("TEST 5: Error Response Caching")
    print("="*60)
    
    url = f"{API_BASE}/api/stats?username=nonexistent_user_cache_test"
    
    try:
        response1 = requests.get(url, timeout=10)
        cache_control_1 = response1.headers.get("Cache-Control")
        
        response2 = requests.get(url, timeout=10)
        cache_control_2 = response2.headers.get("Cache-Control")
        
        if "no-cache" in cache_control_1 or "no-store" in cache_control_1:
            print(f"✓ Error responses are not cached")
            print(f"  Cache-Control: {cache_control_1}")
        else:
            print(f"✗ Error responses may be cached")
            print(f"  Cache-Control: {cache_control_1}")
            
    except Exception as e:
        print(f"✗ Error: {e}")


def test_valid_user_returns_200():
    """Test that valid users still return 200 OK"""
    print("\n" + "="*60)
    print("TEST 6: Valid User Returns Success")
    print("="*60)
    
    # Using a well-known GitHub user
    url = f"{API_BASE}/api/stats?username=torvalds"
    
    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            print(f"✓ Valid user returns 200 OK")
            if "image/svg+xml" in response.headers.get("Content-Type", ""):
                print(f"  ✓ Returns SVG content")
        else:
            print(f"? Valid user returns {response.status_code}")
            if response.status_code == 502:
                print(f"  ✗ GitHub API might be rate-limited or unavailable")
            
    except Exception as e:
        print(f"✗ Error: {e}")


if __name__ == "__main__":
    print("\n🧪 GitCanvas Error Handling Test Suite")
    print("Testing API error responses and exception handling")
    
    try:
        # Quick health check
        response = requests.get(f"{API_BASE}/", timeout=5)
        if response.status_code == 200:
            print(f"✓ API is running at {API_BASE}")
        else:
            print(f"✗ API health check failed: {response.status_code}")
            exit(1)
    except Exception as e:
        print(f"✗ Cannot reach API at {API_BASE}: {e}")
        print("Make sure the API is running: uvicorn api.main:app --reload")
        exit(1)
    
    # Run tests
    test_nonexistent_user()
    test_actions_without_auth()
    test_actions_with_auth()
    test_error_response_format()
    test_cache_not_caching_errors()
    test_valid_user_returns_200()
    
    print("\n" + "="*60)
    print("✅ Test suite complete!")
    print("="*60 + "\n")
