import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

class CostDashboard:
    """Cost Projection dashboard"""
    
    def render(self, data: dict, growth_multiplier: float):
        """Render the cost projection dashboard"""
        st.markdown("## 💰 Cost Projection")
        st.caption("Financial analysis and projections")
        
        costs_df = data['costs']
        latest = costs_df.iloc[-1]
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="💰 Monthly Total",
                value=f"${latest['TotalCost']:,.2f}",
                delta=f"${latest['TotalCost'] * growth_multiplier:,.2f} at {growth_multiplier}x"
            )
        
        with col2:
            annual_cost = latest['TotalCost'] * 12
            st.metric(
                label="📊 Annual Total",
                value=f"${annual_cost:,.2f}",
                delta=f"${annual_cost * growth_multiplier:,.2f} projected"
            )
        
        with col3:
            avg_cost = costs_df['TotalCost'].mean()
            st.metric(
                label="📈 Avg Monthly Cost",
                value=f"${avg_cost:,.2f}",
                delta=f"{((latest['TotalCost'] - avg_cost) / avg_cost * 100):.1f}%"
            )
        
        with col4:
            st.metric(
                label="💡 Cost per Request",
                value=f"${latest['TotalCost'] / 100000:.4f}",
                delta=f"${(latest['TotalCost'] * growth_multiplier) / 100000:.4f} at {growth_multiplier}x"
            )
        
        # Cost breakdown chart
        st.markdown("---")
        st.markdown("### 📊 Cost Breakdown")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Pie chart
            categories = ['Compute', 'Storage', 'Database', 'Network', 'Monitoring']
            values = [latest['ComputeCost'], latest['StorageCost'], latest['DatabaseCost'], 
                     latest['NetworkCost'], latest['MonitoringCost']]
            
            fig = go.Figure(data=[go.Pie(
                labels=categories,
                values=values,
                hole=0.3,
                marker=dict(colors=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'])
            )])
            
            fig.update_layout(
                height=350,
                title='Cost Distribution',
                template='plotly_white',
                margin=dict(l=20, r=20, t=40, b=20)
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Cost trend
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=costs_df.index,
                y=costs_df['TotalCost'],
                mode='lines+markers',
                name='Total Cost',
                line=dict(color='#1f77b4', width=2),
                marker=dict(size=4)
            ))
            
            # Moving average
            ma = costs_df['TotalCost'].rolling(window=7).mean()
            fig.add_trace(go.Scatter(
                x=costs_df.index,
                y=ma,
                mode='lines',
                name='7-day MA',
                line=dict(color='#ff7f0e', width=2, dash='dash')
            ))
            
            fig.update_layout(
                height=350,
                title='Cost Trend',
                template='plotly_white',
                legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
                margin=dict(l=20, r=20, t=40, b=20)
            )
            
            fig.update_yaxes(title_text='Cost ($)')
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Projections
        st.markdown("---")
        st.markdown("### 📈 Cost Projections")
        
        col1, col2, col3 = st.columns(3)
        
        for i, factor in enumerate([2.0, 5.0, 10.0]):
            projected = latest['TotalCost'] * factor
            annual = projected * 12
            
            with [col1, col2, col3][i]:
                st.markdown(f"#### {factor}x Growth")
                st.metric("Monthly", f"${projected:,.2f}")
                st.metric("Annual", f"${annual:,.2f}")
                st.metric("Increase", f"${projected - latest['TotalCost']:,.2f}")
