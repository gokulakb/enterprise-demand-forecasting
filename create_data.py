import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# Create data directory
os.makedirs('data', exist_ok=True)

# Generate dates
start_date = datetime(2023, 1, 1)
dates = [start_date + timedelta(days=i) for i in range(365)]

print("Generating traffic data...")
np.random.seed(42)
traffic_data = {
    'Date': dates,
    'Requests': np.random.randint(80000, 150000, 365),
    'UniqueUsers': np.random.randint(4000, 8000, 365),
    'PageViews': np.random.randint(40000, 70000, 365),
    'PeakRequests': np.random.randint(120000, 200000, 365),
    'ResponseTime': np.random.randint(50, 200, 365)
}
traffic_df = pd.DataFrame(traffic_data)
traffic_df.to_csv('data/traffic.csv', index=False)
print(f"  ✓ Created traffic.csv with {len(traffic_df)} rows")

print("Generating applications data...")
np.random.seed(123)
apps_data = {
    'Date': dates,
    'Applications': np.random.randint(300, 700, 365),
    'Interviews': np.random.randint(60, 140, 365),
    'Offers': np.random.randint(20, 60, 365),
    'Hires': np.random.randint(10, 50, 365),
    'Placements': np.random.randint(5, 45, 365)
}
apps_df = pd.DataFrame(apps_data)
apps_df.to_csv('data/applications.csv', index=False)
print(f"  ✓ Created applications.csv with {len(apps_df)} rows")

print("Generating infrastructure data...")
np.random.seed(456)
infra_data = {
    'Date': dates,
    'CPU': np.random.uniform(20, 80, 365),
    'Memory': np.random.uniform(30, 85, 365),
    'Storage': np.random.uniform(40, 90, 365),
    'Servers': np.random.randint(5, 20, 365),
    'Latency': np.random.uniform(30, 80, 365),
    'Bandwidth': np.random.uniform(50, 150, 365)
}
infra_df = pd.DataFrame(infra_data)
infra_df.to_csv('data/infrastructure.csv', index=False)
print(f"  ✓ Created infrastructure.csv with {len(infra_df)} rows")

print("Generating costs data...")
np.random.seed(789)
costs_data = {
    'Month': dates,
    'ComputeCost': np.random.uniform(300, 700, 365),
    'StorageCost': np.random.uniform(100, 300, 365),
    'DatabaseCost': np.random.uniform(200, 400, 365),
    'NetworkCost': np.random.uniform(80, 220, 365),
    'MonitoringCost': np.random.uniform(60, 140, 365)
}
costs_df = pd.DataFrame(costs_data)
costs_df['TotalCost'] = costs_df[['ComputeCost', 'StorageCost', 'DatabaseCost', 'NetworkCost', 'MonitoringCost']].sum(axis=1)
costs_df.to_csv('data/costs.csv', index=False)
print(f"  ✓ Created costs.csv with {len(costs_df)} rows")

print("\n✅ All datasets generated successfully!")
print("\nFiles created in 'data/' directory:")
import os
for f in os.listdir('data'):
    if f.endswith('.csv'):
        size = os.path.getsize(f'data/{f}')
        print(f"  ✓ {f} ({size} bytes)")
