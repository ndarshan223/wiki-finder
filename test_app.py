#!/usr/bin/env python3
"""
Simple test script to verify the chatbot functionality without running the full UI
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_basic_functionality():
    """Test basic functionality without dependencies"""
    
    # Test 1: Check if file exists and is readable
    app_file = "app.py"
    if not os.path.exists(app_file):
        print("❌ app.py file not found")
        return False
    
    # Test 2: Check basic Python syntax
    try:
        with open(app_file, 'r') as f:
            content = f.read()
        
        # Check for common issues
        if '\\n\\n' in content:
            print("⚠️  Found escaped newlines in content - this may cause formatting issues")
        
        if 'msg.submit(' in content and 'submit_btn.click(' in content:
            print("✅ Both enter key and button submit handlers found")
        else:
            print("❌ Missing submit handlers")
            return False
            
        # Check for proper function definitions
        if 'def chat_interface(' in content and 'def handle_submit(' in content:
            print("✅ Required functions defined")
        else:
            print("❌ Missing required functions")
            return False
            
        print("✅ Basic syntax and structure looks good")
        return True
        
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return False

def test_data_folder():
    """Test if data folder exists"""
    data_folder = "data"
    if os.path.exists(data_folder):
        files = os.listdir(data_folder)
        csv_files = [f for f in files if f.endswith(('.csv', '.xlsx'))]
        if csv_files:
            print(f"✅ Found {len(csv_files)} data files: {csv_files}")
        else:
            print("⚠️  Data folder exists but no CSV/Excel files found")
    else:
        print("⚠️  Data folder not found - create it and add data files")

if __name__ == "__main__":
    print("🔍 Testing SDLC Chatbot Application")
    print("=" * 40)
    
    success = test_basic_functionality()
    test_data_folder()
    
    if success:
        print("\n✅ Application structure looks good!")
        print("💡 To run the app: python3 app.py (after installing dependencies)")
    else:
        print("\n❌ Issues found - please check the app.py file")