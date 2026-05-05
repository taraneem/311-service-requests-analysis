import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="NYC 311 Service Requests Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom styling for a premium feel
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Primary colors */
    :root {
        --primary-teal: #52AB98;
        --dark-teal: #3B5E64;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: var(--primary-teal) !important;
        font-weight: 700 !important;
    }
    
    h4, h5, h6 {
        color: #A0AEC0 !important;
    }

    /* Metrics styling */
    div[data-testid="stMetric"] {
        background-color: rgba(59, 94, 100, 0.05);
        border: 1px solid rgba(82, 171, 152, 0.2);
        padding: 20px;
        border-radius: 12px;
        transition: all 0.3s ease;
    }
    
    div[data-testid="stMetric"]:hover {
        border-color: var(--primary-teal);
        transform: translateY(-2px);
        background-color: rgba(59, 94, 100, 0.1);
    }
    
    div[data-testid="stMetricValue"] {
        color: var(--primary-teal) !important;
        font-weight: 800 !important;
        font-size: 1.5rem !important;
        line-height: 1.2 !important;
    }
    
    /* Info Box */
    .info-box {
        background: linear-gradient(145deg, rgba(59, 94, 100, 0.1), rgba(82, 171, 152, 0.05));
        border-left: 4px solid var(--primary-teal);
        padding: 25px;
        border-radius: 8px;
        margin: 10px 0;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        border-right: 1px solid rgba(82, 171, 152, 0.1);
    }

    /* Buttons & Interactive */
    .stButton>button {
        background-color: var(--dark-teal);
        color: white;
        border-radius: 8px;
        border: none;
    }
</style>
""", unsafe_allow_html=True)

import gdown  

@st.cache_data
def load_data():
    file_id = "1GZXw_sat1A0wTSMO-wyp72-shCnLaf_a"
    url = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(url, "nyc_featured.parquet", quiet=False)
    return pd.read_parquet("nyc_featured.parquet")

# Standard Theme Colors
THEME_COLORS = ["#3B5E64", "#52AB98", "#2E4F4D", "#6CA5A4", "#74BAB8", "#274C4B"]

try:
    df = load_data()
    
    # Filters
    boroughs = df['borough'].unique()
    borough = st.sidebar.multiselect("Select Borough", boroughs)
    if borough:
        df = df[df['borough'].isin(borough)]
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# --- HEADER SECTION ---
st.markdown("<h1>NYC 311 Service Requests Analysis</h1>", unsafe_allow_html=True)
st.markdown("#### Exploring 2.9M+ real-world civic complaints across New York City's five boroughs")
st.markdown("<hr style='border: 1px solid #3B5E64; opacity: 0.3;'>", unsafe_allow_html=True)
st.write("")

# --- ABOUT SECTION ---
st.markdown("### About This Project")
col1, col2 = st.columns([3, 2])

with col1:
    st.markdown("""
    NYC 311 is the primary access point for non-emergency municipal services in New York City. 
    This project deeply analyzes these service requests to uncover patterns in urban challenges, 
    agency responsiveness, and geographic disparities. By understanding how the city's inhabitants 
    interact with their government, we can identify areas for infrastructural improvement and 
    resource optimization. 
    
    **What if Cairo had a 311 system?** Imagine applying this level of data-driven transparency 
    to urban management in Cairo, allowing citizens to report issues and tracking municipal response 
    in real-time to build a more responsive city ecosystem.
    """)

with col2:
    st.markdown("""
    <div class="info-box">
        <h4>📊 Dataset Facts</h4>
        <b>Source:</b> NYC Open Data<br>
        <b>Records:</b> 2.9M+ service requests<br>
        <b>Period:</b> June 2022 — June 2023<br>
        <b>Boroughs:</b> 5 NYC Boroughs<br>
        <b>Columns Used:</b> 16 out of 44 raw columns
    </div>
    """, unsafe_allow_html=True)

st.write("---")

# --- KPI METRICS SECTION ---
st.markdown("### Dataset At A Glance")

# Calculate metrics dynamically
total_complaints = len(df)
avg_response_time = round(df['response_time_days'].mean(), 1) if 'response_time_days' in df.columns else "N/A"
busiest_borough = df['borough'].value_counts().index[0] if 'borough' in df.columns else "N/A"
top_complaint = df['complaint_type'].value_counts().index[0] if 'complaint_type' in df.columns else "N/A"

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric(label="Total Complaints", value=f"{total_complaints:,}")
with kpi2:
    st.metric(label="Avg Response Time", value=f"{avg_response_time} days")
with kpi3:
    st.metric(label="Busiest Borough", value=str(busiest_borough).title())

with kpi4:
    st.metric(label="Top Complaint Type", value=str(top_complaint))
st.write("---")

# --- OVERVIEW CHART SECTION ---
st.subheader("Complaint Distribution by Borough")

if 'borough' in df.columns:
    borough_counts = df['borough'].value_counts().reset_index()
    borough_counts.columns = ['Borough', 'Complaints']
    
    fig = px.bar(
        borough_counts,
        x='Complaints',
        y='Borough',
        orientation='h',
        color_discrete_sequence=[THEME_COLORS[0]],
        text='Complaints'
    )
    
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis_title="Number of Complaints",
        yaxis_title="Borough Name",
        yaxis={'categoryorder':'total ascending'},
        font_color="#E0E0E0",
        margin=dict(l=20, r=20, t=20, b=20)
    )
    fig.update_traces(
        texttemplate='%{text:.2s}', 
        textposition='outside',
        marker_color="#52AB98"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Insight
    st.markdown(f"**Insight:** **{str(busiest_borough).title()}** leads the city in total volume of 311 service requests during this period.")

# --- NAVIGATION HINT SECTION ---
st.markdown("""
<div class="nav-box">
    🧭 Use the sidebar to navigate through Geographic, Temporal, Agency, Channel, and Complaint Type analysis pages
</div>
""", unsafe_allow_html=True)
