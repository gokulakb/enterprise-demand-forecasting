"""
Enterprise Demand Forecasting Platform
Main application entry point
"""

import streamlit as st
import pandas as pd
import logging
from datetime import datetime
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Enterprise Demand Forecasting",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 600;
        color: #2c3e50;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_data():
    """Load all data"""
    from utils.loader import DataLoader
    loader = DataLoader()
    data = loader.load_all_data()
    return data

def main():
    """Main application entry point"""
    
    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/analytics.png", width=80)
        st.title("📊 Demand Forecasting")
        st.markdown("---")
        
        # Navigation
        pages = {
            "🏠 Executive Overview": "overview",
            "📈 Demand Forecast": "forecast",
            "🖥️ Capacity Planning": "capacity",
            "💰 Cost Projection": "cost",
            "⚠️ Assumptions & Risk": "risk"
        }
        
        selected_page = st.radio("Navigate to:", list(pages.keys()))
        page = pages[selected_page]
        
        st.markdown("---")
        
        if st.button("🔄 Reload Data"):
            st.cache_resource.clear()
            st.rerun()
        
        st.markdown("---")
        
        # Filters
        st.subheader("🔍 Filters")
        
        data = load_data()
        
        forecast_days = st.slider(
            "Forecast Horizon (Days)",
            min_value=30,
            max_value=365,
            value=90,
            step=30
        )
        
        growth_multiplier = st.slider(
            "Growth Multiplier",
            min_value=1.0,
            max_value=10.0,
            value=2.0,
            step=0.5
        )
        
        st.markdown("---")
        st.caption("© 2024 Enterprise Forecasting Platform")
    
    # Main content
    st.markdown('<div class="main-header">📊 Enterprise Demand Forecasting Platform</div>', unsafe_allow_html=True)
    
    # Check data
    if not data or 'traffic' not in data or data['traffic'].empty:
        st.error("❌ No data available. Please check data files.")
        return
    
    # Show some basic data to confirm it's working
    st.success(f"✅ Data loaded successfully! {len(data['traffic'])} traffic records found.")
    
    # Show sample data
    with st.expander("📊 View Sample Data"):
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Traffic Data")
            st.dataframe(data['traffic'].head(10))
        with col2:
            st.subheader("Applications Data")
            if 'applications' in data:
                st.dataframe(data['applications'].head(10))
    
    # Page routing
    if page == "overview":
        show_overview(data, forecast_days, growth_multiplier)
    elif page == "forecast":
        show_forecast(data, forecast_days)
    elif page == "capacity":
        show_capacity(data, growth_multiplier)
    elif page == "cost":
        show_cost(data, growth_multiplier)
    elif page == "risk":
        show_risk(data)

def show_overview(data, forecast_days, growth_multiplier):
    """Display executive overview dashboard"""
    try:
        from dashboard.overview import OverviewDashboard
        dashboard = OverviewDashboard()
        dashboard.render(data, forecast_days, growth_multiplier)
    except Exception as e:
        st.error(f"Error loading overview: {e}")
        import traceback
        st.code(traceback.format_exc())

def show_forecast(data, forecast_days):
    """Display demand forecast dashboard"""
    try:
        from dashboard.forecast import ForecastDashboard
        dashboard = ForecastDashboard()
        dashboard.render(data, forecast_days)
    except Exception as e:
        st.error(f"Error loading forecast: {e}")

def show_capacity(data, growth_multiplier):
    """Display capacity planning dashboard"""
    try:
        from dashboard.capacity_dashboard import CapacityDashboard
        dashboard = CapacityDashboard()
        dashboard.render(data, growth_multiplier)
    except Exception as e:
        st.error(f"Error loading capacity: {e}")

def show_cost(data, growth_multiplier):
    """Display cost projection dashboard"""
    try:
        from dashboard.cost_dashboard import CostDashboard
        dashboard = CostDashboard()
        dashboard.render(data, growth_multiplier)
    except Exception as e:
        st.error(f"Error loading cost: {e}")

def show_risk(data):
    """Display assumptions and risk dashboard"""
    try:
        from dashboard.risk_dashboard import RiskDashboard
        dashboard = RiskDashboard()
        dashboard.render(data)
    except Exception as e:
        st.error(f"Error loading risk: {e}")

if __name__ == "__main__":
    main()
