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
