#######################
# Import libraries
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
from censustools import *

#######################  # Page configuration
st.set_page_config(
    page_title="US Population Census - Semester project",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

#######################  # Load data
api2=API('github')
api2.df = readCSV_and_fuse_dfs_04(api2)
df = api2.df
#st.write(df.head())


#######################  # FUNCTIONS to be moved in the Api class


#######################  # Sidebar
with st.sidebar:
    st.title('🏂 US Population Census 4')
    
    year_list = api2.allYearList() # TODO [list(api2.allYearList()).insert(0,0)],  insert 0 for None value
    #selected_year = st.selectbox('Select a year', year_list)
    #choose_year     = pd.to_datetime(df['YYYYMM']).dt.year == selected_year 
    choose_year = st.slider("Select a year", min_value=min(year_list), max_value=max(year_list), value=max(year_list)-1)
    
    #list_full_name_state = [api2.abbrev_to_fullName(api2.id_to_stateName(stateID)) for stateID in api2.allStatesIdList()]
    list_full_name_state = [stateID in api2.allStatesIdList()]
    state = st.selectbox('Select state', list_full_name_state)
    #choose_state    = df['state']== api2.fullName_to_abbrev(state)

    choose_marital  = None
    choose_marital  = df['marital']== 1
    choose_citiz    = None
    choose_citiz    = df['citiz']== 1
    choose_collegcred = None
    choose_collegcred = df['collegcred']== 1
    choose_highsch  = None
    choose_highsch  = df['highsch']== 2
    
    condition = None
    
    if choose_year == 0:
      if condition is None: condition = choose_year
      else: condition &= choose_year
    
    if choose_state  != '':
      if condition is None: condition = choose_state
      else: condition &= choose_state
    
    if choose_marital != '':
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

    st.write(f'condition : {condition}')
