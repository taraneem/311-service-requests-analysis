import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="Reporting Method Analysis", page_icon="📉")
st.title("Reporting Method")
st.markdown("Complaint Reporting Methods and Distribution")
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
</style>
""", unsafe_allow_html=True)

# Filters
boroughs = df['borough'].unique()
borough = st.sidebar.multiselect("Select Borough", boroughs)

if borough:
    df = df[df['borough'].isin(borough)]

col1, col2 = st.columns(2)

with col1:
    # overall split between Phone, Mobile, Online, and other channels
    plot_df = df['open_data_channel_type'].value_counts().reset_index(name='count')
    fig= px.pie(plot_df, names='open_data_channel_type', values='count', title='Reporting Channel Distribution'
     , color_discrete_sequence= THEME_COLORS)
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color="#E0E0E0")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Has mobile reporting grown over time while phone reporting declined?
    month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']
    
    plot_df = df.groupby(['complaint_month', 'open_data_channel_type']).size().reset_index(name='count')
    plot_df = plot_df[plot_df['open_data_channel_type'].isin(['PHONE', 'MOBILE'])]
    plot_df['complaint_month'] = pd.Categorical(
        plot_df['complaint_month'], categories=month_order, ordered=True
    )
    plot_df = plot_df.sort_values('complaint_month').reset_index(drop=True)
    
    fig= px.line(plot_df, x='complaint_month', y='count',
            color='open_data_channel_type',
            title='Mobile vs Phone Reporting Over Time',
            labels={'complaint_month': 'Month', 
                    'count': 'Number of Complaints',
                    'open_data_channel_type': 'Channel'},
            markers=True,
            color_discrete_sequence=THEME_COLORS,
            template='plotly')
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color="#E0E0E0")
    st.plotly_chart(fig, use_container_width=True)

st.divider()
col3, col4 = st.columns(2)

with col3:
    # Which borough is most digitally engaged (highest mobile/online ratio)?
    filtered_df = df[(df['open_data_channel_type'] == 'MOBILE') | (df['open_data_channel_type'] == 'ONLINE')]
    plot_df = filtered_df.groupby(['borough']).size().reset_index(name='count')
    fig = px.bar(plot_df, y='borough', x='count', title='Complaint Volume by Borough for Mobile and Online Reports',
           labels={'borough': 'Borough Name', 'count': 'Number of Complaints'}, color_discrete_sequence=[THEME_COLORS[0]] ,text_auto=True
           )
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color="#E0E0E0")
    st.plotly_chart(fig, use_container_width=True)

with col4:
    # Which complaint types are most reported via mobile vs phone?
    filtered_df = df[(df['open_data_channel_type'] == 'MOBILE') | (df['open_data_channel_type'] == 'PHONE')]
    plot_df = filtered_df.groupby(['complaint_type', 'open_data_channel_type']).size().reset_index(name='count')
    plot_df = plot_df.sort_values(['open_data_channel_type', 'count'], ascending=False)
    plot_df = plot_df.groupby('open_data_channel_type').head(5)
    fig= px.bar(plot_df, x='count', y='complaint_type', color='open_data_channel_type',
           barmode='group',
           title='Top Complaint Types by Reporting Channel (Mobile vs Phone)' , color_discrete_sequence= THEME_COLORS,
           labels={'count':'Number of Complaints' , 'complaint_type':'Complaint Type' , 'open_data_channel_type':'Reporting Channel'})
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color="#E0E0E0")
    st.plotly_chart(fig, use_container_width=True)