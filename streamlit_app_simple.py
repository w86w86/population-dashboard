#######################
# Import libraries
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
from censustools import *

#######################
# Page configuration
st.set_page_config(
    page_title="US Population Census - Semester project 2",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")


#######################
# Load data


api2=API('github')
st.write('1*********************')
st.write(api2.vars['columns']['citiz'])
st.write('2*********************')

api2.df = readCSV_and_fuse_dfs_04(api2)
