import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_data():
    """Generate all data files for the application"""
    
    print("Generating data for deployment...")
    os.makedirs('data', exist_ok=True)
    
    # Generate dates
    start_date = datetime(2023, 1, 1)
    dates = [start_date + timedelta(days=i) for i in range(365)]
    
    # Traffic data
    print("Creating traffic.csv...")
    np.random.seed(42)
    df = pd.DataFrame({
        'Date': dates,
        'Requests': np.random.randint(80000, 150000, 365),
        'UniqueUsers': np.random.randint(4000, 8000, 365),
        'PageViews': np.random.randint(40000, 70000, 365),
        'PeakRequests': np.random.randint(120000, 200000, 365),
        'ResponseTime': np.random.randint(50, 200, 365)
    })
    df.to_csv('data/traffic.csv', index=False)
    print("✅ traffic.csv created")
    
    # Applications data
    print("Creating applications.csv...")
    np.random.seed(123)
    df = pd.DataFrame({
        'Date': dates,
        'Applications': np.random.randint(300, 700, 365),
        'Interviews': np.random.randint(60, 140, 365),
        'Offers': np.random.randint(20, 60, 365),
        'Hires': np.random.randint(10, 50, 365),
        'Placements': np.random.randint(5, 45, 365)
    })
    df.to_csv('data/applications.csv', index=False)
    print("✅ applications.csv created")
    
    # Infrastructure data
    print("Creating infrastructure.csv...")
    np.random.seed(456)
    df = pd.DataFrame({
        'Date': dates,
        'CPU': np.random.uniform(20, 80, 365),
        'Memory': np.random.uniform(30, 85, 365),
        'Storage': np.random.uniform(40, 90, 365),
        'Servers': np.random.randint(5, 20, 365),
        'Latency': np.random.uniform(30, 80, 365),
        'Bandwidth': np.random.uniform(50, 150, 365)
    })
    df.to_csv('data/infrastructure.csv', index=False)
    print("✅ infrastructure.csv created")
    
    # Costs data
    print("Creating costs.csv...")
    np.random.seed(789)
    df = pd.DataFrame({
        'Month': dates,
        'ComputeCost': np.random.uniform(300, 700, 365),
        'StorageCost': np.random.uniform(100, 300, 365),
        'DatabaseCost': np.random.uniform(200, 400, 365),
        'NetworkCost': np.random.uniform(80, 220, 365),
        'MonitoringCost': np.random.uniform(60, 140, 365)
    })
    df['TotalCost'] = df[['ComputeCost', 'StorageCost', 'DatabaseCost', 'NetworkCost', 'MonitoringCost']].sum(axis=1)
    df.to_csv('data/costs.csv', index=False)
    print("✅ costs.csv created")
    
    print("\n✅ All data files generated successfully!")

if __name__ == "__main__":
    generate_data()
