import streamlit as st
import pandas as pd
import os

st.title("Data Test")

# Check data directory
st.write("Current directory:", os.getcwd())
st.write("Data directory exists:", os.path.exists('data'))

if os.path.exists('data'):
    files = os.listdir('data')
    st.write("Files in data:", files)
    
    for f in files:
        if f.endswith('.csv'):
            try:
                df = pd.read_csv(f'data/{f}')
                st.write(f"✅ {f}: {len(df)} rows")
                st.dataframe(df.head())
            except Exception as e:
                st.error(f"Error loading {f}: {e}")
else:
    st.error("Data directory not found!")
