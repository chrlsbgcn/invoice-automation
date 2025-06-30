#!/usr/bin/env python3
"""
Simple startup script for the Invoice Data Extractor Web Application
"""

import os
import sys
from app import app

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 Invoice Data Extractor Web Application")
    print("=" * 60)
    print("Starting the web server...")
    print("📱 Open your browser and go to: http://localhost:5000")
    print("🔄 Press Ctrl+C to stop the server")
    print("=" * 60)
    
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Server stopped. Goodbye!")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1) 