import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(layout="wide", page_title="Complaint Analysis", page_icon="📝")
st.title("Complaint Analysis")
st.markdown("Complaints Analysis and Status patterns")
st.divider()

@st.cache_data
def load_data():
    return pd.read_parquet("nyc_sample.parquet")

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

tab1, tab2, tab3 = st.tabs(["Distributions", "Response Times & Status", "Temporal Trends"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        # Complaint Distribution
        plot_df = df['complaint_type'].value_counts().head(15).reset_index(name='count')
        fig = px.treemap(plot_df,
                   path=['complaint_type'],
                   values='count',
                   title='Complaint Type Distribution — Treemap',
                   color='count',
                   color_continuous_scale='Teal')
        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color="#E0E0E0")
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        # top 10 most frequent complaint types across all of NYC
        plot_df = df['complaint_type'].value_counts().reset_index(name='count').head(10)
        fig= px.bar(data_frame= plot_df , y='complaint_type', x='count' , text_auto=True, color_discrete_sequence= [THEME_COLORS[0]] ,
               title='Top 10 Complaint Types occurring in NYC', labels={'complaint_type':'Complaint Type' , 'count':'Number of Complaints'})
        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color="#E0E0E0")
        st.plotly_chart(fig, use_container_width=True)

    # What is the distribution of complaint details within the top 5 complaint type?
    top_types = df['complaint_type'].value_counts().head(5).index
    plot_df = df[df['complaint_type'].isin(top_types)]
    plot_df = plot_df.groupby(['complaint_type','complaint_detail']).size().reset_index(name='count')
    plot_df = plot_df.sort_values('count', ascending=False).groupby('complaint_type').head(3)
    
    fig=px.bar(data_frame= plot_df , y='complaint_detail', x='count' , color='complaint_type',title='Complaint Types and Details Distribution',color_discrete_sequence=THEME_COLORS,
                 labels={'complaint_detail':'Complaint Detail' , 'count':'Number of Complaints' , 'complaint_type':'Complaint Type'})
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color="#E0E0E0")
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    col3, col4 = st.columns(2)
    with col3:
        # average response time per complaint type
        plot_df = df.groupby('complaint_type')['response_time_hours'].mean().round(2).reset_index().sort_values(by='response_time_hours', ascending=False).head(10)
        fig=px.bar(plot_df, x='response_time_hours', y='complaint_type',title='Average Response Time by Complaint Type',
               labels={'response_time_hours':'Average Response Time (Hours)','complaint_type':'Complaint Type'} ,color_discrete_sequence= [THEME_COLORS[0]] , text_auto=True)
        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color="#E0E0E0")
        st.plotly_chart(fig, use_container_width=True)
        
    with col4:
        # 10 complaint types remain Open the longest without resolution
        filtered_df = df[df['status'] == 'Open']
        plot_df = filtered_df['complaint_type'].value_counts().reset_index(name='count').head(10)
        fig = px.bar(plot_df , x='count' , y='complaint_type', title='Top 10 Open Complaints',
               labels={'count':'Number of Complaints' , 'complaint_type':'Complaint Type'}, color_discrete_sequence= [THEME_COLORS[0]] , text_auto=True)
        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color="#E0E0E0")
        st.plotly_chart(fig, use_container_width=True)
        
    # What is the overall distribution of complaint status (Open/Closed/Pending)?
    plot_df = df['status'].value_counts().reset_index(name='count')
    fig = px.pie(plot_df , names='status', values='count', title='Distribution of Complaint Statuses', color_discrete_sequence=THEME_COLORS)
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color="#E0E0E0")
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    * The pie chart above shows that the majority of complaints are closed, which is a positive sign that the city is addressing the issues raised by residents. However, there is still a significant portion of complaints that are open, 
    indicating that there may be room for improvement in the city's response time and resolution process.
    """)

with tab3:
    # How many complaints were created on average each day over the 2022 - 2023 ?
    plot_df = df.groupby('created_date')['complaint_type'].count().reset_index(name='count')
    fig = px.line(plot_df , x='created_date' , y='count', title='Complaints per Day over 2022 - 2023',
           labels={'count':'Number of Complaints' , 'created_date':'Complaint Created Date'}, color_discrete_sequence= [THEME_COLORS[0]])
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color="#E0E0E0")
    st.plotly_chart(fig, use_container_width=True)
