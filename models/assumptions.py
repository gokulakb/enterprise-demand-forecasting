"""
Assumptions and risk management module
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

@dataclass
class Assumption:
    """Assumption definition"""
    name: str
    value: float
    unit: str
    description: str
    confidence: float  # 0-1
    risk_level: str  # Low, Medium, High
    impact: str  # Low, Medium, High, Critical

@dataclass
class Risk:
    """Risk definition"""
    name: str
    description: str
    probability: float  # 0-1
    impact: str  # Low, Medium, High, Critical
    category: str
    mitigation: str
    status: str  # Active, Mitigated, Resolved

class AssumptionManager:
    """
    Manages assumptions and risks for the forecasting platform
    """
    
    def __init__(self):
        """Initialize the assumption manager"""
        self.assumptions = []
        self.risks = []
        self.scenarios = {}
        
        # Initialize with default assumptions
        self._initialize_assumptions()
        self._initialize_risks()
        self._initialize_scenarios()
    
    def _initialize_assumptions(self):
        """Initialize default assumptions"""
        defaults = [
            Assumption(
                name="Traffic Growth Rate",
                value=0.15,
                unit="%",
                description="Expected annual growth in traffic",
                confidence=0.7,
                risk_level="Medium",
                impact="High"
            ),
            Assumption(
                name="Application Growth Rate",
                value=0.12,
                unit="%",
                description="Expected annual growth in applications",
                confidence=0.65,
                risk_level="Medium",
                impact="Medium"
            ),
            Assumption(
                name="User Retention Rate",
                value=0.85,
                unit="%",
                description="Expected user retention rate",
                confidence=0.75,
                risk_level="Low",
                impact="Medium"
            ),
            Assumption(
                name="Server Capacity per Unit",
                value=0.8,
                unit="%",
                description="Average server utilization before scaling",
                confidence=0.8,
                risk_level="Low",
                impact="Low"
            ),
            Assumption(
                name="Cloud Pricing Growth",
                value=0.05,
                unit="%",
                description="Expected annual cloud cost increase",
                confidence=0.6,
                risk_level="Medium",
                impact="High"
            ),
            Assumption(
                name="Model Accuracy Threshold",
                value=0.85,
                unit="%",
                description="Minimum acceptable model accuracy",
                confidence=0.7,
                risk_level="Medium",
                impact="High"
            ),
            Assumption(
                name="Seasonal Adjustment Factor",
                value=0.15,
                unit="%",
                description="Expected seasonal variation",
                confidence=0.6,
                risk_level="Medium",
                impact="Medium"
            )
        ]
        
        self.assumptions.extend(defaults)
    
    def _initialize_risks(self):
        """Initialize default risks"""
        defaults = [
            Risk(
                name="Demand Forecasting Error",
                description="Inaccurate demand forecasts leading to capacity issues",
                probability=0.3,
                impact="High",
                category="Data Quality",
                mitigation="Regular model retraining, backtesting, and ensemble methods",
                status="Active"
            ),
            Risk(
                name="Cloud Cost Overrun",
                description="Unexpected increase in cloud costs",
                probability=0.4,
                impact="High",
                category="Financial",
                mitigation="Implement cost alerts, optimize resource usage, reserved instances",
                status="Active"
            ),
            Risk(
                name="Infrastructure Capacity Shortage",
                description="Insufficient capacity to handle demand spikes",
                probability=0.25,
                impact="Critical",
                category="Operations",
                mitigation="Autoscaling, capacity buffers, load testing",
                status="Active"
            ),
            Risk(
                name="Seasonal Demand Mismatch",
                description="Failure to anticipate seasonal demand changes",
                probability=0.35,
                impact="Medium",
                category="Business",
                mitigation="Seasonal pattern analysis, advanced forecasting models",
                status="Active"
            ),
            Risk(
                name="Data Quality Issues",
                description="Inconsistent or missing data affecting accuracy",
                probability=0.2,
                impact="Medium",
                category="Data Quality",
                mitigation="Data validation, automated cleaning, anomaly detection",
                status="Active"
            ),
            Risk(
                name="Competitive Market Changes",
                description="Market changes affecting user behavior",
                probability=0.4,
                impact="High",
                category="Market",
                mitigation="Competitive analysis, market monitoring, agile planning",
                status="Active"
            )
        ]
        
        self.risks.extend(defaults)
    
    def _initialize_scenarios(self):
        """Initialize different scenarios"""
        self.scenarios = {
            'expected': {
                'description': 'Most likely scenario based on historical trends',
                'growth_rate': 0.15,
                'confidence': 0.7,
                'cost_multiplier': 1.1,
                'capacity_multiplier': 1.15
            },
            'best_case': {
                'description': 'Optimistic scenario with higher growth and lower costs',
                'growth_rate': 0.25,
                'confidence': 0.3,
                'cost_multiplier': 0.95,
                'capacity_multiplier': 1.05
            },
            'worst_case': {
                'description': 'Pessimistic scenario with lower growth and higher costs',
                'growth_rate': 0.05,
                'confidence': 0.3,
                'cost_multiplier': 1.3,
                'capacity_multiplier': 1.4
            }
        }
    
    def add_assumption(self, name: str, value: float, unit: str,
                      description: str, confidence: float,
                      risk_level: str, impact: str):
        """Add a new assumption"""
        assumption = Assumption(
            name=name,
            value=value,
            unit=unit,
            description=description,
            confidence=confidence,
            risk_level=risk_level,
            impact=impact
        )
        self.assumptions.append(assumption)
    
    def get_assumption(self, name: str) -> Assumption:
        """Get an assumption by name"""
        for assumption in self.assumptions:
            if assumption.name == name:
                return assumption
        return None
    
    def update_assumption(self, name: str, **kwargs):
        """Update an existing assumption"""
        assumption = self.get_assumption(name)
        if assumption:
            for key, value in kwargs.items():
                if hasattr(assumption, key):
                    setattr(assumption, key, value)
        return assumption
    
    def add_risk(self, name: str, description: str, probability: float,
                impact: str, category: str, mitigation: str):
        """Add a new risk"""
        risk = Risk(
            name=name,
            description=description,
            probability=probability,
            impact=impact,
            category=category,
            mitigation=mitigation,
            status="Active"
        )
        self.risks.append(risk)
    
    def get_risk_matrix(self) -> Dict:
        """
        Generate a risk matrix
        
        Returns:
            Dictionary with risk matrix data
        """
        matrix = {
            'High': {'High': [], 'Medium': [], 'Low': []},
            'Medium': {'High': [], 'Medium': [], 'Low': []},
            'Low': {'High': [], 'Medium': [], 'Low': []}
        }
        
        for risk in self.risks:
            # Categorize probability
            if risk.probability >= 0.7:
                prob = 'High'
            elif risk.probability >= 0.3:
                prob = 'Medium'
            else:
                prob = 'Low'
            
            # Add to matrix
            if risk.impact in matrix:
                if prob in matrix[risk.impact]:
                    matrix[risk.impact][prob].append(risk)
        
        return matrix
    
    def get_impact_analysis(self) -> List[Dict]:
        """
        Perform impact analysis on risks
        
        Returns:
            List of impact analysis results
        """
        results = []
        
        for risk in self.risks:
            # Calculate risk score
            prob_score = risk.probability * 10
            impact_scores = {'Low': 1, 'Medium': 3, 'High': 5, 'Critical': 7}
            impact_score = impact_scores.get(risk.impact, 1)
            
            risk_score = prob_score * impact_score
            
            results.append({
                'risk': risk.name,
                'probability': risk.probability,
                'impact': risk.impact,
                'risk_score': risk_score,
                'priority': self._get_priority(risk_score),
                'category': risk.category,
                'mitigation': risk.mitigation
            })
        
        # Sort by risk score (descending)
        results.sort(key=lambda x: x['risk_score'], reverse=True)
        return results
    
    def _get_priority(self, risk_score: float) -> str:
        """Get priority based on risk score"""
        if risk_score >= 25:
            return 'Critical'
        elif risk_score >= 15:
            return 'High'
        elif risk_score >= 8:
            return 'Medium'
        else:
            return 'Low'
    
    def get_forecast_confidence(self) -> Dict:
        """
        Calculate overall forecast confidence
        
        Returns:
            Dictionary with confidence metrics
        """
        confidences = [a.confidence for a in self.assumptions]
        
        if not confidences:
            return {'overall': 0, 'details': {}}
        
        overall = np.mean(confidences) * 100
        
        return {
            'overall': overall,
            'details': {
                'min': min(confidences) * 100,
                'max': max(confidences) * 100,
                'median': np.median(confidences) * 100,
                'std': np.std(confidences) * 100
            },
            'confidence_level': self._get_confidence_level(overall)
        }
    
    def _get_confidence_level(self, confidence: float) -> str:
        """Get confidence level based on percentage"""
        if confidence >= 80:
            return 'Very High'
        elif confidence >= 65:
            return 'High'
        elif confidence >= 50:
            return 'Medium'
        elif confidence >= 35:
            return 'Low'
        else:
            return 'Very Low'
    
    def get_mitigation_recommendations(self) -> List[Dict]:
        """
        Get mitigation recommendations for risks
        
        Returns:
            List of mitigation recommendations
        """
        recommendations = []
        
        for risk in self.risks:
            if risk.status == 'Active':
                recommendations.append({
                    'risk': risk.name,
                    'mitigation': risk.mitigation,
                    'priority': self._get_priority(risk.probability * 10 * 
                                                  {'Low': 1, 'Medium': 3, 
                                                   'High': 5, 'Critical': 7}.get(risk.impact, 1)),
                    'category': risk.category,
                    'status': risk.status
                })
        
        # Sort by priority
        priority_order = {'Critical': 0, 'High': 1, 'Medium': 2, 'Low': 3}
        recommendations.sort(key=lambda x: priority_order.get(x['priority'], 4))
        
        return recommendations
    
    def generate_assumptions_report(self) -> str:
        """
        Generate an assumptions report
        
        Returns:
            Formatted report string
        """
        report = f"""
        ASSUMPTIONS REPORT
        ==================
        Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        
        KEY ASSUMPTIONS
        --------------
        """
        
        for assumption in self.assumptions:
            report += f"""
        {assumption.name}
        - Value: {assumption.value} {assumption.unit}
        - Description: {assumption.description}
        - Confidence: {assumption.confidence*100:.0f}%
        - Risk Level: {assumption.risk_level}
        - Impact: {assumption.impact}
        """
        
        # Scenarios
        report += """
        SCENARIOS
        ---------
        """
        
        for name, scenario in self.scenarios.items():
            report += f"""
        {name.upper()}
        - Description: {scenario['description']}
        - Growth Rate: {scenario['growth_rate']*100:.0f}%
        - Cost Multiplier: {scenario['cost_multiplier']:.2f}
        - Capacity Multiplier: {scenario['capacity_multiplier']:.2f}
        """
        
        # Risks
        report += """
        RISK ASSESSMENT
        --------------
        """
        
        for risk in self.risks:
            report += f"""
        {risk.name}
        - Probability: {risk.probability*100:.0f}%
        - Impact: {risk.impact}
        - Category: {risk.category}
        - Status: {risk.status}
        """
        
        return report