#!/usr/bin/env python3
"""
Test script to verify the FastAPI backend is working
"""

import requests
import json
import time

def test_fastapi_backend():
    base_url = "http://localhost:8000"
    
    print("🧪 Testing HealthInsight AI FastAPI Backend...")
    
    try:
        # Test health endpoint
        print("1. Testing health endpoint...")
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ Health endpoint working")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            return False
        
        # Test root endpoint
        print("\n2. Testing root endpoint...")
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ Root endpoint working")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
            return False
        
        # Test symptom diagnosis
        print("\n3. Testing symptom diagnosis...")
        diagnosis_data = {
            "symptoms": "I have a headache and fever",
            "user_id": "test_user_123"
        }
        response = requests.post(
            f"{base_url}/api/diagnose",
            json=diagnosis_data,
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            print("✅ Symptom diagnosis working")
            result = response.json()
            print(f"   Diagnosis: {result.get('diagnosis', 'N/A')}")
            print(f"   Treatment: {result.get('treatment', [])}")
        else:
            print(f"❌ Symptom diagnosis failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
        
        # Test doctor chat
        print("\n4. Testing doctor chat...")
        chat_data = {
            "message": "What should I do for a cold?",
            "user_id": "test_user_123"
        }
        response = requests.post(
            f"{base_url}/api/chat-with-doctor",
            json=chat_data,
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            print("✅ Doctor chat working")
            result = response.json()
            print(f"   Response: {result.get('response', 'N/A')[:100]}...")
        else:
            print(f"❌ Doctor chat failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
        
        # Test vital signs
        print("\n5. Testing vital signs...")
        vital_data = {
            "user_id": "test_user_123",
            "heart_rate": 75,
            "blood_pressure_systolic": 120,
            "blood_pressure_diastolic": 80,
            "temperature": 98.6,
            "oxygen_saturation": 98,
            "respiratory_rate": 16
        }
        response = requests.post(
            f"{base_url}/api/vital-signs",
            json=vital_data,
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            print("✅ Vital signs working")
            result = response.json()
            print(f"   Status: {result.get('analysis', {}).get('status', 'N/A')}")
        else:
            print(f"❌ Vital signs failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
        
        # Test dashboard
        print("\n6. Testing dashboard...")
        response = requests.get(f"{base_url}/api/dashboard/test_user_123")
        if response.status_code == 200:
            print("✅ Dashboard working")
            result = response.json()
            print(f"   Summary: {result.get('summary', {})}")
        else:
            print(f"❌ Dashboard failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
        
        print("\n🎉 All FastAPI backend tests passed!")
        print("📚 API Documentation: http://localhost:8000/docs")
        print("🔍 Alternative docs: http://localhost:8000/redoc")
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to FastAPI backend")
        print("   Make sure the backend is running on http://localhost:8000")
        return False
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

if __name__ == "__main__":
    # Wait a moment for the server to start
    print("⏳ Waiting for FastAPI server to start...")
    time.sleep(3)
    
    success = test_fastapi_backend()
    if success:
        print("\n🚀 FastAPI backend is ready to use!")
    else:
        print("\n💥 FastAPI backend tests failed!")
