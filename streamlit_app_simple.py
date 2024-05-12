#######################
# Import libraries
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
from censustools import *

########################

api2=API('github')
st.write('1*********************')
st.write(api2.vars['columns']['citiz'])
st.write('2*********************')

#single_file_generator_01(api2)
#merge_02(api2)
#group_by_03(api2)
#api2.df = readCSV_and_fuse_dfs_04(api2)
