"""
Chart creation utilities using Plotly
"""

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Tuple

class ChartBuilder:
    """
    Build professional Plotly charts for the dashboard
    """
    
    def __init__(self):
        """Initialize the chart builder"""
        self.colors = {
            'primary': '#1f77b4',
            'secondary': '#ff7f0e',
            'success': '#2ca02c',
            'danger': '#d62728',
            'purple': '#9467bd',
            'cyan': '#17becf',
            'pink': '#e377c2',
            'gray': '#7f7f7f'
        }
    
    def create_line_chart(self, df: pd.DataFrame, x_col: str, y_cols: List[str],
                         title: str = "", labels: Dict = None) -> go.Figure:
        """
        Create a line chart
        
        Args:
            df: DataFrame containing data
            x_col: Column for x-axis
            y_cols: Columns for y-axis
            title: Chart title
            labels: Dictionary for axis labels
            
        Returns:
            Plotly figure
        """
        fig = go.Figure()
        
        for i, y_col in enumerate(y_cols):
            color = list(self.colors.values())[i % len(self.colors)]
            fig.add_trace(
                go.Scatter(
                    x=df[x_col],
                    y=df[y_col],
                    mode='lines',
                    name=y_col,
                    line=dict(color=color, width=2),
                    hovertemplate='%{x}<br>%{y:,.0f}<extra></extra>'
                )
            )
        
        fig.update_layout(
            title=title,
            template='plotly_white',
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
            margin=dict(l=20, r=20, t=40, b=20),
            hovermode='x unified'
        )
        
        if labels:
            fig.update_xaxes(title_text=labels.get('x', ''))
            fig.update_yaxes(title_text=labels.get('y', ''))
        
        return fig
    
    def create_bar_chart(self, df: pd.DataFrame, x_col: str, y_col: str,
                        title: str = "", orientation: str = 'v') -> go.Figure:
        """
        Create a bar chart
        
        Args:
            df: DataFrame containing data
            x_col: Column for x-axis
            y_col: Column for y-axis
            title: Chart title
            orientation: 'v' for vertical, 'h' for horizontal
            
        Returns:
            Plotly figure
        """
        fig = go.Figure()
        
        fig.add_trace(
            go.Bar(
                x=df[x_col] if orientation == 'v' else df[y_col],
                y=df[y_col] if orientation == 'v' else df[x_col],
                orientation=orientation,
                marker_color=self.colors['primary'],
                text=df[y_col],
                textposition='outside'
            )
        )
        
        fig.update_layout(
            title=title,
            template='plotly_white',
            margin=dict(l=20, r=20, t=40, b=20)
        )
        
        return fig
    
    def create_pie_chart(self, values: List[float], labels: List[str],
                        title: str = "", hole: float = 0.0) -> go.Figure:
        """
        Create a pie or donut chart
        
        Args:
            values: Values for the pie
            labels: Labels for the pie
            title: Chart title
            hole: Hole size for donut chart (0-1)
            
        Returns:
            Plotly figure
        """
        fig = go.Figure()
        
        fig.add_trace(
            go.Pie(
                values=values,
                labels=labels,
                hole=hole,
                textinfo='percent+label',
                textposition='inside',
                marker=dict(
                    colors=list(self.colors.values())[:len(values)]
                )
            )
        )
        
        fig.update_layout(
            title=title,
            template='plotly_white',
            margin=dict(l=20, r=20, t=40, b=20)
        )
        
        return fig
    
    def create_forecast_chart(self, historical: pd.DataFrame, 
                             forecast: pd.DataFrame,
                             target_col: str,
                             confidence_bands: bool = True) -> go.Figure:
        """
        Create a forecast chart with confidence bands
        
        Args:
            historical: Historical data
            forecast: Forecast data
            target_col: Target column name
            confidence_bands: Whether to show confidence bands
            
        Returns:
            Plotly figure
        """
        fig = go.Figure()
        
        # Historical data
        fig.add_trace(
            go.Scatter(
                x=historical['Date'],
                y=historical[target_col],
                mode='lines',
                name='Historical',
                line=dict(color=self.colors['primary'], width=2)
            )
        )
        
        # Forecast
        fig.add_trace(
            go.Scatter(
                x=forecast['Date'],
                y=forecast['Forecast'],
                mode='lines',
                name='Forecast',
                line=dict(color=self.colors['secondary'], width=3, dash='dot')
            )
        )
        
        # Confidence bands
        if confidence_bands and 'Upper' in forecast.columns and 'Lower' in forecast.columns:
            fig.add_trace(
                go.Scatter(
                    x=forecast['Date'],
                    y=forecast['Upper'],
                    mode='lines',
                    name='Upper Bound',
                    line=dict(width=0),
                    showlegend=False
                )
            )
            
            fig.add_trace(
                go.Scatter(
                    x=forecast['Date'],
                    y=forecast['Lower'],
                    mode='lines',
                    name='Lower Bound',
                    line=dict(width=0),
                    fill='tonexty',
                    fillcolor='rgba(255, 127, 14, 0.2)',
                    showlegend=False
                )
            )
        
        fig.update_layout(
            title=f'Forecast - {target_col}',
            template='plotly_white',
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
            margin=dict(l=20, r=20, t=40, b=20),
            hovermode='x unified'
        )
        
        fig.update_xaxes(title_text='Date')
        fig.update_yaxes(title_text=target_col)
        
        return fig
    
    def create_heatmap(self, data: np.ndarray, x_labels: List[str],
                      y_labels: List[str], title: str = "") -> go.Figure:
        """
        Create a heatmap
        
        Args:
            data: 2D array of values
            x_labels: Labels for x-axis
            y_labels: Labels for y-axis
            title: Chart title
            
        Returns:
            Plotly figure
        """
        fig = go.Figure()
        
        fig.add_trace(
            go.Heatmap(
                z=data,
                x=x_labels,
                y=y_labels,
                colorscale='RdBu',
                zmid=0,
                text=data,
                texttemplate='%{text:.2f}',
                textfont={"size": 10}
            )
        )
        
        fig.update_layout(
            title=title,
            template='plotly_white',
            margin=dict(l=20, r=20, t=40, b=20)
        )
        
        return fig
    
    def create_gauge(self, value: float, title: str, 
                    min_val: float = 0, max_val: float = 100,
                    threshold: float = 70) -> go.Figure:
        """
        Create a gauge chart
        
        Args:
            value: Current value
            title: Chart title
            min_val: Minimum value
            max_val: Maximum value
            threshold: Threshold for warning
            
        Returns:
            Plotly figure
        """
        fig = go.Figure()
        
        fig.add_trace(
            go.Indicator(
                mode="gauge+number",
                value=value,
                title={'text': title},
                gauge={
                    'axis': {'range': [min_val, max_val]},
                    'bar': {'color': self.colors['primary']},
                    'threshold': {
                        'line': {'color': 'red', 'width': 4},
                        'thickness': 0.75,
                        'value': threshold
                    },
                    'steps': [
                        {'range': [min_val, threshold * 0.6], 'color': 'lightgreen'},
                        {'range': [threshold * 0.6, threshold * 0.9], 'color': 'lightyellow'},
                        {'range': [threshold * 0.9, max_val], 'color': 'lightcoral'}
                    ]
                },
                number={'suffix': '%'}
            )
        )
        
        fig.update_layout(
            height=300,
            template='plotly_white',
            margin=dict(l=20, r=20, t=40, b=20)
        )
        
        return fig
    
    def create_multi_axis_chart(self, df: pd.DataFrame, x_col: str,
                               y1_col: str, y2_col: str,
                               title: str = "") -> go.Figure:
        """
        Create a chart with two y-axes
        
        Args:
            df: DataFrame containing data
            x_col: Column for x-axis
            y1_col: First y-axis column
            y2_col: Second y-axis column
            title: Chart title
            
        Returns:
            Plotly figure
        """
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig.add_trace(
            go.Scatter(
                x=df[x_col],
                y=df[y1_col],
                mode='lines',
                name=y1_col,
                line=dict(color=self.colors['primary'], width=2)
            ),
            secondary_y=False
        )
        
        fig.add_trace(
            go.Scatter(
                x=df[x_col],
                y=df[y2_col],
                mode='lines',
                name=y2_col,
                line=dict(color=self.colors['secondary'], width=2, dash='dash')
            ),
            secondary_y=True
        )
        
        fig.update_layout(
            title=title,
            template='plotly_white',
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
            margin=dict(l=20, r=20, t=40, b=20),
            hovermode='x unified'
        )
        
        fig.update_xaxes(title_text=x_col)
        fig.update_yaxes(title_text=y1_col, secondary_y=False)
        fig.update_yaxes(title_text=y2_col, secondary_y=True)
        
        return fig