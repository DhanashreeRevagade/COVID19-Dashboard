import streamlit as st
import Base as b
import Graphs as g
import Details as d
import pandas as pd
import numpy as np

st.title("COVID19 Dashboard")
st.sidebar.title("IoT Project")
st.sidebar.header("Group Number 20")
st.sidebar.markdown(
    """<head>
  <title>COVID-19 Dashboard | IOT Group 20</title>
  <style>
  body{
      background-color: #fff;
      font-size: 40px;
  }
  </style>
</head>
<body>
    <ol>
        <li>Hardik Mehta (MIS - 111715025)</li>
        <li>Aditi Bambodi (MIS - 111716003)</li>
        <li>Dhanashree Revagade (MIS - 111715021)</li>
    </ol>
</body>
""", unsafe_allow_html=True
)

st.sidebar.text("Live Updated Data")
st.sidebar.text("Source: John Hopkins University")

st.sidebar.text(" ")
st.sidebar.write("Libraries/Packages used:")
st.sidebar.write("1) Streamlit and 2)Plotly")

allmap = g.mapall()
st.write(allmap)

country_name = st.selectbox('', b.list_all_countries, 79)
to_show_overall = g.plot_cases_of_a_country(country_name)
to_show_daily = g.plot_new_cases_of_country(country_name)
d.show_country_stats(country_name)

sorted_country_df = b.country_df.sort_values('confirmed', ascending= False)




st.write(to_show_daily)
st.write(to_show_overall)

st.header("Death Count Progress Bar")
st.write(g.plot_progressbar_country(country_name))
#g.plot_progressbar_country(country_name)

select_graph = st.selectbox('Visualization type', ['Bar plot', 'Pie chart'])
if select_graph == 'Pie chart':
    
    pie5fig, pie5fig2 = g.top5_pie()
    st.write(pie5fig)
    st.plotly_chart(pie5fig2)

if select_graph=='Bar plot':
    bar5fig = g.top5_bar()
    st.write(bar5fig)
    #st.plotly_chart(bar5fig)

st.title('COVID-19 : Total, Deaths and Recovered')
to_show = d.show_latest_cases(100)
st.table(to_show)
