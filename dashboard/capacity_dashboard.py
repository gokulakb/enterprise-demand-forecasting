import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

class CapacityDashboard:
    """Capacity Planning dashboard"""
    
    def render(self, data: dict, growth_multiplier: float):
        """Render the capacity planning dashboard"""
        st.markdown("## 🖥️ Capacity Planning")
        st.caption("Infrastructure capacity analysis")
        
        infra_df = data['infrastructure']
        latest = infra_df.iloc[-1]
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="🖥️ CPU Usage",
                value=f"{latest['CPU']:.1f}%",
                delta=f"{min(100, latest['CPU'] * growth_multiplier):.1f}% at {growth_multiplier}x"
            )
        
        with col2:
            st.metric(
                label="🧠 Memory Usage",
                value=f"{latest['Memory']:.1f}%",
                delta=f"{min(100, latest['Memory'] * growth_multiplier):.1f}% at {growth_multiplier}x"
            )
        
        with col3:
            st.metric(
                label="💾 Storage Usage",
                value=f"{latest['Storage']:.1f}%",
                delta=f"{min(100, latest['Storage'] * growth_multiplier):.1f}% at {growth_multiplier}x"
            )
        
        with col4:
            st.metric(
                label="📡 Bandwidth",
                value=f"{latest['Bandwidth']:.1f} Mbps",
                delta=f"{latest['Bandwidth'] * growth_multiplier:.1f} Mbps at {growth_multiplier}x"
            )
        
        # Resource utilization chart
        st.markdown("---")
        st.markdown("### 📊 Resource Utilization")
        
        fig = go.Figure()
        
        metrics = ['CPU', 'Memory', 'Storage', 'Bandwidth']
        current_values = [latest[m] for m in metrics]
        projected_values = [min(100, latest[m] * growth_multiplier) for m in metrics]
        
        fig.add_trace(go.Bar(
            name='Current',
            x=metrics,
            y=current_values,
            marker_color='#1f77b4'
        ))
        
        fig.add_trace(go.Bar(
            name=f'{growth_multiplier}x Growth',
            x=metrics,
            y=projected_values,
            marker_color='#ff7f0e'
        ))
        
        fig.update_layout(
            height=400,
            title='Resource Utilization - Current vs Projected',
            template='plotly_white',
            barmode='group',
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
            margin=dict(l=20, r=20, t=40, b=20)
        )
        
        fig.update_yaxes(title_text='Utilization (%)', range=[0, 100])
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Recommendations
        st.markdown("---")
        st.markdown("### 🔄 Recommendations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📊 Current Status")
            status = "🟢 Good" if latest['CPU'] < 70 else "🟡 Warning" if latest['CPU'] < 85 else "🔴 Critical"
            st.metric("CPU Status", status)
            
            status = "🟢 Good" if latest['Memory'] < 70 else "🟡 Warning" if latest['Memory'] < 85 else "🔴 Critical"
            st.metric("Memory Status", status)
        
        with col2:
            st.markdown("#### 📈 Projected Needs")
            servers_needed = int(latest['Servers'] * growth_multiplier)
            st.metric(
                "Servers Required",
                f"{servers_needed}",
                delta=f"{servers_needed - latest['Servers']} additional"
            )
            
            if latest['CPU'] * growth_multiplier > 80:
                st.warning("⚠️ CPU will exceed 80% at this growth rate")
            else:
                st.success("✅ CPU within acceptable range")
