import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

class OverviewDashboard:
    """Executive Overview dashboard with key metrics"""
    
    def render(self, data: dict, forecast_days: int, growth_multiplier: float):
        """Render the executive overview dashboard"""
        st.markdown("## 🏢 Executive Overview")
        st.caption("Real-time enterprise metrics and forecasts")
        
        # Get data
        traffic_df = data['traffic']
        apps_df = data.get('applications', pd.DataFrame())
        infra_df = data.get('infrastructure', pd.DataFrame())
        costs_df = data.get('costs', pd.DataFrame())
        
        # Get latest values
        latest_traffic = traffic_df.iloc[-1]
        
        # Key Metrics Row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="📈 Current Daily Traffic",
                value=f"{latest_traffic['Requests']:,}",
                delta=f"{traffic_df['Requests'].mean():,.0f} avg"
            )
        
        with col2:
            if not apps_df.empty:
                latest_apps = apps_df.iloc[-1]
                st.metric(
                    label="📋 Current Applications",
                    value=f"{latest_apps['Applications']:,}",
                    delta=f"{apps_df['Applications'].mean():,.0f} avg"
                )
            else:
                st.metric(label="📋 Applications", value="N/A")
        
        with col3:
            if not infra_df.empty:
                latest_infra = infra_df.iloc[-1]
                st.metric(
                    label="🖥️ CPU Utilization",
                    value=f"{latest_infra['CPU']:.1f}%",
                    delta=f"Avg: {infra_df['CPU'].mean():.1f}%"
                )
            else:
                st.metric(label="🖥️ CPU", value="N/A")
        
        with col4:
            if not costs_df.empty:
                latest_costs = costs_df.iloc[-1]
                st.metric(
                    label="💰 Monthly Cost",
                    value=f"${latest_costs['TotalCost']:,.2f}",
                    delta=f"${costs_df['TotalCost'].mean():,.2f} avg"
                )
            else:
                st.metric(label="💰 Cost", value="N/A")
        
        # Charts
        st.markdown("---")
        st.markdown("### 📈 Trend Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Traffic trend chart
            fig = self._create_trend_chart(traffic_df, 'Requests', 'Daily Traffic')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Cost trend chart
            if not costs_df.empty:
                fig = self._create_trend_chart(costs_df, 'TotalCost', 'Monthly Cost')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No cost data available")
        
        # Additional metrics
        st.markdown("---")
        st.markdown("### 📊 Key Insights")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Growth rate
            growth = ((traffic_df['Requests'].iloc[-30:].mean() - traffic_df['Requests'].iloc[-60:-30].mean()) / 
                     traffic_df['Requests'].iloc[-60:-30].mean() * 100)
            st.metric(
                label="📊 Traffic Growth Rate",
                value=f"{growth:.1f}%",
                delta="30-day trend"
            )
        
        with col2:
            # Peak traffic
            peak = traffic_df['Requests'].max()
            peak_date = traffic_df[traffic_df['Requests'] == peak]['Date'].iloc[0]
            st.metric(
                label="⛰️ Peak Traffic",
                value=f"{peak:,}",
                delta=f"on {pd.to_datetime(peak_date).strftime('%Y-%m-%d')}"
            )
        
        with col3:
            # Confidence score (simplified)
            confidence = 85 - (traffic_df['Requests'].std() / traffic_df['Requests'].mean() * 100)
            confidence = max(50, min(95, confidence))
            st.metric(
                label="🎯 Forecast Confidence",
                value=f"{confidence:.0f}%",
                delta="Based on data stability"
            )
    
    def _create_trend_chart(self, df, column, title):
        """Create a trend chart"""
        fig = go.Figure()
        
        # Main line
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df[column],
            mode='lines',
            name=column,
            line=dict(color='#1f77b4', width=2),
            hovertemplate='%{y:,.0f}<extra></extra>'
        ))
        
        # Moving average
        ma = df[column].rolling(window=7).mean()
        fig.add_trace(go.Scatter(
            x=df.index,
            y=ma,
            mode='lines',
            name='7-day MA',
            line=dict(color='#ff7f0e', width=2, dash='dash'),
            hovertemplate='%{y:,.0f}<extra></extra>'
        ))
        
        fig.update_layout(
            height=350,
            title=title,
            template='plotly_white',
            margin=dict(l=20, r=20, t=40, b=20),
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
        )
        
        fig.update_xaxes(title_text='Date')
        fig.update_yaxes(title_text=column)
        
        return fig
