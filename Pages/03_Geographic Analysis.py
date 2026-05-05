import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="Geographic Analysis", page_icon="📍")
st.title("📍 Complaint Map")
st.markdown("Geospatial view of a sample of 311 service requests across the city.")
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
</style>
""", unsafe_allow_html=True)

# Filter aside to display filtered data in map
borough_options = ['All'] + sorted(df['borough'].unique())
complaint_options = ['All'] + sorted(df['complaint_type'].unique())

with st.sidebar:
    selected_borough = st.selectbox("Select Borough", borough_options)
    selected_complaint = st.selectbox("Select Complaint Type", complaint_options)
if selected_borough != 'All':
    df = df[df['borough'] == selected_borough]
if selected_complaint != 'All':
    df = df[df['complaint_type'] == selected_complaint]

st.markdown("### Complaint Hotspots Map")

sample = df.sample(5000 , replace=True)

fig = px.scatter_map(sample,
                  lat='latitude',
                  lon='longitude',
                  color='borough',
                  hover_name='complaint_type',
                  zoom=10,
                  height=600,
                  title='NYC 311 Complaint Hotspots',
                  map_style='carto-positron',
                  color_discrete_sequence=THEME_COLORS)
fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color="#E0E0E0")

st.plotly_chart(fig, use_container_width=True)
tab1 , tab2 = st.tabs(['Univariate Analysis' , 'Bivariate Analysis'])

with tab1:

# Top 15 street name with highest complaints
  st.markdown("### Top 15 Street Names with Highest Complaints")
  plot_df = df['street_name'].value_counts().reset_index().head(15)

  fig = px.bar(data_frame= plot_df, y='street_name', x='count'
        , labels={'street_name' : 'Street Name', 'count' :'Number of Complaints' } 
        , text_auto=True, title='Top 15 streets with the highest complaint volume', 
        color_discrete_sequence=[THEME_COLORS[0]])
  fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color="#E0E0E0")
  st.plotly_chart(fig, use_container_width=True)

with tab2:

# Borough with the highest response time

 st.markdown("### Borough with the Highest Response Time")
 plot_df= df.groupby('borough')['response_time_days'].mean().astype('int').reset_index().sort_values(by='response_time_days')

 fig = px.bar(data_frame=plot_df, x='borough', y='response_time_days', title='Average Response Time in Days',
                             labels={'borough':'Borough Name' , 'response_time_days' : 'Average response time'}, 
                             text_auto=True , color_discrete_sequence=[THEME_COLORS[0]])
 fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color="#E0E0E0")
 st.plotly_chart(fig, use_container_width=True)

 # Hotspot ZIP Codes
 st.markdown("### Hotspot ZIP Codes")
 plot_df = df.groupby(['borough', 'incident_zip']).size().reset_index(name='count')
 plot_df = plot_df.sort_values(['borough', 'count'] , ascending=False)
 plot_df = plot_df.groupby('borough').head(1)

 fig =px.bar(data_frame= plot_df, x='incident_zip', color='borough',y ='count'
        , labels={'incident_zip' : 'Incident ZIP Code', 'borough' :'borough Name' } , text_auto=True,
        title='The most ZIP codes that generate complaints within each borough?',
        color_discrete_sequence=THEME_COLORS
        )
 fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color="#E0E0E0")
 st.plotly_chart(fig, use_container_width=True)

 # Top 3 complaints in each borough

 st.markdown("### Top 3 Complaints in each Borough")
 plot_df = df.groupby(['borough', 'complaint_type']).size().reset_index(name='count')
 plot_df = plot_df.sort_values(['borough' , 'count'] , ascending=False)
 plot_df = plot_df.groupby('borough').head(3)

 fig=px.bar(plot_df, y='borough', x='count', color='complaint_type',
             barmode='group', 
             title='The most dominant complaint type per borough',
             labels={'borough': 'Borough Name', 'count': 'Number of complaints' , 'color': 'Complaint Type'},
             text_auto=True , color_discrete_sequence=THEME_COLORS)
 fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color="#E0E0E0")
 st.plotly_chart(fig, use_container_width=True)

# reporting channel (Phone/Mobile/Online) differ across boroughs

 st.markdown("### Reporting Channel (Phone/Mobile/Online) Differ Across Boroughs")
 plot_df = df.groupby(['borough', 'open_data_channel_type']).size().reset_index(name='count')
 plot_df = plot_df.sort_values(['borough' , 'count'] , ascending=False)
 plot_df = plot_df.groupby('borough').head(3)

 fig = px.bar(plot_df, y='borough', x='count', color='open_data_channel_type',
             barmode='group', 
             title='Reporting Method Distribution',
             labels={'borough': 'Borough Name', 'count': 'Usage Number'},
             text_auto=True , color_discrete_sequence=THEME_COLORS)
 fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color="#E0E0E0")
 st.plotly_chart(fig, use_container_width=True)
