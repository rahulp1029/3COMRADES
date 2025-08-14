#!/usr/bin/env python3
"""
Test Script for Prescription Analyzer Feature
Tests both frontend and backend integration
"""

import requests
import time
import json

def test_prescription_analyzer():
    """Test the prescription analyzer API endpoint"""
    print("🧪 Testing Prescription Analyzer Feature")
    print("=" * 50)
    
    # Test backend health
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running")
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend connection failed: {e}")
        return False
    
    # Test prescription analyzer API
    try:
        test_data = {
            "user_id": "test-user-123",
            "image_data": "test-image-data-base64"
        }
        
        response = requests.post(
            "http://localhost:8000/api/analyze-prescription",
            json=test_data,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get("status") == "success" and "analysis" in result:
                print("✅ Prescription Analyzer API: PASSED")
                print(f"   Status: {result['status']}")
                
                # Check analysis structure
                analysis = result["analysis"]
                if "patient" in analysis and "medications" in analysis:
                    print("✅ Analysis structure: PASSED")
                    print(f"   Patient: {analysis['patient']['name']}")
                    print(f"   Medications: {len(analysis['medications'])} found")
                    print(f"   Instructions: {analysis['general_instructions'][:50]}...")
                else:
                    print("❌ Analysis structure: FAILED")
                    return False
            else:
                print("❌ Prescription Analyzer API: FAILED - Invalid response format")
                return False
        else:
            print(f"❌ Prescription Analyzer API: FAILED - Status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Prescription Analyzer API: FAILED - {e}")
        return False
    
    # Test frontend
    try:
        response = requests.get("http://localhost:5000", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend is running")
            
            # Check if prescription analyzer content is present
            content = response.text
            if "Prescription Analyzer" in content and "prescription-analyzer" in content:
                print("✅ Frontend Prescription Analyzer: PASSED")
                print("   Navigation button found")
                print("   Feature page content found")
            else:
                print("❌ Frontend Prescription Analyzer: FAILED - Content not found")
                return False
        else:
            print(f"❌ Frontend check failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Frontend connection failed: {e}")
        return False
    
    print("\n🎉 All tests passed! Prescription Analyzer is working correctly!")
    print("\n📱 You can now:")
    print("   1. Open http://localhost:5000 in your browser")
    print("   2. Click on 'Prescription Analyzer' in the navigation")
    print("   3. Upload a prescription image")
    print("   4. Get AI-powered analysis with medication details")
    
    return True

if __name__ == "__main__":
    print("🚀 HealthInsight AI - Prescription Analyzer Test")
    print("=" * 60)
    
    success = test_prescription_analyzer()
    
    if success:
        print("\n✅ Prescription Analyzer feature is fully functional!")
    else:
        print("\n❌ Some tests failed. Please check the server status.")
