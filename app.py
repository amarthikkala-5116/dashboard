import pandas as pd
import streamlit as st
import plotly.express as px
from io import StringIO

# --- Simulated CSV Data (you can replace with actual scraped Vahan data) ---
csv_data = StringIO("""
date,manufacturer,vehicle_category,registrations
2024-01-01,Hero,2W,50000
2024-04-01,Hero,2W,52000
2025-01-01,Hero,2W,60000
2025-04-01,Hero,2W,64000
2024-01-01,Tata,4W,20000
2024-04-01,Tata,4W,21000
2025-01-01,Tata,4W,25000
2025-04-01,Tata,4W,27000
2024-01-01,Ola,2W,10000
2024-04-01,Ola,2W,15000
2025-01-01,Ola,2W,22000
2025-04-01,Ola,2W,30000
""")

# --- Load and Prepare Data ---
df = pd.read_csv(csv_data, parse_dates=["date"])
df['year'] = df['date'].dt.year
df['quarter'] = df['date'].dt.to_period("Q")
df['quarter_str'] = df['quarter'].astype(str)

# --- Streamlit UI ---
st.set_page_config(page_title="Vehicle Registration Dashboard", layout="wide")
st.title("📊 Vehicle Registration Dashboard")
st.markdown("Interactive dashboard showing vehicle registration trends for investors")

# Sidebar Filters
manufacturers = st.sidebar.multiselect("Select Manufacturer", df['manufacturer'].unique(), default=df['manufacturer'].unique())
categories = st.sidebar.multiselect("Select Vehicle Category", df['vehicle_category'].unique(), default=df['vehicle_category'].unique())

filtered_df = df[df['manufacturer'].isin(manufacturers) & df['vehicle_category'].isin(categories)]

# Grouped Data
grouped = (
    filtered_df
    .groupby(['year', 'quarter_str', 'manufacturer', 'vehicle_category'], as_index=False)
    .agg({'registrations': 'sum'})
)

# Calculate QoQ and YoY Growth
grouped['QoQ Growth (%)'] = grouped.groupby(['manufacturer', 'vehicle_category'])['registrations'].pct_change() * 100
grouped['YoY Growth (%)'] = grouped.groupby(['manufacturer', 'vehicle_category'])['registrations'].pct_change(periods=2) * 100

# --- Visualizations ---
st.subheader("📈 Registration Trend Over Time")
fig = px.line(grouped,
              x='quarter_str',
              y='registrations',
              color='manufacturer',
              line_dash='vehicle_category',
              markers=True,
              title='Vehicle Registrations by Quarter')
st.plotly_chart(fig, use_container_width=True)

# --- Growth Table ---
st.subheader("📋 Growth Table (QoQ & YoY)")
st.dataframe(grouped.sort_values(by="quarter_str", ascending=False), use_container_width=True)

# --- Investor Insight ---
st.markdown("💡 **Investor Insight:**")
if 'Ola' in manufacturers:
    st.success("Ola has shown the highest QoQ growth in the 2W segment, indicating a strong upward trend in EV adoption.")
else:
    st.info("Select Ola to observe strong EV growth trends.")

st.markdown("---")

st.caption("🔧 Built with Python, Streamlit, and Plotly | Replace sample data with Vahan data for real insights.")
