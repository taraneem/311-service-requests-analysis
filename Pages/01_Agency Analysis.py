import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="Agency Analysis", page_icon="🏛")
st.title("Agency Analysis")
st.markdown("Agency Distribution and Resolution patterns")
st.divider()

import gdown  

@st.cache_data
def load_data():
    file_id = "1GZXw_sat1A0wTSMO-wyp72-shCnLaf_a"
    url = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(url, "nyc_featured.parquet", quiet=False)
    return pd.read_parquet("nyc_featured.parquet")

df = load_data()
df.columns = df.columns.str.lower()

# Standard Theme Colors
THEME_COLORS = ["#52AB98", "#3B5E64", "#2E4F4D", "#6CA5A4", "#74BAB8", "#274C4B"]

# Apply custom styling
st.markdown("""
<style>
    h1, h2, h3 { color: #52AB98 !important; font-weight: 700 !important; }
    .stTabs [data-baseweb="tab"] { color: #888; }
    .stTabs [aria-selected="true"] { color: #52AB98 !important; border-bottom-color: #52AB98 !important; }
    div[data-testid="stExpander"] { border: 1px solid rgba(82, 171, 152, 0.2); border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

# Filter borough and agency multiselect
boroughs = df['borough'].unique()
agencies = df['agency_name'].unique()

borough = st.sidebar.multiselect("Select Borough", boroughs)
agency = st.sidebar.multiselect("Select Agency", agencies)

if borough:
    df = df[df['borough'].isin(borough)]
if agency:
    df = df[df['agency_name'].isin(agency)]
    

tab1, tab2 = st.tabs(["Volume Analysis", "Response Time Analysis"])

with tab1:
    # top 10 agency handles the most complaints overall
    plot_df = df['agency_name'].value_counts().reset_index().head(10)
    fig = px.bar(plot_df , x='count', y='agency_name',title='Top 10 Agencies with the Highest Complaint Volume' , 
        labels={'count':'Number of Complaints' , 'agency_name':'Agency Name'}, color_discrete_sequence=[THEME_COLORS[0]], text_auto=True)
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color="#E0E0E0")
    st.plotly_chart(fig, use_container_width=True)

with tab2:
   # agency response time
    plot_df = df.groupby('agency_name')['response_time_hours'].mean().reset_index().sort_values(by='response_time_hours', ascending=False)
    fig= px.bar(plot_df, x='response_time_hours', y='agency_name',
       title='Average Response Time by Agency',
       labels={'response_time_hours': 'Average Response Time (Hours)', 
               'agency_name': 'Agency Name'},color_discrete_sequence=[THEME_COLORS[0]])
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color="#E0E0E0")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(""" **Key Insight :** The Department of Parks and Recreation has the highest average response 
time (~6000 hours ≈ 250 days) because park maintenance complaints are 
low urgency and require scheduled work crews. The NYPD responds fastest 
because most police complaints require immediate on-ground response.""")
    



