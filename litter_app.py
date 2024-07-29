



#%% load libraries
from dash import Dash, dcc, html, Input, Output, dash_table # pip install dash
import dash_bootstrap_components as dbc 
from dash.exceptions import PreventUpdate
from dash_iconify import DashIconify



# import data libraries
import pandas as pd  # pip install pandas
import datetime as dt # pip install datetime
import numpy as np    # pip install numpy
import cv2

# plotting packages
import plotly.graph_objects as go #pip install plotly
import plotly.express as px
import folium  # pip install folium

# load data wrangling module
import app_data as ad


#%% load data
df = ad.litter
df_piv = ad.litter_sum

#%% create function

def mysum(main_category):

    temp = df.loc[df['main_category'] == main_category]
    temp_sum = temp['litter_count'].sum()
    temp_sum = int(temp_sum)

    return(temp_sum)


#%% Set Variables
# mapbox token
mytoken = 'Enter your mapbox token here.'

color_discrete_map = {'Softdrinks': '#3366CC',
                            'Food': '#DC3912',
                            'Other':'#FF9900',
                            'Smoking': '#109618',
                            'Alcohol': '#990099',
                            'Coffee': '#0099C6',
                            'Sanitary': '#DD4477',
                            'Custom_Litter_Type': '#66AA00',
                            'Industrial': '#B82E2E'}

# get totals by main category

total_litter = df['litter_count'].sum()
total_litter = int(total_litter)

total_softdrinks = mysum('Softdrinks')
total_food = mysum('Food')
total_other = mysum('Other')
total_smoking = mysum('Smoking')
total_alcohol = mysum('Alcohol')
total_coffee = mysum('Coffee')
total_sanitary = mysum('Sanitary')
total_custom = mysum('Custom_Litter_Type')
total_industrial = mysum('Industrial')
total_dogshit = mysum('Pet_Waste')

total_small_constributors = total_sanitary + total_custom + total_industrial + total_dogshit




#%% Density for at least 3 pickups
df_piv_three = df_piv[df_piv['total_count_pickup_dates'] >= 3].nlargest(10, 'avg_litter_pickedup')

density_bar_three = px.bar(df_piv_three, x='avg_litter_pickedup', 
       y= 'add_blocknum_street',
       hover_data={'add_blocknum_street': True,
                   'avg_litter_pickedup': True,
                   'total_count_pickup_dates': True},
        labels={'add_blocknum_street': 'Street Block',
                'avg_litter_pickedup': 'Average Litter Picked Up',
                'total_count_pickup_dates': 'Count of Outings'},
        color = 'add_blocknum_street',
        color_discrete_sequence=px.colors.qualitative.G10)

density_bar_three.update_layout(yaxis_title=None, xaxis_title = None,plot_bgcolor = 'lightgrey')
density_bar_three.update_layout(showlegend=False)
density_bar_three.update_layout(font=dict(size=15))


# test plot
density_fig = px.scatter_mapbox(df_piv_three, lat="min_lat", lon="min_lon",    
                        color='add_blocknum_street', size="avg_litter_pickedup",
                        color_discrete_sequence=px.colors.qualitative.G10,
                        zoom=13,
                        hover_data={'avg_litter_pickedup': True,
                                    'min_lat': False,
                                    'min_lon': False,
                                    'add_blocknum_street': True,
                                    'total_count_pickup_dates': True},
                        labels = {'add_blocknum_street': 'Street Block',
                                  'total_count_pickup_dates': 'Count of Outings',
                                  'avg_litter_pickedup': 'Average Litter Picked Up'}
                        )
density_fig.update_layout(legend_title_text = 'Street Block')
density_fig.update_layout(mapbox_accesstoken = mytoken)
# density_fig.update_layout(legend=dict(bgcolor = 'LightGrey',
#                                   bordercolor = 'Black'))
density_fig.update_layout(showlegend=False)

# %% app instantiation

app = Dash(__name__,
                external_stylesheets=[dbc.themes.COSMO])

#%% app layout

