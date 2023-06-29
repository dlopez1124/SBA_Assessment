#!/usr/bin/env python
# coding: utf-8

# In[1]:




import pandas as pd
import geopandas as gpd
import folium
import streamlit as st
import altair as alt
import branca.colormap as cm
import streamlit_folium
import warnings
warnings.filterwarnings('ignore')




state_gdf = gpd.read_file('cb_2022_us_state_500k/cb_2022_us_state_500k.shp')

state_gdf = state_gdf.rename(columns={'NAME': 'Entity State'})

state_gdf = state_gdf[['Entity State', 'geometry']]

wosb_by_state = pd.read_csv('Data/wosb_by_state.csv')

wosb_gdf = state_gdf.merge(wosb_by_state, how='left', on='Entity State')
wosb_gdf = wosb_gdf.dropna()

wosb_gdf = wosb_gdf.sort_values(by='Entity State').reset_index(drop=True)

wosb_gdf['Total WOSB Action Obligation'] = wosb_gdf['Total WOSB Action Obligation'].apply(lambda x: '${:,.2f}'.format(x))
wosb_gdf['EDWOSB Action Obligation'] = wosb_gdf['EDWOSB Action Obligation'].apply(lambda x: '${:,.2f}'.format(x))
wosb_gdf['Ineligible NAICS Action Obligation'] = wosb_gdf['Ineligible NAICS Action Obligation'].apply(lambda x: '${:,.2f}'.format(x))
wosb_gdf['Eligible NAICS Action Obligation'] = wosb_gdf['Eligible NAICS Action Obligation'].apply(lambda x: '${:,.2f}'.format(x))



s = gpd.GeoSeries(wosb_gdf['geometry'])

x_map = s.centroid.x.mean()
y_map = s.centroid.y.mean()

pd.options.display.float_format = '{:.2f}'.format

st.title('SBA WOSB Analysis')
st.subheader('By: David Lopez Jr.')
st.caption('Source: GSA Federal Procurement Data System, Contracts with WOSB Set-Asides, 04/01/2011 to 06/27/2023')



@st.cache(allow_output_mutation=True)
def choropleth_map(wosb_gdf):
    mymap = folium.Map(location=[y_map, x_map], zoom_start=4,tiles=None)
    folium.TileLayer('CartoDB positron',name="Light Map",control=False).add_to(mymap)
    folium.Choropleth(geo_data=wosb_gdf,
                      data=wosb_gdf,
                      columns=['Entity State',"Prop Ineligible"],
                      key_on="feature.properties.Entity State",
                      fill_color='YlGnBu',
                      fill_opacity=1,
                      line_opacity=1,
                      legend_name="Proportion of WOSB Funds Obligated to Ineligible NAICS Codes",
                      smooth_factor=0,
                      #Highlight= True,
                      name = "Proportion Ineligible NAICS",
                      #show=False,
                      #overlay=True,
                      nan_fill_color = "White").add_to(mymap)
    
    style_function = lambda x: {'fillColor': '#ffffff', 
                            'color':'#000000', 
                            'fillOpacity': .1, 
                            'weight': 1}
    
    highlight_function = lambda x: {'fillColor': '#0000000', 
                               'color':'#000000', 
                                'fillOpacity': 0.1, 
                                'weight': 1}
    
    hover = folium.features.GeoJson(
        wosb_gdf,
        style_function=style_function,
        control=False,
        highlight_function=highlight_function,
        tooltip=folium.features.GeoJsonTooltip(
            fields=['Entity State',
                'Eligible NAICS Action Obligation',
                'EDWOSB Action Obligation',
               'Ineligible NAICS Action Obligation'],
        aliases=['State: ',
		 'Obligated to WOSB Eligible NAICS Code: ',
                 'Obligated to EDWOSB Eligible NAICS Code: ',
                 'Obligated to WOSB Ineligible NAICS Code: '],
       style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
    )
)
    mymap.add_child(hover)
    mymap.keep_in_front(hover)
    folium.LayerControl().add_to(mymap)
    
    return mymap

streamlit_folium.folium_static(choropleth_map(wosb_gdf))



df_sorted = wosb_by_state.sort_values('Prop Ineligible', ascending=False)
df_sorted['Prop Ineligible'] = pd.to_numeric(df_sorted['Prop Ineligible'])
df_sorted['Proportion of WOSB Funds Obligated to Ineligible NAICS Codes'] = df_sorted['Prop Ineligible']



# Get the top 15 states
top_15_states = df_sorted[['Entity State', 'Prop Ineligible']].head(15).reset_index(drop=True)

chart = alt.Chart(top_15_states).mark_bar().encode(
    y=alt.Y('Entity State', sort='-x'),  # Sort states in descending order
    x='Prop Ineligible',
    tooltip=['Entity State', 'Prop Ineligible']
).properties(
    width=600,
    height=400,
    title='Top 15 States or Territories by Proportion of WOSB Funds Obligated to Ineligible NAICS Codes'
).configure_axisX(
    labelAngle=0  # Set x-axis labels orientation to horizontal
)

# Render the chart using Streamlit
st.altair_chart(chart, use_container_width=True)


def display_state_info(state):
    if state == 'Alabama':
        st.header('Information about Alabama')
        # Display specific information or perform actions for Alabama
    elif state == 'Alaska':
        st.write('Information about Alaska')
        # Display specific information or perform actions for Alaska
    elif state == 'Arizona':
        st.write('Information about Arizona')
        # Display specific information or perform actions for Arizona
    elif state == 'Arkansas':
        st.write('Information about Arkansas')
        # Display specific information or perform actions for Arkansas
    elif state == 'California':
        st.write('Information about California')
        # Display specific information or perform actions for California
    # Add elif statements for the remaining states, Washington D.C., Puerto Rico, and Guam
    elif state == 'Washington D.C.':
        st.write('Information about Washington D.C.')
        # Display specific information or perform actions for Washington D.C.
    elif state == 'Puerto Rico':
        st.write('Information about Puerto Rico')
        # Display specific information or perform actions for Puerto Rico
    elif state == 'Guam':
        st.write('Information about Guam')
        # Display specific information or perform actions for Guam

# List of states, including Washington D.C., Puerto Rico, and Guam

def display_state_info(state):
    if state != 'Click Here to Select a State or Territory':
        state_info = wosb_gdf[wosb_gdf['Entity State'] == state]
        st.subheader(f"WOSB Information for {state}")
        st.write(f"Total WOSB Funds Obligated: {state_info['Total WOSB Action Obligation'].values[0]}")
        st.write(f"EDWOSB Funds Obligated to Eligible NAICS Codes: {state_info['EDWOSB Action Obligation'].values[0]}")
        st.write(f"WOSB Funds Obligated to Eligible NAICS Codes: {state_info['Eligible NAICS Action Obligation'].values[0]}")
        st.write(f"WOSB Funds Obligated to Ineligible NAICS Codes: {state_info['Ineligible NAICS Action Obligation'].values[0]}")

# List of states, including Washington D.C., Puerto Rico, and Guam
states = ['Click Here to Select a State or Territory','Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'District of Columbia',
          'Florida', 'Georgia', 'Guam','Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky',
          'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi',
          'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico',
          'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Puerto Rico',
          'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont',
          'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']

# Add a selectbox to the sidebar
selected_state = st.selectbox('Select State', states)

# Call the display_state_info function with the selected state
display_state_info(selected_state)

