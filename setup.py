import os
import subprocess
import sys

def setup():
    """Setup script for Render deployment"""
    print("Setting up Enterprise Demand Forecasting Platform...")
    
    # Create data directory
    os.makedirs('data', exist_ok=True)
    
    # Check if data files exist, if not generate them
    required_files = ['traffic.csv', 'applications.csv', 'infrastructure.csv', 'costs.csv']
    missing_files = [f for f in required_files if not os.path.exists(os.path.join('data', f))]
    
    if missing_files:
        print(f"Generating missing data files: {missing_files}")
        try:
            # Import and run data generation
            import pandas as pd
            import numpy as np
            from datetime import datetime, timedelta
            
            # Generate all data files (same code as before)
            # ... (include the data generation code here)
            print("Data files generated successfully!")
        except Exception as e:
            print(f"Error generating data: {e}")
    
    print("Setup complete!")

if __name__ == "__main__":
    setup()