app.layout = html.Div([
    html.Br(),



    html.H4(dcc.Markdown("[Iowa City Litter Crew](https://www.meetup.com/iowa-city-litter-crew/)"),
            style= {'textAlign': 'left'}),
    
    html.H1('Litter and Litter Data Collected in Iowa City',
            style={'textAlign':'center'}),

    html.Br(),

    html.H1('Litter Collected',
            style = {'textAlign': 'center'}),
    
    html.Br(),

    dbc.Row([


        dbc.Col([
            dbc.Card([
                dbc.CardBody(
                    [
                        dbc.Row([
                            dbc.Col([
                                html.H4('Total Litter Collected', className='card-title'),
                                DashIconify(icon="f7:trash",
                                    width=30)
                            ]),
                            dbc.Col([
                                html.P(total_litter, 
                                       className= 'card-text',
                                       style={'textAlign': 'right',
                                              'fontSize': 40},
                                       )
                            ]),
                        ])
                        
                    ]
                )
            ])
        ]),

        dbc.Col([
            dbc.Card([
                dbc.CardBody(
                    [
                        dbc.Row([
                            dbc.Col([
                                html.H4('Soft Drinks', className='card-title'),
                                DashIconify(icon="mdi:bottle-soda-classic-outline",
                                    width=30)
                            ]),
                            dbc.Col([
                                html.P(total_softdrinks, 
                                       className= 'card-text',
                                       style={'textAlign': 'right',
                                              'fontSize': 40},
                                       )
                            ]),
                        ])
                        
                    ]
                )
            ])
        ]),

        dbc.Col([
            dbc.Card([
                dbc.CardBody(
                    [
                        dbc.Row([
                            dbc.Col([
                                html.H4('Food', className='card-title'),
                                DashIconify(icon="pajamas:food",
                                    width=30)
                            ]),
                            dbc.Col([
                                html.P(total_food, 
                                       className= 'card-text',
                                       style={'textAlign': 'right',
                                              'fontSize': 40},
                                       )
                            ]),
                        ])
                        
                    ]
                )
            ])
        ]),


        dbc.Col([
            dbc.Card([
                dbc.CardBody(
                    [
                        dbc.Row([
                            dbc.Col([
                                html.H4('Other', className='card-title'),
                                DashIconify(icon="material-symbols:shopping-bag-outline",
                                    width=30)
                            ]),
                            dbc.Col([
                                html.P(total_other, 
                                        className= 'card-text',
                                        style={'textAlign': 'right',
                                                'fontSize': 40},
                                        )
                            ]),
                        ])
                        
                    ]
                )
            ])
        ]),


    ]),


    dbc.Row([

        dbc.Col([
            dbc.Card([
                dbc.CardBody(
                    [
                        dbc.Row([
                            dbc.Col([
                                html.H4('Smoking', className='card-title'),
                                DashIconify(icon="mdi:smoking",
                                    width=30)
                            ]),
                            dbc.Col([
                                html.P(total_smoking, 
                                        className= 'card-text',
                                        style={'textAlign': 'right',
                                                'fontSize': 40},
                                        )
                            ]),
                        ])
                        
                    ]
                )
            ])
        ]),

        dbc.Col([
            dbc.Card([
                dbc.CardBody(
                    [
                        dbc.Row([
                            dbc.Col([
                                html.H4('Alcohol', className='card-title'),
                                DashIconify(icon="streamline:champagne-party-alcohol",
                                    width=30)
                            ]),
                            dbc.Col([
                                html.P(total_alcohol, 
                                        className= 'card-text',
                                        style={'textAlign': 'right',
                                                'fontSize': 40},
                                        )
                            ]),
                        ])
                        
                    ]
                )
            ])
        ]),

        
        dbc.Col([
            dbc.Card([
                dbc.CardBody(
                    [
                        dbc.Row([
                            dbc.Col([
                                html.H4('Coffee', className='card-title'),
                                DashIconify(icon="ep:coffee",
                                    width=30)
                            ]),
                            dbc.Col([
                                html.P(total_coffee, 
                                        className= 'card-text',
                                        style={'textAlign': 'right',
                                                'fontSize': 40},
                                        )
                            ]),
                        ])
                        
                    ]
                )
            ])
        ]),




     

        dbc.Col([
            dbc.Card([
                dbc.CardBody(
                    [
                        dbc.Row([
                            dbc.Col([
                                html.H4('Sanitary, Industrial, and Custom', className='card-title'),
                                DashIconify(icon="f7:facemask",
                                    width=30)
                            ]),
                            dbc.Col([
                                html.P(total_small_constributors, 
                                        className= 'card-text',
                                        style={'textAlign': 'right',
                                                'fontSize': 40},
                                        )
                            ]),
                        ])
                        
                    ]
                )
            ])
        ]),

    ]),

    html.Br(),
    html.Br(),

    html.H1('Litter Location, Composition and Timeline',
            style = {'textAlign': 'center'}), 
    html.Br(),

    html.H5('Select or remove item(s) from the drop down.'),
    dcc.Dropdown(
        id = 'litter_type_dd',
        placeholder = 'Select a litter type...',
        multi=True,
        value = ['Coffee', 'Food'],
        clearable = True,
        searchable = True,
        options = [{'label': main_category,
                   'value': main_category}
                   for main_category in sorted(df['main_category'].unique())], style={'width': '70%',
                                                                                      'height': '100%',
                                                                                      'font-size': 25}),

    html.Br(),

    html.H5('Select the date range.'),    

    dcc.DatePickerRange(
        id = 'date_range',
        min_date_allowed = df['date_taken_date'].min(),
        max_date_allowed = df['date_taken_date'].max(),
        initial_visible_month = dt.date(2023,8,1),
        start_date = df['date_taken_date'].min(),
        end_date = df['date_taken_date'].max()
        
    ), 

    html.Br(),
    html.Br(),

    # dash_table.DataTable(
                
    #             id = 'mytable',
    #             fill_width=False,
    #             style_cell={'font_size': '20',
    #                         'text_align': 'center'}),
    
    dbc.Row([

        dbc.Col([

            dash_table.DataTable(
                
                id = 'mytable',
                fill_width=False,
                style_cell={'fontSize': 20,
                            'text_align': 'center',
                            'padding': '5px'},
                style_header={'fontWeight': 'bold'},
                style_table={'paddingLeft':'50px',
                             'paddingTop': '50px'})
                
    ,
                ]),
        

        dbc.Col([dcc.Graph(id = 'sunburst_chart',
                           style = {'height': '40vh',
                                    'width' : '30vw',
                                    'paddingLeft':'0px',
                                    'paddingTop':'0px'})
        
        ]) ,

        dbc.Col([
            dcc.Graph(id = 'litter_density_map',
                      style = {'height': '50vh',
                               'width': '50vw'},
            config = {'modeBarButtonsToRemove': ['select','zoom', "pan2d", "autoScale",
                                                   "autoScale2d" "select2d", "lasso2d"]})

        ]),



    ]),  

    
    dcc.Graph(id = 'bar_chart',
            style = {'height': '50vh'},
            config = {'modeBarButtonsToRemove': ['select','zoom', "pan2d", "autoScale",
                                                   "autoScale2d" "select2d", "lasso2d"]}),
    
    html.Br(),
    html.Br(),
    html.H1('Top 10 Litter Density by Street Block',
            style = {'textAlign': 'center'}),
    
    html.Br(),
    html.H3('Street blocks with highest average litter with at least 3 unique event dates.',
            style = {'textAlign': 'center'}),
    
   
    

    

    dbc.Row([
        dbc.Col([
            dcc.Graph(figure=density_fig,
              style = {'width': '40vw', 'height': '50vh'},
              config = {'modeBarButtonsToRemove': ['select','zoom', "pan2d", "autoScale",
                                                   "autoScale2d" "select2d", "lasso2d"]})
        ]),

        dbc.Col([
            dcc.Graph(figure=density_bar_three,
              style = {'width': '40vw', 'height': '50vh'},
              config = {'modeBarButtonsToRemove': ['select','zoom', "pan2d", "autoScale",
                                                   "autoScale2d" "select2d", "lasso2d"]})
        ]),

    
    ]),
    

      
    
   
])

