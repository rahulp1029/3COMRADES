#!/usr/bin/env python3
"""
Comprehensive Integration Test for HealthInsight AI
Tests both frontend and backend connectivity and functionality
"""

import requests
import time
import json
from datetime import datetime

def test_backend_health():
    """Test backend health endpoint"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend health check: PASSED")
            return True
        else:
            print(f"❌ Backend health check: FAILED - Status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend health check: FAILED - {e}")
        return False

def test_frontend_health():
    """Test frontend health"""
    try:
        response = requests.get("http://localhost:5000", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend health check: PASSED")
            return True
        else:
            print(f"❌ Frontend health check: FAILED - Status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Frontend health check: FAILED - {e}")
        return False

def test_symptom_checker():
    """Test symptom checker API"""
    try:
        data = {
            "symptoms": "headache, fever, fatigue",
            "user_id": "test-user-123"
        }
        response = requests.post(
            "http://localhost:8000/api/diagnose",
            json=data,
            timeout=10
        )
        if response.status_code == 200:
            result = response.json()
            if "diagnosis" in result and "treatment" in result:
                print("✅ Symptom checker API: PASSED")
                print(f"   Diagnosis: {result['diagnosis']}")
                return True
            else:
                print("❌ Symptom checker API: FAILED - Invalid response format")
                return False
        else:
            print(f"❌ Symptom checker API: FAILED - Status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Symptom checker API: FAILED - {e}")
        return False

def test_skin_analyzer():
    """Test skin analyzer API"""
    try:
        # Create a dummy base64 image data
        dummy_image = "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAYEBQYFBAYGBQYHBwYIChAKCgkJChQODwwQFxQYGBcUFhYaHSUfGhsjHBYWICwgIyYnKSopGR8tMC0oMCUoKSj/2wBDAQcHBwoIChMKChMoGhYaKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCj/wAARCAABAAEDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAv/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFQEBAQAAAAAAAAAAAAAAAAAAAAX/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwCdABmX/9k="
        
        data = {
            "user_id": "test-user-123",
            "image_data": dummy_image
        }
        response = requests.post(
            "http://localhost:8000/api/analyze-skin-condition",
            json=data,
            timeout=10
        )
        if response.status_code == 200:
            result = response.json()
            if "title" in result and "description" in result:
                print("✅ Skin analyzer API: PASSED")
                print(f"   Analysis: {result['title']}")
                return True
            else:
                print("❌ Skin analyzer API: FAILED - Invalid response format")
                return False
        else:
            print(f"❌ Skin analyzer API: FAILED - Status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Skin analyzer API: FAILED - {e}")
        return False

def test_doctor_chat():
    """Test doctor chat API"""
    try:
        data = {
            "message": "I have been feeling tired lately",
            "user_id": "test-user-123"
        }
        response = requests.post(
            "http://localhost:8000/api/chat-with-doctor",
            json=data,
            timeout=10
        )
        if response.status_code == 200:
            result = response.json()
            if "response" in result:
                print("✅ Doctor chat API: PASSED")
                print(f"   Response: {result['response'][:50]}...")
                return True
            else:
                print("❌ Doctor chat API: FAILED - Invalid response format")
                return False
        else:
            print(f"❌ Doctor chat API: FAILED - Status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Doctor chat API: FAILED - {e}")
        return False

def test_vital_signs():
    """Test vital signs API"""
    try:
        data = {
            "user_id": "test-user-123",
            "heart_rate": 75.0,
            "blood_pressure_systolic": 120,
            "blood_pressure_diastolic": 80,
            "temperature": 98.6,
            "oxygen_saturation": 98.0,
            "respiratory_rate": 16.0
        }
        response = requests.post(
            "http://localhost:8000/api/vital-signs",
            json=data,
            timeout=10
        )
        if response.status_code == 200:
            result = response.json()
            if "status" in result and "analysis" in result:
                print("✅ Vital signs API: PASSED")
                print(f"   Status: {result['status']}")
                return True
            else:
                print("❌ Vital signs API: FAILED - Invalid response format")
                return False
        else:
            print(f"❌ Vital signs API: FAILED - Status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Vital signs API: FAILED - {e}")
        return False

def test_dashboard():
    """Test dashboard API"""
    try:
        response = requests.get(
            "http://localhost:8000/api/dashboard/test-user-123",
            timeout=10
        )
        if response.status_code == 200:
            result = response.json()
            if "status" in result and "data" in result:
                print("✅ Dashboard API: PASSED")
                print(f"   Summary: {result['summary']}")
                return True
            else:
                print("❌ Dashboard API: FAILED - Invalid response format")
                return False
        else:
            print(f"❌ Dashboard API: FAILED - Status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Dashboard API: FAILED - {e}")
        return False

def main():
    """Run all integration tests"""
    print("🚀 HealthInsight AI - Full Integration Test")
    print("=" * 50)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tests = [
        ("Backend Health", test_backend_health),
        ("Frontend Health", test_frontend_health),
        ("Symptom Checker", test_symptom_checker),
        ("Skin Analyzer", test_skin_analyzer),
        ("Doctor Chat", test_doctor_chat),
        ("Vital Signs", test_vital_signs),
        ("Dashboard", test_dashboard)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"Testing {test_name}...")
        if test_func():
            passed += 1
        print()
        time.sleep(1)  # Small delay between tests
    
    print("=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your HealthInsight AI is fully integrated and working!")
        print("\n📱 You can now access:")
        print("   Frontend: http://localhost:5000")
        print("   Backend API: http://localhost:8000")
        print("   API Docs: http://localhost:8000/docs")
    else:
        print("⚠️  Some tests failed. Please check the server status and try again.")
    
    return passed == total

if __name__ == "__main__":
    main()
