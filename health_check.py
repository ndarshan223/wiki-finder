#!/usr/bin/env python3
"""Health check script for debugging container issues."""

import os
import sys
from pathlib import Path

def check_files():
    """Check if required files exist."""
    required_files = [
        'main.py', 'app.py', 'config.py',
        'core/__init__.py', 'ui/__init__.py'
    ]
    
    missing = []
    for file in required_files:
        if not Path(file).exists():
            missing.append(file)
    
    if missing:
        print(f"❌ Missing files: {missing}")
        return False
    
    print("✅ All required files present")
    return True

def check_data():
    """Check data directory."""
    data_dir = Path('data')
    if not data_dir.exists():
        print("❌ Data directory missing")
        return False
    
    csv_files = list(data_dir.glob('*.csv'))
    if not csv_files:
        print("❌ No CSV files in data directory")
        return False
    
    print(f"✅ Found {len(csv_files)} CSV files")
    return True

def check_models():
    """Check models directory."""
    models_dir = Path('models')
    if not models_dir.exists():
        print("❌ Models directory missing")
        return False
    
    print("✅ Models directory exists")
    return True

def check_imports():
    """Test critical imports."""
    try:
        import gradio
        import pandas
        import sentence_transformers
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Running health checks...")
    
    checks = [
        check_files(),
        check_data(), 
        check_models(),
        check_imports()
    ]
    
    if all(checks):
        print("✅ All health checks passed")
        sys.exit(0)
    else:
        print("❌ Some health checks failed")
        sys.exit(1)