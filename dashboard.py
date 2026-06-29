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

#filtered_df = inf_df[
#    inf_df["facility_type"].isin(selected_types)
#]

m1 = folium.Map(location=map_center, zoom_start=8, tiles="CartoDB positron")

for _, row in filtered_df.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"{row['municipality']}\n"
              f"{row['facility_name'].rsplit(maxsplit=1)[-1]}\n"
              f"{row['facility_type']}\n"
              f"OpStatus={code[row['operational_status']]}\n"
              f"Severity={row['damage_severity']}\n"
              f"Pop={row['population_served']}",
        icon=folium.Icon(
            color=stat_color[row["operational_status"]],
            prefix='fa',
            icon=facility_icon[row['facility_type']]
        )
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

# Hospital and water treatment infrastructure map
# Show radius around hospitals and water treatment plants
m2 = folium.Map(location=map_center, zoom_start=8, tiles="CartoDB positron")  #tiles="OpenStreetMap")

rad_hosp_miles = 15
rad_wt_miles = 30
critical = ['Hospital','Water Treatment Plant']
radius_m = [rad_hosp_miles*1609.34,rad_wt_miles*1609.34]  # Miles
col = ['blue','grey']
radius = dict(zip(critical,radius_m))
color = dict(zip(critical,col))

infr = inf_df[inf_df['facility_type'].isin(critical)]

for _, row in infr.iterrows():   # radius circles
    folium.Circle(
        location=([row['latitude'],row['longitude']]),
        radius=radius[row['facility_type']],
        color=None,
        fill=True,
        fill_color=color[row["facility_type"]],
        fill_opacity=0.2,
    ).add_to(m2)

for _, row in infr.iterrows():   # Dots
    folium.Circle(location=[row['latitude'],row['longitude']],
                        radius=3, fill=True, fill_opacity=1,
                        popup=f"{row['municipality']}\n{row['facility_name'].rsplit(maxsplit=1)[-1]}\n{row['facility_type']}\n{code[row['operational_status']]}\nSeverity={row['damage_severity']}\nPop={row['population_served']}\nRoad Access: {row['road_access']}",
                        color=stat_color[row["operational_status"]],
                       ).add_to(m2)

legend_html = """
<div style="
     position: fixed;
     bottom: 50px;
     left: 50px;
     width: 260px;
     z-index: 999999;
     background-color: white;
     border: 2px solid grey;
     padding: 10px;
     font-size: 14px;
     color: black;
     font-family: Arial;
     opacity: 0.95;">

    <b style="color:black;">Vital Infrastructure</b><br>

    <span style="color:grey; font-weight:bold;">●</span>
    <span style="color:black;"> Hospital Radius</span><br>

    <span style="color:blue; font-weight:bold;">●</span>
    <span style="color:black;"> Water Treatment Radius</span><br>

    <span style="color:green; font-weight:bold;">●</span>
    <span style="color:orange; font-weight:bold;">●</span>
    <span style="color:red; font-weight:bold;">●</span>
    <span style="color:black;"> Facility Status</span>

</div>
"""
m2.get_root().html.add_child(folium.Element(legend_html))


### TAB 2 - Recovery Status
# Delivery delay by tx mode
fig2_1 = px.box(
    rel_df,
    x='municipality',
    y='delivery_delay_hours',
    color='transport_mode', 
    title='Delivery Delay for Transport Modes by Municipality',
    labels={
        'delivery_delay_hours': 'Delay (hours)',
        'transport_mode': 'Mode',
        'municipality': 'Municipality'
    },
)
fig2_1.show()

# Delivery Delay by Supply Type
supply_mun = rel_df.groupby(['municipality','supply_type'])['delivery_delay_hours'].mean().reset_index()
fig2_2 = px.bar(supply_mun,
             y='supply_type',
             x='delivery_delay_hours',
             color='municipality',
             barmode='stack',
             title='Delivery Delay by Supply Type',
             labels={
                 'supply_type':'Supply Type',
                 'delivery_delay_hours':'Delay (hours)',
                 'municipality':'Municipality'
             })
fig2_2.show()


### TAB 3 - Key Performance Indicators
# Requested vs Delivered
delivery = rel_df.groupby('municipality')[['quantity_requested','quantity_delivered']].sum().reset_index()
fig3_1 = px.bar(
    delivery,
    x='municipality',
    y=['quantity_requested', 'quantity_delivered'],
    barmode='stack',
    title='Supply Delivery by Municipality: Fulfilled Against Requested',
    #text='pct_delivered',
    labels={
        'municipality':'Municipality',
        'value':'Quantity',
        'quantity_requested':'Requested',
        'quantity_delivered':'Delivered'
    },
)
fig3_1.update_layout(legend_title_text='Delivery')
fig3_1.show()

# Delay timeline
bydate_mun = rel_df.groupby(['date','municipality'], as_index=False)['delivery_delay_hours'].mean()
fig3_2 = px.line(
    bydate_mun,
    x='date',
    y='delivery_delay_hours',
    color='municipality',
    title=f'Mean Delivery Delay by Municipality',
    labels={
        'delivery_delay_hours': 'Delay (hours)',
        'date': 'Date',
        'municipality': 'Municipality'
    },
    )
fig3_2.show()


# Tab layout
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Infrastructure", "Recovery", "Performance", "Actions", "About"])

# Damage
with tab1:
    st.header("Infrastructure and Damage Assessment")

    # Compact filter bar (not sidebar, not columns)
    selected_types = st.multiselect(
        "Facility Types",
        sorted(inf_df["facility_type"].unique()),
        default=sorted(inf_df["facility_type"].unique()),
        label_visibility="collapsed"
    )

    filtered_df = inf_df[
        inf_df["facility_type"].isin(selected_types)
    ]

    st_folium(m1, width=700, height=500)
    st.markdown("""
    A minimum radius should be maintained between hospitals and between water treatment plants. 
    The following map shows a 15 mile radius around hospitals and a 30 mile radius around water treatment plants. 
    """)
    st_folium(m2, width=700, height=500)            

# Recovery
with tab2:
    st.header("Recovery Status")
    st.subheader(f" ")
    st.markdown("""
    """)
    st.plotly_chart(fig2_1, use_container_width=True)
    st.plotly_chart(fig2_2, use_container_width=True)

# KPIs
with tab3:
    st.header("Key Performance Indicators")
    st.subheader(f"DAY {date_range}")
    st.markdown("""
    """)
    st.plotly_chart(fig3_1, use_container_width=True)
    st.plotly_chart(fig3_2, use_container_width=True)

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
