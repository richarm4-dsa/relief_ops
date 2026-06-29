# DSA506 Visual Analytics and Communications  
# Michelle Richardson  
# Test 1  

# Dashboard

import numpy as np
import pandas as pd
from pathlib import Path
import plotly.express as px
import folium
import streamlit as st
from streamlit_folium import st_folium
from folium.plugins import HeatMap
from IPython.display import display, IFrame
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent

# Build the absolute path to your Data folder
#data_path = SCRIPT_DIR / ".." / "Data"
data_path = SCRIPT_DIR

# Data import
infrastructure = data_path / "isla_coralina_infrastructure.csv"
inf_df = pd.read_csv(infrastructure)
inf_df['date_last_update'] = pd.to_datetime(inf_df['date_last_update'])

reliefops = data_path / "isla_coralina_relief_operations.csv"
rel_df = pd.read_csv(reliefops)
rel_df['date'] = pd.to_datetime(rel_df['date'])

# Variables
map_center = (inf_df.latitude.mean(),inf_df.longitude.mean())
date_range = (rel_df['date'].max() - rel_df['date'].min()).days + 1

# Streamlit and plots
st.title("📊 Isla Carolina Hurricane Maris Recovery Operations")


# Infrastructure map
op_status = ['Fully Operational', 'Partially Operational', 'Non-Operational']
colors = ['green','orange','red']
op_code = ['Operational','Partly Operational','Not Operational']
stat_color = dict(zip(op_status,colors))
code = dict(zip(op_status,op_code))

facility_icon = {'Supply Distribution Center':'truck', 
            'Bridge':'road',
            'Water Treatment Plant':'tint' ,
            'Power Substation':'bolt',
            'School (Shelter)':'home',
            'Fire Station':'fire-extinguisher',
            'Shelter':'home',
            'Health Clinic':'medkit',
            'Hospital':'h-square',
            'Communications Tower':'podcast'}

m1 = folium.Map(location=map_center, zoom_start=8, tiles="CartoDB positron")

for _, row in inf_df.iterrows():
    folium.Marker(location=[row['latitude'],row['longitude']],
                  popup=f"{row['municipality']}\n{row['facility_name'].rsplit(maxsplit=1)[-1]}\n{row['facility_type']}\nOpStatus={code[row['operational_status']]}\nSeverity={row['damage_severity']}\nPop={row['population_served']}",
                  icon=folium.Icon(color=stat_color[row["operational_status"]],prefix='fa',icon=facility_icon[row['facility_type']])
                 ).add_to(m1)

legend_html = """
<div style="
     position: fixed; 
     bottom: 50px; left: 50px; 
     width: 240px;
     z-index: 999999;
     background-color: white;
     border: 2px solid grey;
     padding: 10px;
     font-size: 14px;">
     
     <b style="color:black;">Facility Status</b><br>
     
     <span style="color:green; font-weight: bold;">●</span>
     <span style="color:black;"> Operational</span><br>

     <span style="color:orange; font-weight: bold;">●</span>
     <span style="color:black;"> Partially Operational</span><br>

     <span style="color:red; font-weight: bold;">●</span>
     <span style="color:black;"> Not Operational</span><br>
</div>
"""

m1.get_root().html.add_child(folium.Element(legend_html))


# Tab layout
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Infrastructure", "Recovery", "Performance", "Actions", "About"])

# Damage
with tab1:
    st.header("Infrastructure and Damage Assessment")
    st.subheader(f" ")
    st.markdown("""
    
    """)
    st_folium(m1, width=700, height=500)
    #st.plotly_chart(fig2, use_container_width=True)
    #st.plotly_chart(fig3, use_container_width=True)


# Recovery
with tab2:
    st.header("Recovery Status")
    st.subheader(f" ")
    st.markdown("""
    
    """)
    #st.plotly_chart(fig1, use_container_width=True)
    #st.plotly_chart(fig2, use_container_width=True)
    #st.plotly_chart(fig3, use_container_width=True)

# KPIs
with tab3:
    st.header("Key Performance Indicators")
    st.subheader(f" ")
    st.markdown("""
    
    """)
    #st.plotly_chart(fig1, use_container_width=True)
    #st.plotly_chart(fig2, use_container_width=True)
    #st.plotly_chart(fig3, use_container_width=True)


# Actions/Analyses
with tab4:
    st.header("Analysis and Recommended Actions")
    st.subheader(f" ")
    st.markdown("""
    
    """)

# About
with tab5:
    st.header("About")
    st.subheader(f" ")
    st.markdown("""
    
    """)
