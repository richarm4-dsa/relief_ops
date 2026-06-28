# DSA506 Visual Analytics and Communications  
# Michelle Richardson  
# Test 1  

# Dashboard

import numpy as np
import pandas as pd
from pathlib import Path
import plotly.express as px
import folium
from folium.plugins import HeatMap
from IPython.display import display, IFrame
import streamlit as st
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent

# Build the absolute path to your Data folder
#data_path = SCRIPT_DIR / ".." / "Data"
data_path = SCRIPT_DIR

# Data import
infrastructure = data_path / "isla_coralina_infrastructure.csv"
inf_df = pd.read_csv(infrastructure)
inf_df['date'] = pd.to_datetime(inf_df['date'])

reliefops = data_path / "isla_coralina_relief_operations.csv"
rel_df = pd.read_csv(reliefops)
rel_df['date'] = pd.to_datetime(rel_df['date'])

# Variables
map_center = (inf_df.latitude.mean(),inf_df.longitude.mean())
date_range = (rel_df['date'].max() - rel_df['date'].min()).days + 1

# Streamlit and plots
st.title("📊 Isla Carolina Hurricane Maris Recovery Operations")


# Tab layout
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Infrastructure", "Recovery", "Performance", "Actions", "About"])

# Damage
with tab1:
    st.header("Infrastructure and Damage Assessment")
    st.subheader(f" ")
    st.markdown("""
    
    """)
    #st.plotly_chart(fig1, use_container_width=True)
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
