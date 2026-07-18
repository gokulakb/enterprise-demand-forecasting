"""
Cost projection module
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

@dataclass
class CostConfig:
    """Cost configuration parameters"""
    compute_per_unit: float = 0.10  # Cost per compute unit
    storage_per_gb: float = 0.02   # Cost per GB storage
    database_per_gb: float = 0.05  # Cost per GB database
    network_per_gb: float = 0.01   # Cost per GB network
    monitoring_per_unit: float = 0.01  # Cost per monitoring unit
    backup_per_gb: float = 0.005   # Cost per GB backup

class CostProjector:
    """
    Enterprise cost projection and optimization
    """
    
    def __init__(self, cost_config: CostConfig = None):
        """Initialize the cost projector"""
        self.cost_config = cost_config or CostConfig()
        self.cost_data = None
        
    def analyze_current_costs(self, costs_df: pd.DataFrame) -> Dict:
        """
        Analyze current costs
        
        Args:
            costs_df: Cost data
            
        Returns:
            Dictionary with current cost metrics
        """
        latest = costs_df.iloc[-1]
        
        return {
            'total': latest['TotalCost'],
            'compute': latest['ComputeCost'],
            'storage': latest['StorageCost'],
            'database': latest['DatabaseCost'],
            'network': latest['NetworkCost'],
            'monitoring': latest['MonitoringCost'],
            'date': latest['Month'],
            'avg_monthly': costs_df['TotalCost'].mean(),
            'min_monthly': costs_df['TotalCost'].min(),
            'max_monthly': costs_df['TotalCost'].max()
        }
    
    def project_costs(self, current_costs: Dict, growth_factor: float, 
                     forecast_demand: float) -> Dict:
        """
        Project future costs
        
        Args:
            current_costs: Current cost metrics
            growth_factor: Expected growth factor
            forecast_demand: Forecasted demand
            
        Returns:
            Dictionary with projected costs
        """
        projections = {}
        
        # Base projection (proportional to growth)
        base_multiplier = growth_factor
        
        # Additional factors
        demand_factor = 1 + (forecast_demand / 100) * 0.01
        efficiency_factor = 0.95  # Assuming 5% efficiency improvement
        
        projections['total'] = current_costs['total'] * base_multiplier * demand_factor * efficiency_factor
        projections['compute'] = current_costs['compute'] * base_multiplier * demand_factor * efficiency_factor
        projections['storage'] = current_costs['storage'] * base_multiplier * demand_factor * efficiency_factor
        projections['database'] = current_costs['database'] * base_multiplier * demand_factor * efficiency_factor
        projections['network'] = current_costs['network'] * base_multiplier * demand_factor * efficiency_factor
        projections['monitoring'] = current_costs['monitoring'] * base_multiplier * demand_factor * efficiency_factor
        
        # Per-unit metrics
        projections['cost_per_request'] = projections['total'] / (forecast_demand + 1)
        projections['cost_per_user'] = projections['total'] / (forecast_demand * 0.01 + 1)
        
        return projections
    
    def get_cost_metrics(self, costs_df: pd.DataFrame, 
                        forecast_demand: float,
                        growth_factors: List[float] = [1.0, 2.0, 5.0, 10.0]) -> Dict:
        """
        Get comprehensive cost metrics
        
        Args:
            costs_df: Cost data
            forecast_demand: Forecasted demand
            growth_factors: List of growth factors to consider
            
        Returns:
            Dictionary with cost metrics
        """
        current = self.analyze_current_costs(costs_df)
        
        metrics = {
            'current': current,
            'projections': {},
            'breakdown': self._get_cost_breakdown(costs_df),
            'trends': self._analyze_cost_trends(costs_df)
        }
        
        for factor in growth_factors:
            projections = self.project_costs(current, factor, forecast_demand)
            metrics['projections'][f'{factor}x'] = projections
        
        # Calculate savings opportunities
        metrics['savings_opportunities'] = self._calculate_savings_opportunities(
            costs_df, current
        )
        
        self.cost_data = metrics
        return metrics
    
    def _get_cost_breakdown(self, costs_df: pd.DataFrame) -> Dict:
        """
        Get cost breakdown by category
        
        Args:
            costs_df: Cost data
            
        Returns:
            Dictionary with cost breakdown
        """
        latest = costs_df.iloc[-1]
        total = latest['TotalCost']
        
        breakdown = {}
        for col in ['ComputeCost', 'StorageCost', 'DatabaseCost', 
                   'NetworkCost', 'MonitoringCost']:
            if total > 0:
                percentage = (latest[col] / total) * 100
            else:
                percentage = 0
            breakdown[col] = {
                'amount': latest[col],
                'percentage': percentage
            }
        
        return breakdown
    
    def _analyze_cost_trends(self, costs_df: pd.DataFrame) -> Dict:
        """
        Analyze cost trends over time
        
        Args:
            costs_df: Cost data
            
        Returns:
            Dictionary with trend analysis
        """
        # Calculate month-over-month changes
        costs_df = costs_df.sort_values('Month')
        monthly_changes = costs_df['TotalCost'].pct_change() * 100
        
        return {
            'avg_monthly_growth': monthly_changes.mean(),
            'max_monthly_growth': monthly_changes.max(),
            'min_monthly_growth': monthly_changes.min(),
            'trend_direction': 'increasing' if monthly_changes.mean() > 0 else 'decreasing'
        }
    
    def _calculate_savings_opportunities(self, costs_df: pd.DataFrame, 
                                       current: Dict) -> List[Dict]:
        """
        Calculate potential savings opportunities
        
        Args:
            costs_df: Cost data
            current: Current cost metrics
            
        Returns:
            List of savings opportunities
        """
        opportunities = []
        
        # Check for over-provisioning
        avg_cost = costs_df['TotalCost'].mean()
        if current['total'] > avg_cost * 1.2:
            opportunities.append({
                'category': 'Cost Optimization',
                'description': 'Current costs are above average. Review resource utilization.',
                'potential_savings': current['total'] * 0.1,
                'effort': 'medium'
            })
        
        # Check compute costs
        if current['compute'] > current['total'] * 0.4:
            opportunities.append({
                'category': 'Compute Optimization',
                'description': 'Compute costs are high. Consider rightsizing instances.',
                'potential_savings': current['compute'] * 0.15,
                'effort': 'high'
            })
        
        # Check storage costs
        if current['storage'] > current['total'] * 0.15:
            opportunities.append({
                'category': 'Storage Optimization',
                'description': 'Storage costs are high. Review data retention policies.',
                'potential_savings': current['storage'] * 0.2,
                'effort': 'low'
            })
        
        return opportunities
    
    def calculate_roi(self, initial_investment: float, projected_savings: List[float]) -> Dict:
        """
        Calculate ROI for cost optimization initiatives
        
        Args:
            initial_investment: Initial investment amount
            projected_savings: List of projected annual savings
            
        Returns:
            Dictionary with ROI metrics
        """
        total_savings = sum(projected_savings)
        net_benefit = total_savings - initial_investment
        roi = (net_benefit / initial_investment) * 100 if initial_investment > 0 else 0
        
        return {
            'initial_investment': initial_investment,
            'total_savings': total_savings,
            'net_benefit': net_benefit,
            'roi_percentage': roi,
            'payback_period': initial_investment / total_savings if total_savings > 0 else float('inf')
        }
    
    def generate_cost_report(self, costs_df: pd.DataFrame, 
                           forecast_demand: float) -> str:
        """
        Generate a cost projection report
        
        Args:
            costs_df: Cost data
            forecast_demand: Forecasted demand
            
        Returns:
            Formatted report string
        """
        metrics = self.get_cost_metrics(costs_df, forecast_demand)
        current = metrics['current']
        
        report = f"""
        COST PROJECTION REPORT
        ======================
        Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        
        CURRENT COSTS
        -------------
        Monthly Total: ${current['total']:,.2f}
        Monthly Average: ${current['avg_monthly']:,.2f}
        Yearly Total: ${current['total'] * 12:,.2f}
        
        COST BREAKDOWN
        --------------
        Compute: ${current['compute']:,.2f}
        Storage: ${current['storage']:,.2f}
        Database: ${current['database']:,.2f}
        Network: ${current['network']:,.2f}
        Monitoring: ${current['monitoring']:,.2f}
        
        PROJECTED COSTS
        ---------------
        """
        
        for factor, projection in metrics['projections'].items():
            report += f"""
        {factor} GROWTH
        - Monthly: ${projection['total']:,.2f}
        - Annual: ${projection['total'] * 12:,.2f}
        - Cost per Request: ${projection['cost_per_request']:,.4f}
        - Cost per User: ${projection['cost_per_user']:,.2f}
        """
        
        # Add savings opportunities
        if metrics['savings_opportunities']:
            report += """
        SAVINGS OPPORTUNITIES
        --------------------
        """
            for opp in metrics['savings_opportunities']:
                report += f"""
        - {opp['description']}
          Potential Savings: ${opp['potential_savings']:,.2f} ({opp['effort']} effort)
        """
        
        return report