import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import plotly
import plotly.express as px
import plotly.graph_objects as go

# Loading Datasets
conf_global = pd.read_csv('time_series_covid19_confirmed_global.csv')
dead_global = pd.read_csv('time_series_covid19_deaths_global.csv')
reco_global = pd.read_csv('time_series_covid19_recovered_global.csv')

country_list = conf_global['Country/Region']
country_list = pd.DataFrame(data=country_list, columns=['Country/Region'])
country_list = country_list.sort_values('Country/Region')
country_list = country_list['Country/Region'].unique()
count_country = len(country_list)

date_list = conf_global.columns[4:]
days = len(date_list)

# Global Statistics

# Total confired cases in the world
conf_total = conf_global.copy().drop(['Province/State','Country/Region','Lat','Long'],axis=1)
conf_total = pd.DataFrame(conf_total.sum()).transpose()
conf_total = conf_total.melt(var_name='Date',value_name='Confirmed')

# Total recovered cases in the world
reco_total = reco_global.copy().drop(['Province/State','Country/Region','Lat','Long'],axis=1)
reco_total = pd.DataFrame(reco_total.sum()).transpose()
reco_total = reco_total.melt(var_name='Date',value_name='Recovered')

# Total deaths in the world
dead_total = dead_global.copy().drop(['Province/State','Country/Region','Lat','Long'],axis=1)
dead_total = pd.DataFrame(dead_total.sum()).transpose()
dead_total = dead_total.melt(var_name='Date',value_name='Deaths')

# Overall status of COVID-19
global_table = pd.merge(conf_total,reco_total, on='Date') #pd.concat([conf_total,reco_total['Recovered']], axis=1)
global_table = global_table.merge(dead_total) #pd.merge(global_table,dead_total, on='Date')

# Total active cases in the world
# active = confirmed - recovered - deaths
global_table['Active'] = global_table['Confirmed'] - global_table['Recovered'] - global_table['Deaths']

# Recovery Rate = recovered*100/confirmed
global_table['Recovery%'] = global_table['Recovered']*100/global_table['Confirmed']

# Mortality Rate = deaths*100/confirmed
global_table['Mortality%'] = global_table['Deaths']*100/global_table['Confirmed']

global_table

conf_graph = go.Scatter(x=global_table['Date'],
                       y=global_table['Confirmed'],
                       mode = 'lines',
                       name = 'Confirmed')
reco_graph = go.Scatter(x=global_table['Date'],
                       y=global_table['Recovered'],
                       mode = 'lines',
                       name = 'Recovered')
dead_graph = go.Scatter(x=global_table['Date'],
                       y=global_table['Deaths'],
                       mode = 'lines',
                       name = 'Deaths')
actv_graph = go.Scatter(x=global_table['Date'],
                       y=global_table['Active'],
                       mode = 'lines',
                       name = 'Active')
rec_rate = go.Bar(x=global_table['Date'],
                       y=global_table['Recovery%'],
                       # mode = 'lines',
                       name = 'Recovery Rate')
mor_rate = go.Bar(x=global_table['Date'],
                       y=global_table['Mortality%'],
                       # mode = 'lines',
                       name = 'Mortality Rate')
graphs = [conf_graph,reco_graph,dead_graph,actv_graph]
rates = [rec_rate,mor_rate]
layout = go.Layout(title='Global COVID-19 Status')
fig_1 = go.Figure(data=graphs, layout=layout)
fig_1.show()
rate_layout = go.Layout(title='Global Daily COVID-19 Status: Changes in Rates')
fig_rate_1 = go.Figure(data=rates, layout=rate_layout)
fig_rate_1.show()

dates = global_table['Date']
daily_inc_table = global_table.drop('Date',axis=1).diff()
daily_inc_table = pd.concat([dates,daily_inc_table], axis=1)
daily_inc_table

conf_inc = go.Bar(x=daily_inc_table['Date'],
                       y=daily_inc_table['Confirmed'],
                       # mode = 'lines',
                       name = 'Confirmed Daily Increase')
reco_inc = go.Bar(x=daily_inc_table['Date'],
                       y=daily_inc_table['Recovered'],
                       # mode = 'lines',
                       name = 'Recovered Daily Increase')
dead_inc = go.Bar(x=daily_inc_table['Date'],
                       y=daily_inc_table['Deaths'],
                       # mode = 'lines',
                       name = 'Deaths Daily Increase')
actv_inc = go.Bar(x=daily_inc_table['Date'],
                       y=daily_inc_table['Active'],
                       # mode = 'lines',
                       name = 'Active Daily Increase')
rec_inc_rate = go.Bar(x=daily_inc_table['Date'],
                       y=daily_inc_table['Recovery%'],
                       # mode = 'lines',
                       name = 'Recovery Rate Change')
mor_inc_rate = go.Bar(x=daily_inc_table['Date'],
                       y=daily_inc_table['Mortality%'],
                       # mode = 'lines',
                       name = 'Mortality Rate Change')
