#!/usr/bin/env python3
import os
import sys
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

def load_env():
    """Load .env file and verify required variables"""
    env_path = backend_dir.parent / '.env'
    
    if not env_path.exists():
        print(f"❌ .env file not found at: {env_path}")
        return False
    
    # Load environment variables
    with open(env_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and ('=' in line or ':' in line):
                key, value = line.split('=' if '=' in line else ':', 1)
                os.environ[key.strip()] = value.strip().strip('\'"')
    
    # Verify required variables
    required = ['REDDIT_CLIENT_ID', 'REDDIT_CLIENT_SECRET']
    missing = [var for var in required if not os.getenv(var)]
    
    if missing:
        print(f"❌ Missing environment variables: {missing}")
        return False
    
    print("✅ Environment loaded successfully")
    return True

if __name__ == '__main__':
    print("🚀 VueLites Backend • http://localhost:5001")
    
    if not load_env():
        sys.exit(1)
    
    try:
        from flask_api.main.app import app
        app.run(debug=True, host='0.0.0.0', port=5001)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)