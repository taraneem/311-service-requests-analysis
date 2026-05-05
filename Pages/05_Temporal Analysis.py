import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="Temporal Analysis", page_icon="📅")
st.title("Temporal Analysis")
st.markdown("Temporal patterns of 311 service requests across the city.")
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

# Filters
boroughs = df['borough'].unique()
borough = st.sidebar.multiselect("Select Borough", boroughs)

if borough:
    df = df[df['borough'].isin(borough)]

tab1 , tab2 = st.tabs(["Univariate Trends Analysis", "Bivariate Trends Analysis"])

with tab1:
    # complaint volume change month by month
    month_order = ['January', 'February', 'March', 'April', 'May', 'June',
               'July', 'August', 'September', 'October', 'November', 'December']

    plot_df = df['complaint_month'].value_counts().reset_index(name='count')
    plot_df['complaint_month'] = pd.Categorical(
    plot_df['complaint_month'], categories=month_order, ordered=True
     )
    plot_df = plot_df.sort_values('complaint_month').reset_index(drop=True)
    fig =px.line(plot_df, x='complaint_month', y='count',
        title='Monthly Complaint Volume Over Time',
        markers=True,
        color_discrete_sequence=[THEME_COLORS[0]],
        template='plotly' )
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color="#E0E0E0")
    st.plotly_chart(fig, use_container_width=True)

    col1,col2 = st.columns(2)
    with col1:
    # Day receives most complaint
     plot_df = df['complaint_day'].value_counts().reset_index(name='count')
     day_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
     plot_df['complaint_day'] = pd.Categorical(plot_df['complaint_day'], categories=day_order, ordered=True)
     plot_df = plot_df.sort_values('complaint_day')

     fig= px.bar(plot_df , y='complaint_day', x='count' , title='Complaints by Day of the Week',
             text_auto=True, labels={'complaint_day' : 'Day' , 'count' :'Number of Complaints'} 
             , color_discrete_sequence=[THEME_COLORS[0]])
     fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color="#E0E0E0")
     st.plotly_chart(fig, use_container_width=True)

     with col2:
    # Period of the day with most complaints
      plot_df = df['complaint_period'].value_counts().reset_index(name='count')
      fig= px.pie(data_frame= plot_df ,  names='complaint_period' , values='count' , title='Complaints by the Period of the day' 
     ,color_discrete_sequence=THEME_COLORS)
      fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color="#E0E0E0")
      st.plotly_chart(fig, use_container_width=True)

with tab2:
  plot_df = df.groupby(['borough', 'complaint_hour']).size().reset_index(name='count')
  fig= px.line(plot_df, x='complaint_hour', y='count',
        color='borough',
        title='Complaint Volume by Hour Across Boroughs',
        labels={'complaint_hour': 'Hour of Day', 'count': 'Number of Complaints'},
        markers=True,
        color_discrete_sequence=THEME_COLORS,
        template='plotly')
  fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color="#E0E0E0")
  st.plotly_chart(fig, use_container_width=True)

  st.markdown("""
  **Key Insights:**
  - Complaints drop to their lowest point between 3-5 AM across all boroughs,
  then rise sharply as the city wakes up, peaking around 9 AM.
  - Brooklyn consistently leads in complaint volume at every hour of the day.
  - Staten Island remains the quietest borough throughout.
  """)

  # Day + period combination has the highest complaint density
  day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
  period_order = ['Morning', 'Afternoon', 'Evening', 'Night']

  plot_df = df.groupby(['complaint_day', 'complaint_period']).size().reset_index(name='count')


  pivot = plot_df.pivot(index='complaint_day', columns='complaint_period', values='count')

  pivot = pivot.reindex(index=day_order, columns=period_order)

  fig= px.imshow(pivot,
          title='Complaint Density by Day and Period',
          labels={'x': 'Period of Day', 'y': 'Day of Week', 'color': 'Count'},
          aspect='auto',
          color_continuous_scale='Teal')
  fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color="#E0E0E0")
  st.plotly_chart(fig, use_container_width=True)





    



