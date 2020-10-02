import numpy as np
import pandas as pd
import plotly.graph_objects as go

'''
#for static fetching of data

death_df = pd.read_csv('Data/time_series_covid19_deaths_global.csv')
confirmed_df = pd.read_csv('Data/time_series_covid19_confirmed_global.csv')
recovered_df = pd.read_csv('Data/time_series_covid19_recovered_global.csv')
country_df = pd.read_csv('Data/cases_country.csv')
delta_df = pd.read_csv('Data/cases_time.csv')
'''

death_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
confirmed_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
recovered_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')
country_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/web-data/data/cases_country.csv')
delta_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/web-data/data/cases_time.csv')

country_df.reset_index()
delta_df = delta_df[['Country_Region', 'Delta_Confirmed', 'Last_Update']]

country_df.columns = map(str.lower, country_df.columns)
confirmed_df.columns = map(str.lower, confirmed_df.columns)
death_df.columns = map(str.lower, death_df.columns)
recovered_df.columns = map(str.lower, recovered_df.columns)
delta_df.columns = map(str.lower, delta_df.columns)
confirmed_df = confirmed_df.rename(columns={'province/state': 'state', 'country/region': 'country', 'lat': 'lat', 'long': 'lon'})
recovered_df = recovered_df.rename(columns={'province/state': 'state', 'country/region': 'country'})
death_df = death_df.rename(columns={'province/state': 'state', 'country/region': 'country'})
country_df = country_df.rename(columns={'country_region': 'country'})
delta_df = delta_df.rename(columns={'last_update': 'date', 'country_region': 'country_name'})

list_all_countries = list(confirmed_df['country'].unique())
confirmed_total = int(country_df['confirmed'].sum())
deaths_total = int(country_df['deaths'].sum())
recovered_total = int(country_df['recovered'].sum())
active_total = int(country_df['active'].sum())

confirmed_today = int(confirmed_df[confirmed_df.columns[-1]].sum() - confirmed_df[confirmed_df.columns[-2]].sum())
confirmed_sign = '+' if confirmed_today>=0 else '-'
death_today = int(death_df[death_df.columns[-1]].sum() - death_df[death_df.columns[-2]].sum())
death_sign = '+' if death_today>=0 else '-'
recovered_today = int(recovered_df[recovered_df.columns[-1]].sum() - recovered_df[recovered_df.columns[-2]].sum())
recovered_sign = '+' if recovered_today>=0 else '-'

country_stats_df = country_df[['country','confirmed', 'deaths', 'recovered']]
fig = go.FigureWidget( layout=go.Layout() )

delta_pivoted_df = delta_df.pivot_table(index='date', columns='country_name', values='delta_confirmed', aggfunc=np.sum)
delta_pivoted_df.reset_index(level=0, inplace=True)
delta_world_df = pd.DataFrame()
delta_world_df['World'] = delta_pivoted_df[delta_pivoted_df.columns].sum(axis=1)
delta_world_df['date'] = delta_pivoted_df['date']
