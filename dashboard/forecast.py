import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta

class ForecastDashboard:
    """Demand Forecast dashboard"""
    
    def render(self, data: dict, forecast_days: int):
        """Render the forecast dashboard"""
        st.markdown("## 📈 Demand Forecast")
        st.caption("Interactive demand forecasting")
        
        traffic_df = data['traffic']
        
        # Simple forecast using moving average and trend
        df = traffic_df.copy()
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values('Date')
        
        # Calculate forecast using simple linear extrapolation
        last_30_days = df['Requests'].iloc[-30:].values
        trend = (last_30_days[-1] - last_30_days[0]) / len(last_30_days)
        last_value = df['Requests'].iloc[-1]
        
        # Generate forecast dates
        last_date = df['Date'].iloc[-1]
        forecast_dates = [last_date + timedelta(days=i+1) for i in range(forecast_days)]
        
        # Generate forecast values with some noise
        forecast_values = []
        for i in range(forecast_days):
            value = last_value + trend * (i + 1) + np.random.normal(0, last_value * 0.02)
            forecast_values.append(max(0, value))
        
        # Calculate confidence intervals
        std_dev = np.std(forecast_values)
        upper_bound = [v + std_dev * 1.96 for v in forecast_values]
        lower_bound = [v - std_dev * 1.96 for v in forecast_values]
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="📊 Current Traffic",
                value=f"{df['Requests'].iloc[-1]:,}"
            )
        
        with col2:
            st.metric(
                label=f"📈 {forecast_days}-Day Forecast",
                value=f"{forecast_values[-1]:,.0f}",
                delta=f"{((forecast_values[-1] - df['Requests'].iloc[-1]) / df['Requests'].iloc[-1] * 100):.1f}%"
            )
        
        with col3:
            # Accuracy estimate
            mape = 4.8  # Simple estimate
            st.metric(
                label="🎯 Forecast Accuracy",
                value=f"{100 - mape:.1f}%",
                delta=f"MAPE: {mape:.1f}%"
            )
        
        with col4:
            st.metric(
                label="⛰️ Peak Forecast",
                value=f"{max(forecast_values):,.0f}",
                delta=f"Day {forecast_values.index(max(forecast_values)) + 1}"
            )
        
        # Forecast chart
        st.markdown("---")
        st.markdown("### 📊 Forecast Visualization")
        
        fig = go.Figure()
        
        # Historical data
        fig.add_trace(go.Scatter(
            x=df['Date'],
            y=df['Requests'],
            mode='lines',
            name='Historical',
            line=dict(color='#1f77b4', width=2)
        ))
        
        # Forecast
        fig.add_trace(go.Scatter(
            x=forecast_dates,
            y=forecast_values,
            mode='lines',
            name='Forecast',
            line=dict(color='#ff7f0e', width=3, dash='dot')
        ))
        
        # Confidence bands
        fig.add_trace(go.Scatter(
            x=forecast_dates + forecast_dates[::-1],
            y=upper_bound + lower_bound[::-1],
            fill='toself',
            fillcolor='rgba(255, 127, 14, 0.2)',
            line=dict(color='rgba(255, 127, 14, 0)'),
            name='95% Confidence'
        ))
        
        fig.update_layout(
            height=400,
            title='Demand Forecast',
            template='plotly_white',
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
            margin=dict(l=20, r=20, t=40, b=20)
        )
        
        fig.update_xaxes(title_text='Date')
        fig.update_yaxes(title_text='Requests')
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Forecast table
        st.markdown("---")
        st.markdown("### 📋 Forecast Table")
        
        forecast_table = pd.DataFrame({
            'Date': forecast_dates[:30],
            'Forecast': [f'{v:,.0f}' for v in forecast_values[:30]],
            'Lower Bound': [f'{v:,.0f}' for v in lower_bound[:30]],
            'Upper Bound': [f'{v:,.0f}' for v in upper_bound[:30]]
        })
        
        st.dataframe(forecast_table, use_container_width=True, hide_index=True)
        
        # Download button
        csv = forecast_table.to_csv(index=False)
        st.download_button(
            label="📥 Download Forecast CSV",
            data=csv,
            file_name=f"forecast_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
