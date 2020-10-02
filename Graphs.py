import Base as b
import numpy as np
import streamlit as st
import plotly.express as px
import time
import plotly.graph_objects as go

import pycountry
import pandas as pd

def plot_cases_of_a_country(country):
    labels = ['Confirmed', 'Deaths', 'Recovered']
    colors = ['black', 'red', 'green']
    line_size = [5, 5, 5]

    df_list = [b.confirmed_df, b.death_df, b.recovered_df]

    fig = go.Figure()

    for i, df in enumerate(df_list):
        if country == 'World' or country == 'world':
            x_data = np.array(list(df.iloc[:, 4:].columns))
            y_data = np.sum(np.asarray(df.iloc[:,4:]),axis = 0)

        else:
            x_data = np.array(list(df.iloc[:, 4:].columns))
            y_data = np.sum(np.asarray(df[df['country'] == country].iloc[:,4:]),axis = 0)

        fig.add_trace(go.Scatter(x=x_data, y=y_data, mode='lines+markers',
        name=labels[i],
        line=dict(color=colors[i], width=line_size[i]),
        connectgaps=True,
        text = "Total " + str(labels[i]) +": "+ str(y_data[-1])
        ))

    fig.update_layout(
        title="COVID 19 cases of " + country,
        xaxis_title='Date',
        yaxis_title='No. of Confirmed Cases',
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor='#f5f5f5',
        plot_bgcolor='rgba(0,0,0,0)'
    )

    fig.update_yaxes(type="linear")
    return fig

def plot_new_cases_of_country(Country):
    country = Country
    if(country == 'World' or country == 'world'):
        y_data = np.array(list(b.delta_world_df[country]))
    elif(country == 'US'):
        y_list = list(b.delta_pivoted_df[country])
        y_list = [x / 2 for x in y_list]
        y_data = np.array(y_list)
    else:
        y_data = np.array(list(b.delta_pivoted_df[country]))
    x_data = np.array(list(b.delta_df['date']))
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=x_data,
        y=y_data,
        name='Daily Increase',
        marker_color='black',
        hovertemplate='Date: %{x}; \n  New Cases: %{y}',
    ))
    fig.update_layout(
            title="Daily increase in cases of " + country,
            xaxis_title='Date',
            yaxis_title='No. of New Cases',
            margin=dict(l=20, r=20, t=40, b=20),
            paper_bgcolor='#F6F6F7',
            plot_bgcolor='rgba(0,0,0,0)',
    )
    fig.update_yaxes(type="linear")
    return fig

def plot_progressbar_country(country):

    df = b.death_df
    if country == 'World' or country == 'world':
        #x_data = np.array(list(df.iloc[:, 4:].columns))
        y_data = np.sum(np.asarray(df.iloc[:,4:]),axis = 0)
    else:
        #x_data = np.array(list(df.iloc[:, 4:].columns))
        y_data = np.sum(np.asarray(df[df['country'] == country].iloc[:,4:]),axis = 0)
    progress_bar = st.sidebar.progress(0)
    status_text = st.sidebar.empty()
    last_rows =[ [0]]
    chart_data = pd.DataFrame(
            last_rows)
    chart_data.rename(columns={0: "Deaths"})
    chart = st.line_chart(chart_data)
    leny = (y_data.size-1)/100

    for i in range(1, 101):
        new_rows = [y_data[int(i*leny)]]
        status_text.text("%i%% Complete" % i)
        chart.add_rows(new_rows)
        progress_bar.progress(i)
        last_rows = new_rows
        time.sleep(0.05)

    progress_bar.empty()
    st.button("Re-run")


def top5_pie():
    #st.title("Top 5 countries with confirmed cases and recovered cases")
    df = b.country_stats_df.sort_values('confirmed', ascending= False).reset_index(drop=True).head(5)
    df2 = b.country_stats_df.sort_values('recovered', ascending= False).reset_index(drop=True).head(5)
    fig = px.pie(df, values=df['confirmed'][:5], names=df['country'][:5], title='Total Confirmed Cases')
    fig2 = px.pie(df2, values=df2['recovered'][:5], names=df['country'][:5], title='Total Recovered Cases')
    return fig, fig2

def top5_bar():
    st.title("Selected Top 5 Countries")
    df = b.country_stats_df.sort_values('confirmed', ascending= False).reset_index(drop=True).head(5)

    fig = go.Figure(data=[
    go.Bar(name='Confirmed', x=df['country'][:5], y=df['confirmed'][:5]),
    go.Bar(name='Recovered', x=df['country'][:5], y=df['recovered'][:5]),
    go.Bar(name='Deaths', x=df['country'][:5], y=df['deaths'][:5])])

    return fig

def mapall():
    df_confirm =  pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
    #df_confirm = pd.read_csv('Data/time_series_covid19_confirmed_global.csv')
    df_confirm = df_confirm.drop(columns=['Province/State','Lat', 'Long'])
    df_confirm = df_confirm.groupby('Country/Region').agg('sum')
    date_list = list(df_confirm.columns)

    # Get the three-letter country codes for each country
    def get_country_code(name):
        try:
            return pycountry.countries.lookup(name).alpha_3
        except:
            return None
    df_confirm['country'] = df_confirm.index
    df_confirm['iso_alpha_3'] = df_confirm['country'].apply(get_country_code)

    # Transform the dataset in a long format
    df_long = pd.melt(df_confirm, id_vars=['country','iso_alpha_3'], value_vars=date_list)

    fig = px.choropleth(df_long,                            # Input Dataframe
                        locations="iso_alpha_3",           # identify country code column
                        color="value",                     # identify representing column
                        hover_name="country",              # identify hover name
                        animation_frame="variable",        # identify date column
                        projection="natural earth",        # select projection
                        color_continuous_scale = 'Peach',  # select prefer color scale
                        range_color=[0,50000],              # select range of dataset
                        width = 800
                                      
                        )
    return fig