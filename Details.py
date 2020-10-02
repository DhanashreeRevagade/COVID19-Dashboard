import streamlit as st
import Base as b

def show_country_stats(country):

    country_confirmed_df = b.confirmed_df[b.confirmed_df['country'] == country]
    country_death_df = b.death_df[b.death_df['country'] == country]
    country_recovered_df = b.recovered_df[b.recovered_df['country'] == country]

    country_confirmed = country_confirmed_df[country_confirmed_df.columns[-1]].sum()
    country_death = country_death_df[country_death_df.columns[-1]].sum()
    country_recovered = country_recovered_df[country_recovered_df.columns[-1]].sum()

    country_confirmed_today = int(country_confirmed_df[country_confirmed_df.columns[-1]].sum()) - int(country_confirmed_df[country_confirmed_df.columns[-2]].sum())
    country_death_today = int(country_death_df[country_death_df.columns[-1]].sum()) - int(country_death_df[country_death_df.columns[-2]].sum())
    country_recovered_today = int(country_recovered_df[country_recovered_df.columns[-1]].sum()) - int(country_recovered_df[country_recovered_df.columns[-2]].sum())

    country_confirmed_today_sign = '+' if country_confirmed_today>=0 else ''
    country_death_today_sign = '+' if country_death_today>=0 else ''
    country_recovered_today_sign = '+' if country_recovered_today else ''

    st.markdown(
        '''
        <h1></h1>
    <div class="jumbotron text-center" style='background-color: #fff'>
    <div class="row">
        <div class="col-sm-4">
        <p>Total Confirmed</p>
        <p>[''' + str(country_confirmed_today_sign) + str(country_confirmed_today) + ''']</p>
        <h2>''' + str(country_confirmed) + '''</h2>
        </div>
        <div class="col-sm-4" style='background-color: #fff; border-radius: 5px'>
        <p>Total Deaths</p>
        <p>[''' + str(country_death_today_sign) + str(country_death_today) + ''']</p>
        <h2>''' + str(country_death) + '''</h2>
        </div>
        <div class="col-sm-4">
        <p>Total Recovered</p>
        <p>[''' + str(country_recovered_today_sign) + str(country_recovered_today) + ''']</p>
        <h2>''' + str(country_recovered) + '''</h2>
        </div>
        ''',
        unsafe_allow_html=True
    )

def show_latest_cases(n):
    n = int(n)
    if n>0:
        return b.country_stats_df.sort_values('confirmed', ascending= False).reset_index(drop=True).head(n).style.set_properties(**{'text-align': 'right', 'font-size': '15px'})
