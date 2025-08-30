#!/usr/bin/env python3
"""
Project Explorer Pro - Startup Script
Launch the production-ready application
"""

import subprocess
import sys
import os

def main():
    """Start the Project Explorer Pro application"""
    print("🚀 Starting Project Explorer Pro...")
    print("=" * 50)
    
    # Check if required packages are installed
    try:
        import streamlit
        import pandas
        import plotly
        import sklearn
        print("✅ All required packages are installed")
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("Please run: pip install -r requirements.txt")
        return
    
    # Check if the production app file exists
    app_file = "streamlit_app_production.py"
    if not os.path.exists(app_file):
        print(f"❌ Production app file not found: {app_file}")
        return
    
    # Check if the dataset exists
    dataset_path = r"C:\Users\excalibur\Desktop\Company\Sundai\project-explorer-3d\src\integrations\supabase\projects_dataset\sundai_projects_umap.csv"
    if not os.path.exists(dataset_path):
        print(f"⚠️  Dataset not found at: {dataset_path}")
        print("The app will still run but may not have data to analyze")
    
    print("🌐 Launching Project Explorer Pro...")
    print("📱 Access the app at: http://localhost:8512")
    print("🛑 Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        # Start the Streamlit app
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "streamlit_app_production.py", 
            "--server.port", "8512",
            "--server.headless", "true"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

if __name__ == "__main__":
    main()