incs = [conf_inc,reco_inc,dead_inc,actv_inc]
rates = [rec_inc_rate,mor_inc_rate]
layout = go.Layout(title='Global Daily COVID-19 Status')
fig_2 = go.Figure(data=incs, layout=layout)
fig_2.show()
rate_layout = go.Layout(title='Global Daily COVID-19 Status: Changes in Rates')
fig_rate_2 = go.Figure(data=rates, layout=rate_layout, )
fig_rate_2.show()

# Country wise Data

tab_conf = conf_global.melt(id_vars=["Province/State", "Country/Region", "Lat", "Long"], var_name="Date", value_name="Confirmed").fillna('')
tab_conf

tab_reco = reco_global.melt(id_vars=["Province/State", "Country/Region", "Lat", "Long"], var_name="Date", value_name="Recovered").fillna('')
tab_reco

tab_dead = dead_global.melt(id_vars=["Province/State", "Country/Region", "Lat", "Long"], var_name="Date", value_name="Deaths").fillna('')
tab_dead

tab_full = tab_conf.merge(tab_reco).merge(tab_dead)
tab_full['Active'] = tab_full['Confirmed'] - tab_full['Recovered'] - tab_full['Deaths']
tab_full['Mortality%'] = tab_full['Deaths']*100/tab_full['Confirmed']
tab_full['Recovery%'] = tab_full['Recovered']*100/tab_full['Confirmed']
tab_full

# Worldwide COVID-19 Status

world_map = px.density_mapbox(tab_full,
                              lat=tab_full['Lat'],
                              lon=tab_full['Long'],
                              z = 'Confirmed',
                              hover_name=tab_full['Province/State'],
                              hover_data=['Country/Region','Confirmed', 'Deaths', 'Recovered', 'Active'],
                              animation_frame='Date',
                              color_continuous_scale='portland',
                              range_color=[0, 10000],
                              radius=50,
                              opacity=1,
                              zoom=0.7,
                              height=800)
world_map.update_layout(title='Worldwide COVID-19 Status',
                        mapbox_style='open-street-map',
                        mapbox_center_lon=0, 
                        margin={'r':5, 't':25, 'l':5, 'b':5})

# Latest Update: Country wise Active COVID-19 patients

latest_update='7/13/20'
current_active = pd.DataFrame(tab_full[tab_full['Date']==latest_update])
current_active = current_active.reset_index().drop(['index'], axis=1)
current_active

pie_chart = px.pie(
                    data_frame= current_active,
                    values='Active',
                    names = 'Country/Region',
                    color = 'Country/Region',
                    hover_name = 'Active',
                    hover_data = ['Confirmed', 'Deaths', 'Recovered', 'Mortality%', 'Recovery%'],
                    title = 'Latest COVID-19 Update: Current Active',
                    template = 'presentation',
                    width = 1000,
                    height = 1000,
                    hole=0.25
)
pie_chart.update_traces(marker=dict(line=dict(color='#0000ff', width=1)),
                        rotation=0)
pie_chart

# Country Specific Statistics

def cases_country(country):
    # for some countries, data is spread over several Provinces
    if tab_full[tab_full['Country/Region'] == country]['Province/State'].nunique() > 1:
        country_table = tab_full[tab_full['Country/Region'] == country]
        country_df = pd.DataFrame(pd.pivot_table(country_table, values = ['Confirmed', 'Deaths', 'Recovered', 'Active', 'Recovery%', 'Mortality%'],
                              index='Date', aggfunc=sum).to_records())
        return country_df.set_index('Date')[['Confirmed', 'Deaths', 'Recovered', 'Active', 'Recovery%', 'Mortality%']]
    df = tab_full[(tab_full['Country/Region'] == country) 
                & (tab_full['Province/State'].isin(['', country]))]
    return df.set_index('Date')[['Confirmed', 'Deaths', 'Recovered', 'Active', 'Recovery%', 'Mortality%']]


def cases_province(province):
    # for some countries, data is spread over several Provinces
    df = tab_full[(tab_full['Province/State'] == province)]
    return df.set_index('Date')[['Confirmed', 'Deaths', 'Recovered', 'Active', 'Recovery%', 'Mortality%']]

def mapper(country_stat,country_list,country_num):
    country = country_list[country_num]
    country_stat = cases_country(country).fillna('').reset_index().rename(columns={'index':'Date'})
    conf_graph = go.Scatter(x=country_stat['Date'],
                           y=country_stat['Confirmed'],
                           mode = 'lines',
                           name = 'Confirmed')
    reco_graph = go.Scatter(x=country_stat['Date'],
                           y=country_stat['Recovered'],
                           mode = 'lines',
                           name = 'Recovered')
    dead_graph = go.Scatter(x=country_stat['Date'],
                           y=country_stat['Deaths'],
                           mode = 'lines',
                           name = 'Deaths')
    actv_graph = go.Scatter(x=country_stat['Date'],
                           y=country_stat['Active'],
                           mode = 'lines',
                           name = 'Active')

    graphs = [conf_graph,reco_graph,dead_graph,actv_graph]
    rates = [rec_rate,mor_rate]
    layout = go.Layout(title= country +' COVID-19 Status', )
    fig_1 = go.Figure(data=graphs, layout=layout)
    return fig_1

for country_num in range(count_country):
    fig_1 = mapper(country_stat,country_list,country_num)
    fig_1.show()