#%% Map Chart
@app.callback(Output('litter_density_map','figure'),
              Input('litter_type_dd','value'),
              Input('date_range', 'start_date'),
              Input('date_range', 'end_date'))


def density_map(mycategory, start_date, end_date):

    if not start_date or not end_date or not mycategory:
        raise PreventUpdate   
    
    temp_df = df.loc[df['main_category'].isin(mycategory)]


    temp_df = temp_df.loc[temp_df['date_taken_date'].between(pd.to_datetime(start_date), 
                                                                 pd.to_datetime(end_date))]
    
    
    
    
    fig = px.scatter_mapbox(temp_df, lat="lat", lon="lon",    
                            color="main_category", 
                            size="litter_count",
                            zoom=13,
                            color_discrete_map=color_discrete_map,
                            hover_data={'litter_count': True,
                                    'lat': False,
                                    'lon': False,
                                    'main_category': True},
                            labels = {'litter_count': 'Litter Count',
                                      'main_category': 'Litter Type'})
    
    fig.update_layout(legend=dict(bgcolor = 'LightGrey',
                                  bordercolor = 'Black',
                                  orientation = 'v',
                                  yanchor='top',
                                  x=0.01)),
    
    fig.update_layout(legend_title = 'Litter Type',
                      font=dict(size = 15))
    
    fig.update_layout(mapbox_accesstoken = mytoken)
    return fig

