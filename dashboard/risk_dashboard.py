import streamlit as st
import pandas as pd
import plotly.graph_objects as go

class RiskDashboard:
    """Assumptions and Risk dashboard"""
    
    def render(self, data: dict):
        """Render the risk dashboard"""
        st.markdown("## ⚠️ Assumptions & Risk Management")
        st.caption("Comprehensive risk assessment")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="📊 Assumptions",
                value="7",
                delta="Documented"
            )
        
        with col2:
            st.metric(
                label="⚠️ Active Risks",
                value="6",
                delta="3 High Priority"
            )
        
        with col3:
            st.metric(
                label="🔴 High/Critical Risks",
                value="3",
                delta="2 High, 1 Critical"
            )
        
        with col4:
            st.metric(
                label="🎯 Confidence Level",
                value="78%",
                delta="High"
            )
        
        # Scenarios
        st.markdown("---")
        st.markdown("### 📊 Scenarios")
        
        col1, col2, col3 = st.columns(3)
        
        scenarios = {
            'Expected': {'growth': '15%', 'cost': '1.0x', 'confidence': '70%', 'color': '🟢'},
            'Best Case': {'growth': '25%', 'cost': '0.95x', 'confidence': '30%', 'color': '🟦'},
            'Worst Case': {'growth': '5%', 'cost': '1.3x', 'confidence': '30%', 'color': '🔴'}
        }
        
        for i, (name, details) in enumerate(scenarios.items()):
            with [col1, col2, col3][i]:
                st.markdown(f"#### {details['color']} {name}")
                st.metric("Growth Rate", details['growth'])
                st.metric("Cost Multiplier", details['cost'])
                st.metric("Confidence", details['confidence'])
        
        # Risk Matrix
        st.markdown("---")
        st.markdown("### 🎯 Risk Matrix")
        
        # Create a simple risk matrix
        risk_data = [
            ['High', 'Medium', 'Low'],
            ['High', 1, 2, 1],
            ['Medium', 2, 1, 0],
            ['Low', 0, 1, 1]
        ]
        
        fig = go.Figure(data=go.Heatmap(
            z=[[1, 2, 1], [2, 1, 0], [0, 1, 1]],
            x=['Low', 'Medium', 'High'],
            y=['Low', 'Medium', 'High'],
            colorscale='RdYlGn_r',
            showscale=True,
            text=[[1, 2, 1], [2, 1, 0], [0, 1, 1]],
            texttemplate='%{text}',
            textfont={"size": 20, "color": "black"}
        ))
        
        fig.update_layout(
            height=400,
            title='Risk Matrix',
            template='plotly_white',
            xaxis_title='Probability',
            yaxis_title='Impact',
            margin=dict(l=20, r=20, t=40, b=20)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Risk list
        st.markdown("---")
        st.markdown("### 📋 Risk Details")
        
        risks = [
            {"Risk": "Demand Forecasting Error", "Impact": "High", "Probability": "30%", "Status": "Active"},
            {"Risk": "Cloud Cost Overrun", "Impact": "High", "Probability": "40%", "Status": "Active"},
            {"Risk": "Infrastructure Capacity Shortage", "Impact": "Critical", "Probability": "25%", "Status": "Active"},
            {"Risk": "Seasonal Demand Mismatch", "Impact": "Medium", "Probability": "35%", "Status": "Active"},
            {"Risk": "Data Quality Issues", "Impact": "Medium", "Probability": "20%", "Status": "Active"},
            {"Risk": "Competitive Market Changes", "Impact": "High", "Probability": "40%", "Status": "Active"}
        ]
        
        risk_df = pd.DataFrame(risks)
        st.dataframe(risk_df, use_container_width=True, hide_index=True)
        
        # Mitigation recommendations
        st.markdown("---")
        st.markdown("### 🛡️ Mitigation Recommendations")
        
        mitigations = [
            {"Priority": "🔴 High", "Risk": "Infrastructure Capacity Shortage", 
             "Mitigation": "Implement autoscaling, add capacity buffers, regular load testing"},
            {"Priority": "🟠 Medium", "Risk": "Cloud Cost Overrun", 
             "Mitigation": "Implement cost alerts, optimize resource usage, reserved instances"},
            {"Priority": "🟡 Low", "Risk": "Data Quality Issues", 
             "Mitigation": "Data validation, automated cleaning, anomaly detection"}
        ]
        
        for m in mitigations:
            st.markdown(f"""
            **{m['Priority']} - {m['Risk']}**
            - **Mitigation:** {m['Mitigation']}
            ---
            """)
