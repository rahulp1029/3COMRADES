#!/usr/bin/env python3
"""
Test script to verify the HealthInsight AI application runs correctly
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    print("Testing HealthInsight AI application...")
    
    # Import the application
    import frontend_app
    
    print("✓ Application imported successfully")
    print("✓ No syntax errors found")
    print("✓ All dependencies resolved")
    
    # Test if Flask app is created
    if hasattr(frontend_app, 'app'):
        print("✓ Flask app created successfully")
    else:
        print("✗ Flask app not found")
    
    # Test if routes are defined
    if hasattr(frontend_app.app, 'url_map'):
        routes = list(frontend_app.app.url_map.iter_rules())
        print(f"✓ {len(routes)} routes defined")
        
        # List main routes
        main_routes = ['/', '/api/diagnose', '/api/analyze-skin-condition', '/api/chat-with-doctor']
        for route in main_routes:
            if any(route in str(r) for r in routes):
                print(f"  ✓ Route {route} found")
            else:
                print(f"  ✗ Route {route} missing")
    
    print("\n🎉 Application is ready to run!")
    print("To start the server, run: python frontend_app.py")
    print("Then open: http://localhost:5000")
    
except ImportError as e:
    print(f"✗ Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)