#%% Sunburst Chart

@app.callback(Output('sunburst_chart','figure'),
              Input('litter_type_dd','value'),
              Input('date_range', 'start_date'),
              Input('date_range', 'end_date'))

def sunburst_chart(mycategory, start_date, end_date):

    if not start_date or not end_date or not mycategory:
        raise PreventUpdate
    
    
        
   
    temp_df = df.loc[df['main_category'].isin(mycategory)]


    temp_df = temp_df.loc[temp_df['date_taken_date'].between(pd.to_datetime(start_date), 
                                                                 pd.to_datetime(end_date))]
    
    temp_piv = pd.DataFrame(temp_df.groupby(['main_category', 'sub_category'])['litter_count'].sum().reset_index())



    fig = px.sunburst(temp_piv, 
                  path = ['main_category', 'sub_category'], 
                  values='litter_count', 
                  hover_name='main_category', 
                  color = 'main_category',
                  color_discrete_map=color_discrete_map)
             
    
    
    fig.update_traces(textinfo="label+percent parent")
    #fig.update_traces(hovertemplate = "Main Category: %{parent}: <br>Sub Category: %{label} </br>Count:%{value} </br>Percentage:%{percentParent:.02f}")
    fig.update_traces(hovertemplate = "Main Category: %{parent}: <br>Sub Category: %{label} </br>Count:%{value}")
    fig.update_layout(margin = dict(t=0, l=0, r=0, b=0))
    #fig.layout.coloraxis.colorbar['thickness'] = 200
    fig.update_layout(font=dict(size=15))
    return fig

#%%


#%% Summary Table

@app.callback(Output('mytable','data'),
              Input('litter_type_dd','value'),
              Input('date_range', 'start_date'),
              Input('date_range', 'end_date'))



def get_my_table(mycategory, start_date, end_date):

    if not start_date or not end_date or not mycategory:
        raise PreventUpdate   
    
    mytable = df.loc[df['main_category'].isin(mycategory)]


    mytable = mytable.loc[mytable['date_taken_date'].between(pd.to_datetime(start_date), 
                                                                 pd.to_datetime(end_date))]
    
    mytable = pd.DataFrame(mytable.groupby(['main_category'])['litter_count'].sum().reset_index())
    mytable = mytable.sort_values(by = 'litter_count', ascending=False)

    mytable = (pd.DataFrame([*mytable.values, ['Total', *mytable.sum(numeric_only=True).values]], 
              columns=mytable.columns))
    
    mytable = mytable.rename(columns={'main_category': 'Main Category',
                                      'litter_count': 'Litter Count'})
    
    

    return mytable.to_dict('records')




#%% bar chart

@app.callback(Output('bar_chart','figure'),
              Input('litter_type_dd','value'),
              Input('date_range', 'start_date'),
              Input('date_range', 'end_date'))


def my_bar_chart(mycategory, start_date, end_date):

    if not start_date or not end_date or not mycategory:
        raise PreventUpdate

    temp_df = df.loc[df['main_category'].isin(mycategory)]


    temp_df = temp_df.loc[temp_df['date_taken_date'].between(pd.to_datetime(start_date), 
                                                                 pd.to_datetime(end_date))]
    
    temp_df = pd.DataFrame(temp_df.groupby(['date_taken_date', 'main_category'])['litter_count'].sum().reset_index())

    fig = px.bar(temp_df,
             x='date_taken_date',
             y = 'litter_count',
            hover_data={'date_taken_date': True,
                        'main_category' : True,
                         'litter_count': True},
            labels = {
                'date_taken_date': 'Date Litter Picked Up',
                'litter_count': 'Litter Count',
                'main_category': 'Litter Type',
            },
            color = 'main_category',
            color_discrete_map=color_discrete_map)
    
    fig.update_layout(showlegend = False)
    fig.update_layout(plot_bgcolor = 'lightgrey')
    fig.update_layout(font=dict(size=15))
    return fig






#%% Run App
if __name__ == '__main__':
    app.run_server()