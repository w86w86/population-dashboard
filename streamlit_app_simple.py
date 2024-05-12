#######################
# Import libraries
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
from censustools import *

#######################  # Page configuration
st.set_page_config(
    page_title="US Population Census - Semester project 2",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

#######################  # Load data
api2=API('github')
api2.df = readCSV_and_fuse_dfs_04(api2)
df = api2.df
#st.write(df.head())

#######################  # Sidebar
with st.sidebar:
    st.title('🏂 US Population Census - Semester project 2')
    
    year_list = api2.allYearList()
    
    selected_year = st.selectbox('Select a year', [0] + year_list)
    choose_year     = pd.to_datetime(df['YYYYMM']).dt.year == selected_year
    choose_state    = None
    choose_state    = df['state']==20
    choose_marital  = None
    choose_marital  = df['marital']== 1
    choose_citiz    = None
    choose_citiz    = df['citiz']== 1
    choose_collegcred = None
    choose_collegcred = df['collegcred']== 1
    choose_highsch  = None
    choose_highsch  = df['highsch']== 2
    
    condition = None
    
    if choose_year is not None:
      if condition is None: condition = choose_year
      else: condition &= choose_year
    
    if choose_state is not None:
      if condition is None: condition = choose_state
      else: condition &= choose_state
    
    if choose_marital is not None:
      if condition is None: condition = choose_marital
      else: condition &= choose_marital
    
    if choose_citiz is not None:
      if condition is None: condition = choose_citiz
      else: condition &= choose_citiz
    
    if choose_collegcred is not None:
      if condition is None: condition = choose_collegcred
      else: condition &= choose_collegcred
    
    if choose_highsch is not None:
      if condition is None: condition = choose_highsch
      else: condition &= choose_highsch
