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

#######################  # Sidebar
with st.sidebar:
    st.title('US Population Census CPS')

    ## YEAR 
    year_list = api2.allYearList() # TODO [list(api2.allYearList()).insert(0,0)],  insert 0 for None value 
    selected_year = st.slider("Select a year", min_value=min(year_list), max_value=max(year_list), value=max(year_list)-1)
    choose_year     = pd.to_datetime(df['YYYYMM']).dt.year==selected_year 

    ## STATE 
    choose_state     = None
    option = st.radio('States display:', ('No State','State' ), index=0) 
    if option == 'State':
        list_full_name_state = [api2.abbrev_to_fullName(api2.id_to_stateName(stateID)) for stateID in api2.allStatesIdList()]
        selected_stateAbbrev = st.selectbox('Select state', list_full_name_state)         
        choose_state    = df['state']==api2.abbrev_to_id(api2.fullName_to_abbrev(selected_stateAbbrev) )

    ## MARITAL
    choose_marital     = None
    option = st.radio('Marital display:', ('No','yes'), index=0) 
    if option == 'yes':
        selected_marital = st.selectbox('Married ? ', ['No','Yes'])         
        choose_marital    = df['marital']==(1 if selected_marital=='Yes' else 2) 

    ## CITIZ 
    choose_citiz     = None
    option = st.radio('Citizen display:', ('No','yes'), index=0) 
    if option == 'yes':
        selected_citiz = st.selectbox('Citizen ?', ['No','Yes'])         
        choose_citiz   = df['citiz']==(1 if selected_citiz=='Yes' else 2) 

    ## HS and COLLEGE 
    choose_collegcred     = None
    choose_highsch        = None
    option = st.radio('High School & College Credit display:', ('No','yes'), index=0) 
    if option == 'yes':
        selected_collegcred = st.selectbox('Got College Credit?', ['No','Yes'])         
        choose_collegcred   = df['collegcred']==(1 if selected_collegcred=='Yes' else 2) 
        selected_highsch    = st.selectbox('Finished HighSchool?', ['No','Yes'])  
        choose_highsch      = df['highsch']==(1 if selected_highsch=='Yes' else 2) 
        #st.write('Inside: High School & College Credit display')

    condition      = None
    display_select = ''

    display_select += f'year: {selected_year}'
    if choose_year is not None:
      if condition is None: condition = choose_year
      else: 
          condition &= choose_year
    
    if choose_state  is not None:
      if condition is None: condition = choose_state
      else: 
          condition &= choose_state
          display_select += f', for the state: {selected_stateAbbrev}'
    
    if choose_marital  is not None:
      if condition is None: condition = choose_marital
      else: 
          condition &= choose_marital
          display_select += f', marital situation: {selected_marital}'
    
    if choose_citiz is not None:
      if condition is None: condition = choose_citiz
      else: 
          condition &= choose_citiz
          display_select += f', citizen status: {selected_citiz}'
    
    if choose_collegcred is not None:
      if condition is None: condition = choose_collegcred
      else: 
          condition &= choose_collegcred 
          #display_select += f", Got 4yrs of college credit: {selected_collegcred}"
          
    if choose_highsch is not None:
      if condition is None: condition = choose_highsch
      else: 
          condition &= choose_highsch
          #display_select += f', Finish HS: {selected_highsch}' 

    #st.write(f'condition: [{condition}]')
    g2 = api2.df [condition]
    
    
    # [STATE LEVEL] -------  Display the 7 highest population
    state_data = g2.groupby(['state'])['weight'].sum().reset_index().sort_values(by='weight', ascending=False).head(7)
    state_data['state'] = state_data['state'].apply(lambda x: api2.id_to_stateName(x))


#######################  # Main Layout
#Display
st.write(f'Display according to the following conditions: \n{display_select}.')

#Display the df(7states only)
st.write (state_data.reset_index(drop=True) )

