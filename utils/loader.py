import pandas as pd
import os
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

class DataLoader:
    """Load and manage data files for the application"""
    
    def __init__(self, data_dir: str = 'data/'):
        """Initialize the data loader"""
        self.data_dir = data_dir
        self.data = {}
        
    def load_csv(self, filename: str, **kwargs) -> Optional[pd.DataFrame]:
        """Load a CSV file"""
        # Try multiple paths
        paths = [
            os.path.join('data', filename),
            os.path.join(os.getcwd(), 'data', filename),
            os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', filename),
            filename
        ]
        
        for path in paths:
            if os.path.exists(path):
                try:
                    df = pd.read_csv(path, **kwargs)
                    logger.info(f"Loaded {len(df)} rows from {path}")
                    return df
                except Exception as e:
                    logger.error(f"Error loading {path}: {e}")
                    continue
        
        logger.warning(f"File not found: {filename}")
        return None
    
    def load_all_data(self) -> Dict[str, pd.DataFrame]:
        """Load all required data files"""
        files = {
            'traffic': 'traffic.csv',
            'applications': 'applications.csv',
            'infrastructure': 'infrastructure.csv',
            'costs': 'costs.csv'
        }
        
        logger.info(f"Current working directory: {os.getcwd()}")
        logger.info(f"Data directory exists: {os.path.exists('data')}")
        
        for key, filename in files.items():
            df = self.load_csv(filename)
            if df is not None:
                self.data[key] = df
                logger.info(f"✅ Loaded {key} data")
            else:
                logger.warning(f"❌ Failed to load {key} data")
        
        logger.info(f"Loaded {len(self.data)} datasets")
        return self.data
    
    def get_data(self, key: str) -> Optional[pd.DataFrame]:
        """Get a specific dataset"""
        return self.data.get(key)
