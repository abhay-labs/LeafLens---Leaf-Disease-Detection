"""
API Test Script for Leaf Disease Detection
==========================================

This script tests the FastAPI endpoints to ensure they work correctly.
"""

import requests
import json
from pathlib import Path

API_URL = "http://localhost:8000"  # Change if your API runs elsewhere
TEST_IMAGE_PATH = "Media/brown-spot-4 (1).jpg"  # Make sure this exists


def test_root_endpoint():
    """Test the root endpoint"""
    try:
        response = requests.get(f"{API_URL}/")
        if response.status_code == 200:
            print("✓ Root endpoint working!")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"✗ Root endpoint failed with status {response.status_code}")
    except Exception as e:
        print(f"Error testing root endpoint: {str(e)}")


def test_file_upload_endpoint():
    """Test the disease detection API endpoint (file upload)"""
    if not Path(TEST_IMAGE_PATH).exists():
        print(f"Error: Test image not found at {TEST_IMAGE_PATH}")
        return

    try:
        print(f"Sending image file to {API_URL}/disease-detection-file...")
        with open(TEST_IMAGE_PATH, "rb") as img_file:
            files = {"file": (Path(TEST_IMAGE_PATH).name, img_file, "image/jpeg")}
            response = requests.post(f"{API_URL}/disease-detection-file", files=files)

        if response.status_code == 200:
            result = response.json()
            print("✓ File upload API request successful!")
            print("\nResponse:")
            print(json.dumps(result, indent=2))
        else:
            print(f"✗ File upload API request failed with status {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error (file upload endpoint): {str(e)}")


if __name__ == "__main__":
    print("Leaf Disease Detection API Test")
    print("=" * 40)

    print("\n1. Testing root endpoint...")
    test_root_endpoint()

    print("\n2. Testing disease detection endpoint...")
    test_file_upload_endpoint()
