#######################
# Import libraries
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

#######################
# Page configuration
st.set_page_config(
    page_title="US Population Dashboard",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")


#######################
# (10) IMPORT LIBRARY
"""
import requests
import os
import pandas as pd
import regex as re 
import time
from datetime import datetime as dt
import json
import logging

from censustools import *
"""

api2=API('gdrive')
single_file_generator_01(api2)
merge_02(api2)
group_by_03(api2)
api2.df = readCSV_and_fuse_dfs_04(api2)

# Load data
df_reshaped = pd.read_csv('data/us-population-2010-2019-reshaped.csv')


#######################
# Sidebar
with st.sidebar:
    st.title('🏂 US Population Dashboard')
    

#######################
# Plots

# Heatmap

# Choropleth map


# Donut chart
    

# Convert population to text 

# Calculation year-over-year population migrations


#######################
# Dashboard Main Panel
col = st.columns((1.5, 4.5, 2), gap='medium')

    
    st.markdown('#### States Migration')


    migrations_col = st.columns((0.2, 1, 0.2))
    with migrations_col[1]:
        st.write('Inbound')
        
        st.write('Outbound')
        
        
with col[1]:
    st.markdown('#### Total Population')
        

with col[2]:
    st.markdown('#### Top States')

    with st.expander('About', expanded=True):
        st.write('''
            - Data: [U.S. Census Bureau](https://www.census.gov/data/datasets/time-series/demo/popest/2010s-state-total.html).
            - :orange[**Gains/Losses**]: states with high inbound/ outbound migration for selected year
            - :orange[**States Migration**]: percentage of states with annual inbound/ outbound migration > 50,000
            ''')
