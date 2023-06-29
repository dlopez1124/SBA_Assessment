#!/usr/bin/env python
# coding: utf-8

# In[1]:




import pandas as pd
import streamlit as st
import warnings
warnings.filterwarnings('ignore')





wosb_by_state = pd.read_csv('Data/wosb_by_state.csv')

wosb_gdf = wosb_by_state

#wosb_gdf = state_gdf.merge(wosb_by_state, how='left', on='Entity State')
#wosb_gdf = wosb_gdf.dropna()

#wosb_gdf = wosb_gdf.sort_values(by='Entity State').reset_index(drop=True)

wosb_gdf['Total WOSB Action Obligation'] = wosb_gdf['Total WOSB Action Obligation'].apply(lambda x: '${:,.2f}'.format(x))
wosb_gdf['EDWOSB Action Obligation'] = wosb_gdf['EDWOSB Action Obligation'].apply(lambda x: '${:,.2f}'.format(x))
wosb_gdf['Ineligible NAICS Action Obligation'] = wosb_gdf['Ineligible NAICS Action Obligation'].apply(lambda x: '${:,.2f}'.format(x))
wosb_gdf['Eligible NAICS Action Obligation'] = wosb_gdf['Eligible NAICS Action Obligation'].apply(lambda x: '${:,.2f}'.format(x))



#s = gpd.GeoSeries(wosb_gdf['geometry'])

#x_map = s.centroid.x.mean()
#y_map = s.centroid.y.mean()

pd.options.display.float_format = '{:.2f}'.format

st.title('SBA WOSB Analysis')
st.subheader('By: David Lopez Jr.')
st.caption('Source: GSA Federal Procurement Data System, Contracts with WOSB Set-Asides, 04/01/2011 to 06/27/2023')

st.markdown('---')


st.markdown('##### Please use the following hyperlink to view the [WOSB Analysis Choropleth Map](https://dlopez1124.github.io/SBA_Assessment/). Thank you.', unsafe_allow_html=True)

st.markdown('')


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

st.markdown('---')

st.markdown('Link to [GitHub Repository](https://github.com/dlopez1124/SBA_Assessment)')

