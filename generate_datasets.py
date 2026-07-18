# save as generate_data.py and run
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_all_data():
    """Generate all datasets and save as CSV"""
    
    # Create data directory
    os.makedirs('data', exist_ok=True)
    
    # Generate dates
    start_date = datetime(2023, 1, 1)
    dates = [start_date + timedelta(days=i) for i in range(365)]
    
    # ============ TRAFFIC DATA ============
    print("Generating traffic data...")
    np.random.seed(42)
    
    base_requests = 100000
    base_users = 5000
    base_views = 50000
    
    seasonal_pattern = []
    for i in range(365):
        weekday = i % 7
        if weekday < 5:
            weekly_factor = 1.0 + np.random.normal(0, 0.05)
        else:
            weekly_factor = 0.7 + np.random.normal(0, 0.03)
        
        month = (i // 30) % 12
        month_factors = [0.9, 0.85, 0.95, 1.0, 1.05, 1.1, 1.15, 1.1, 1.05, 1.0, 0.95, 0.9]
        monthly_factor = month_factors[month]
        growth_factor = 1 + (i / 365) * 0.2
        seasonal_pattern.append(weekly_factor * monthly_factor * growth_factor)
    
    noise_factor = 0.05
    traffic_data = {
        'Date': dates,
        'Requests': [int(base_requests * factor * (1 + np.random.normal(0, noise_factor))) for factor in seasonal_pattern],
        'UniqueUsers': [int(base_users * factor * (1 + np.random.normal(0, noise_factor))) for factor in seasonal_pattern],
        'PageViews': [int(base_views * factor * (1 + np.random.normal(0, noise_factor))) for factor in seasonal_pattern],
        'PeakRequests': [int(base_requests * 1.5 * factor * (1 + np.random.normal(0, noise_factor))) for factor in seasonal_pattern],
        'ResponseTime': [max(50, int(100 * (1 + np.random.normal(0, 0.1)))) for _ in seasonal_pattern]
    }
    
    traffic_df = pd.DataFrame(traffic_data)
    traffic_df.to_csv('data/traffic.csv', index=False)
    print(f"  ✓ Generated {len(traffic_df)} traffic records")
    
    # ============ APPLICATIONS DATA ============
    print("Generating applications data...")
    np.random.seed(123)
    
    base_applications = 500
    base_interviews = 100
    base_offers = 40
    base_hires = 30
    
    patterns = []
    for i in range(365):
        weekday = i % 7
        if weekday < 5:
            weekly_factor = 1.0 + np.random.normal(0, 0.05)
        else:
            weekly_factor = 0.5 + np.random.normal(0, 0.02)
        
        month = (i // 30) % 12
        season_factors = [1.2, 1.1, 0.9, 1.0, 1.0, 0.8, 1.1, 1.0, 1.2, 1.1, 1.0, 0.9]
        season_factor = season_factors[month]
        growth = 1 + (i / 365) * 0.15
        patterns.append(weekly_factor * season_factor * growth)
    
    apps_data = {
        'Date': dates,
        'Applications': [int(base_applications * p * (1 + np.random.normal(0, 0.08))) for p in patterns],
        'Interviews': [int(base_interviews * p * (1 + np.random.normal(0, 0.08))) for p in patterns],
        'Offers': [int(base_offers * p * (1 + np.random.normal(0, 0.08))) for p in patterns],
        'Hires': [int(base_hires * p * (1 + np.random.normal(0, 0.08))) for p in patterns],
        'Placements': [int(base_hires * 0.9 * p * (1 + np.random.normal(0, 0.08))) for p in patterns]
    }
    
    apps_df = pd.DataFrame(apps_data)
    apps_df.to_csv('data/applications.csv', index=False)
    print(f"  ✓ Generated {len(apps_df)} applications records")
    
    # ============ INFRASTRUCTURE DATA ============
    print("Generating infrastructure data...")
    np.random.seed(456)
    
    base_cpu = 40
    base_memory = 60
    base_storage = 70
    base_servers = 10
    base_latency = 50
    base_bandwidth = 100
    
    patterns = []
    for i in range(365):
        growth = 1 + (i / 365) * 0.15
        weekday = i % 7
        if weekday < 5:
            weekly = 1.0 + np.random.normal(0, 0.02)
        else:
            weekly = 0.8 + np.random.normal(0, 0.02)
        patterns.append(growth * weekly)
    
    infra_data = {
        'Date': dates,
        'CPU': [min(95, base_cpu * p * (1 + np.random.normal(0, 0.05))) for p in patterns],
        'Memory': [min(95, base_memory * p * (1 + np.random.normal(0, 0.05))) for p in patterns],
        'Storage': [min(95, base_storage * p * (1 + np.random.normal(0, 0.03))) for p in patterns],
        'Servers': [max(5, int(base_servers * p * (1 + np.random.normal(0, 0.02)))) for p in patterns],
        'Latency': [max(10, base_latency * (1 + np.random.normal(0, 0.05))) for p in patterns],
        'Bandwidth': [max(50, base_bandwidth * p * (1 + np.random.normal(0, 0.05))) for p in patterns]
    }
    
    infra_df = pd.DataFrame(infra_data)
    infra_df.to_csv('data/infrastructure.csv', index=False)
    print(f"  ✓ Generated {len(infra_df)} infrastructure records")
    
    # ============ COSTS DATA ============
    print("Generating costs data...")
    np.random.seed(789)
    
    base_compute = 500
    base_storage = 200
    base_database = 300
    base_network = 150
    base_monitoring = 100
    
    patterns = []
    for i in range(365):
        growth = 1 + (i / 365) * 0.12
        weekday = i % 7
        if weekday < 5:
            weekly = 1.0 + np.random.normal(0, 0.02)
        else:
            weekly = 0.9 + np.random.normal(0, 0.02)
        patterns.append(growth * weekly)
    
    costs_data = {
        'Month': dates,
        'ComputeCost': [max(100, base_compute * p * (1 + np.random.normal(0, 0.05))) for p in patterns],
        'StorageCost': [max(50, base_storage * p * (1 + np.random.normal(0, 0.04))) for p in patterns],
        'DatabaseCost': [max(100, base_database * p * (1 + np.random.normal(0, 0.05))) for p in patterns],
        'NetworkCost': [max(50, base_network * p * (1 + np.random.normal(0, 0.04))) for p in patterns],
        'MonitoringCost': [max(30, base_monitoring * p * (1 + np.random.normal(0, 0.03))) for p in patterns]
    }
    
    costs_df = pd.DataFrame(costs_data)
    costs_df['TotalCost'] = costs_df[['ComputeCost', 'StorageCost', 'DatabaseCost', 'NetworkCost', 'MonitoringCost']].sum(axis=1)
    costs_df.to_csv('data/costs.csv', index=False)
    print(f"  ✓ Generated {len(costs_df)} cost records")
    
    print("\n✅ All datasets generated successfully!")
    print("\nFiles created in 'data/' directory:")
    print("  ✓ traffic.csv")
    print("  ✓ applications.csv")
    print("  ✓ infrastructure.csv")
    print("  ✓ costs.csv")
    
    # Verify the files
    print("\n📊 Verifying files...")
    for filename in ['traffic.csv', 'applications.csv', 'infrastructure.csv', 'costs.csv']:
        try:
            df = pd.read_csv(f'data/{filename}')
            print(f"  ✓ {filename}: {len(df)} rows, {len(df.columns)} columns")
        except Exception as e:
            print(f"  ✗ Error reading {filename}: {e}")

if __name__ == "__main__":
    generate_all_data()