# [CITY LEVEL]
def city_state(long_city:str)-> str:
  try:
    parts = long_city.split(',')
    city_name = parts[0].split('-')[0].strip()
    state_abbr = parts[1].split('-')[0].strip()
  except Exception as e:
    #print (f"City is not having the same format (cities, ST): {long_city}"), like Bloomington-Normal IL with no SPACE (important)
    pattern = r'([\s\S]*)([A-Z]{2})'
    res = re.search(pattern, long_city)
    city_name = res.group(1).strip()
    state_abbr = res.group(2).strip()
  return f"{city_name} {state_abbr}"

def cityID_to_fullNames(CBSA_Id):
  try:
    res = api2.allVars_dict[2010]['GTCBSA']['values']['item'][str(CBSA_Id)]
  except Exception as e:
    res = "Unkown NE" 
  return res

city_data = g2.groupby(['city'])['weight'].sum().reset_index().sort_values(by='weight', ascending=False) 
city_data['cityFullName'] = city_data['city'].apply(cityID_to_fullNames)
city_data['cityName'] = city_data['cityFullName'].apply(city_state)

def show_usa_map(city_data, us_cities_geojson_file):
    city_data = city_data.reset_index(drop=True)

    # Load GeoJSON file for US cities
    with open('us_cities.geojson', 'r') as f:
        geojson_data = json.load(f)

    coordinates_list =[]
    df_all_cities = pd.unique(city_data['cityName'])
    for feature in geojson_data['features']:
        city_name = feature['properties']['name']
        if city_name in df_all_cities:
          ind   = city_data.index[city_data['cityName'] == city_name].tolist()[0]
          coord = feature['geometry']['coordinates']
          coordinates_list.append ([ind, coord])

    coordinates_dict = {ind: coord for ind, coord in coordinates_list}
    city_data = city_data[city_data.index.isin(coordinates_dict.keys())] #delete all cities with error in their name
    city_data['coordinate'] = city_data.index.map(lambda x: coordinates_dict[x])

    #Display the US map
    fig = px.scatter_geo(city_data,
                        lon=[coord[0] for coord in city_data['coordinate']],
                        lat=[coord[1] for coord in city_data['coordinate']],
                        hover_name='cityFullName',
                        size='weight',
                        color='weight',
                        scope='usa',
                        color_continuous_scale='Viridis')
    #fig.update_layout(title='Population per condition')
    #Black Background 
    fig.update_layout(
        geo=dict(
            bgcolor='rgb(17,17,17)'
        )
    )

    st.plotly_chart(fig)

show_usa_map(city_data, 'us_cities.geojson')

#######################  # Logistic regression
import statsmodels.api as sm
X = g2[['state', 'nativity', 'marital', 'sex']]
y = g2['citiz'].replace(2, 0)
#X = sm.add_constant(X)
model = sm.Logit(y, X)
result = model.fit()

st.write('''
    This table presents the results of a logistic regression analysis that predicts citizenship status based on demographic
    and socio-economic factors depending on where the individual live (state), where he/she was born (nativity), 
    marital status and gender.
    As a result, this is the variables that are significants in association with citizenship, 
    suggesting who are more likely to be citizens or not.
''')

good_pval = 0.05
good_coef = 0.5
for independant_var, coef, pvalue in zip(result.params.index, result.params.values, result.pvalues.values):
    if coef > good_coef or coef < -good_coef:
        if pvalue < good_pval:
            significance_label = ""
        st.write(f"   - The variable :green[**{independant_var}**] is significant for to become a citizen: Coefficient={coef:.4f} (p-value={pvalue:.4f})")

with st.expander('Logistic Regression Result Table', expanded=False):
    st.write(result.summary())

#######################  # About us
with st.expander('About', expanded=True):
        st.write('''
            - Data: [US Census Bureau API from the Current Population Survey (CPS)](https://www.census.gov/data/developers/data-sets/census-microdata-api/cps/basic.html).
            - Semester project for :orange[**Econ 8320**] Tools for Data Analysis!
            - Streamlit dashboard highlighting demographic changes in the US from 2010 to 2023
            - Information at the year-month-city level, describing the proportion in the overall population of at least 7 demographic variables 
            - Website from your GitHub 
            - Author: Souleymane Diawara - May 2024. 
            ''')
