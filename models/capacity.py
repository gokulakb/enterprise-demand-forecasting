"""
Capacity planning module
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from dataclasses import dataclass
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

@dataclass
class ServerConfig:
    """Server configuration parameters"""
    cpu_cores: int = 4
    memory_gb: int = 16
    storage_gb: int = 500
    network_mbps: int = 1000
    max_concurrent: int = 1000
    cost_per_hour: float = 0.5

@dataclass
class CapacityMetrics:
    """Capacity metrics container"""
    current_cpu: float
    current_memory: float
    current_storage: float
    current_network: float
    current_servers: int
    current_concurrent: int
    projected_cpu: float
    projected_memory: float
    projected_storage: float
    projected_network: float
    required_servers: int
    required_cpu: int
    required_memory: int
    required_storage: int
    utilization: float
    scaling_recommendation: str

class CapacityPlanner:
    """
    Enterprise capacity planning and infrastructure management
    """
    
    def __init__(self, server_config: ServerConfig = None):
        """
        Initialize the capacity planner
        
        Args:
            server_config: Server configuration parameters
        """
        self.server_config = server_config or ServerConfig()
        self.capacity_data = None
        
    def analyze_current_capacity(self, infrastructure_df: pd.DataFrame) -> Dict:
        """
        Analyze current infrastructure capacity
        
        Args:
            infrastructure_df: Infrastructure data
            
        Returns:
            Dictionary with current capacity metrics
        """
        latest = infrastructure_df.iloc[-1]
        
        return {
            'cpu_usage': latest['CPU'],
            'memory_usage': latest['Memory'],
            'storage_usage': latest['Storage'],
            'servers': latest['Servers'],
            'latency': latest['Latency'],
            'bandwidth_usage': latest['Bandwidth'],
            'date': latest['Date']
        }
    
    def project_capacity(self, current: Dict, growth_factor: float, 
                        forecast_demand: float) -> Dict:
        """
        Project future capacity needs
        
        Args:
            current: Current capacity metrics
            growth_factor: Expected growth factor (1x, 2x, 5x, 10x)
            forecast_demand: Forecasted demand
            
        Returns:
            Projected capacity requirements
        """
        projections = {}
        
        # Project each metric
        projections['cpu'] = min(100, current['cpu_usage'] * growth_factor)
        projections['memory'] = min(100, current['memory_usage'] * growth_factor)
        projections['storage'] = min(100, current['storage_usage'] * growth_factor)
        projections['servers'] = int(np.ceil(current['servers'] * growth_factor))
        projections['bandwidth'] = current['bandwidth_usage'] * growth_factor
        projections['latency'] = current['latency'] * (1 + (growth_factor - 1) * 0.1)
        
        # Calculate required resources
        projections['required_cpu_cores'] = int(np.ceil(
            projections['cpu'] / 100 * self.server_config.cpu_cores * projections['servers']
        ))
        projections['required_memory_gb'] = int(np.ceil(
            projections['memory'] / 100 * self.server_config.memory_gb * projections['servers']
        ))
        projections['required_storage_gb'] = int(np.ceil(
            projections['storage'] / 100 * self.server_config.storage_gb * projections['servers']
        ))
        
        # Autoscaling recommendations
        projections['autoscaling_threshold'] = self._calculate_autoscaling_threshold(
            projections['cpu'], current['cpu_usage']
        )
        
        return projections
    
    def _calculate_autoscaling_threshold(self, projected_cpu: float, 
                                        current_cpu: float) -> str:
        """
        Calculate autoscaling recommendations
        
        Args:
            projected_cpu: Projected CPU usage
            current_cpu: Current CPU usage
            
        Returns:
            Recommendation string
        """
        ratio = projected_cpu / current_cpu if current_cpu > 0 else 1.0
        
        if ratio < 0.5:
            return "Scale down (over-provisioned)"
        elif ratio < 0.8:
            return "Maintain current capacity"
        elif ratio < 1.2:
            return "Prepare to scale up"
        elif ratio < 2.0:
            return "Scale up immediately"
        else:
            return "Emergency scaling required"
    
    def get_capacity_metrics(self, infrastructure_df: pd.DataFrame, 
                           forecast_demand: float, 
                           growth_factors: List[float] = [1.0, 2.0, 5.0, 10.0]) -> Dict:
        """
        Get comprehensive capacity metrics
        
        Args:
            infrastructure_df: Infrastructure data
            forecast_demand: Forecasted demand
            growth_factors: List of growth factors to consider
            
        Returns:
            Dictionary with capacity metrics
        """
        current = self.analyze_current_capacity(infrastructure_df)
        
        metrics = {
            'current': current,
            'projections': {},
            'recommendations': {}
        }
        
        for factor in growth_factors:
            projections = self.project_capacity(current, factor, forecast_demand)
            metrics['projections'][f'{factor}x'] = projections
            
            # Generate recommendations
            metrics['recommendations'][f'{factor}x'] = {
                'autoscaling': projections['autoscaling_threshold'],
                'additional_servers': max(0, projections['servers'] - current['servers']),
                'additional_cpu': max(0, projections['required_cpu_cores'] - 
                                    self.server_config.cpu_cores * current['servers']),
                'additional_memory': max(0, projections['required_memory_gb'] - 
                                       self.server_config.memory_gb * current['servers']),
                'additional_storage': max(0, projections['required_storage_gb'] - 
                                        self.server_config.storage_gb * current['servers'])
            }
        
        # Calculate utilization
        metrics['utilization'] = self._calculate_utilization(infrastructure_df)
        
        self.capacity_data = metrics
        return metrics
    
    def _calculate_utilization(self, infrastructure_df: pd.DataFrame) -> Dict:
        """
        Calculate average utilization of resources
        
        Args:
            infrastructure_df: Infrastructure data
            
        Returns:
            Dictionary with utilization metrics
        """
        latest = infrastructure_df.iloc[-1]
        avg_cpu = infrastructure_df['CPU'].mean()
        avg_memory = infrastructure_df['Memory'].mean()
        avg_storage = infrastructure_df['Storage'].mean()
        avg_bandwidth = infrastructure_df['Bandwidth'].mean()
        
        return {
            'cpu': {
                'current': latest['CPU'],
                'average': avg_cpu,
                'peak': infrastructure_df['CPU'].max(),
                'trend': 'increasing' if avg_cpu < latest['CPU'] else 'decreasing'
            },
            'memory': {
                'current': latest['Memory'],
                'average': avg_memory,
                'peak': infrastructure_df['Memory'].max(),
                'trend': 'increasing' if avg_memory < latest['Memory'] else 'decreasing'
            },
            'storage': {
                'current': latest['Storage'],
                'average': avg_storage,
                'peak': infrastructure_df['Storage'].max(),
                'trend': 'increasing' if avg_storage < latest['Storage'] else 'decreasing'
            },
            'bandwidth': {
                'current': latest['Bandwidth'],
                'average': avg_bandwidth,
                'peak': infrastructure_df['Bandwidth'].max(),
                'trend': 'increasing' if avg_bandwidth < latest['Bandwidth'] else 'decreasing'
            }
        }
    
    def get_autoscaling_recommendation(self, current_utilization: float, 
                                     threshold: float = 0.75) -> Dict:
        """
        Get autoscaling recommendation based on current utilization
        
        Args:
            current_utilization: Current utilization percentage
            threshold: Utilization threshold for scaling
            
        Returns:
            Dictionary with recommendation
        """
        if current_utilization < threshold * 0.6:
            return {
                'action': 'scale_down',
                'message': 'Resources are underutilized. Consider downsizing.',
                'urgency': 'low'
            }
        elif current_utilization < threshold:
            return {
                'action': 'maintain',
                'message': 'Resources are optimally utilized.',
                'urgency': 'none'
            }
        elif current_utilization < threshold * 1.2:
            return {
                'action': 'scale_up',
                'message': 'Resources are approaching capacity. Prepare to scale.',
                'urgency': 'medium'
            }
        else:
            return {
                'action': 'emergency_scale',
                'message': 'Resources are critically utilized. Immediate scaling required.',
                'urgency': 'high'
            }
    
    def generate_capacity_report(self, infrastructure_df: pd.DataFrame, 
                               forecast_demand: float) -> str:
        """
        Generate a capacity planning report
        
        Args:
            infrastructure_df: Infrastructure data
            forecast_demand: Forecasted demand
            
        Returns:
            Formatted report string
        """
        metrics = self.get_capacity_metrics(infrastructure_df, forecast_demand)
        
        report = f"""
        CAPACITY PLANNING REPORT
        ========================
        Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        
        CURRENT INFRASTRUCTURE
        ----------------------
        CPU Usage: {metrics['current']['cpu_usage']:.1f}%
        Memory Usage: {metrics['current']['memory_usage']:.1f}%
        Storage Usage: {metrics['current']['storage_usage']:.1f}%
        Active Servers: {metrics['current']['servers']}
        Average Latency: {metrics['current']['latency']:.1f}ms
        
        PROJECTED REQUIREMENTS
        ----------------------
        """
        
        for factor, projection in metrics['projections'].items():
            report += f"""
        {factor} GROWTH
        -----
        - CPU: {projection['cpu']:.1f}% (Required Cores: {projection['required_cpu_cores']})
        - Memory: {projection['memory']:.1f}% (Required GB: {projection['required_memory_gb']})
        - Storage: {projection['storage']:.1f}% (Required GB: {projection['required_storage_gb']})
        - Servers: {projection['servers']}
        - Recommendation: {projection['autoscaling_threshold']}
        """
        
        return report