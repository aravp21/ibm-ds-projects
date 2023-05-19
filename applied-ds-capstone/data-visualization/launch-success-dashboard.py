# import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# read data
spacex_df = pd.read_csv("spacex_launch_dash_data.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# create Dash application
app = dash.Dash(__name__)

# create app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable launch site selection
                                # default select value is for all sites
                                dcc.Dropdown(id='site-dropdown', options=[{'label': 'All Sites', 'value': 'ALL'},
                                                                        {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'}, 
                                                                        {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                                        {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'}, 
                                                                        {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}], 
                                            value='ALL', placeholder="Select a Launch Site Here", searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # show success vs. failure counts for specific launch site, if selected
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=1000, marks={0: '0', 2500: '2500', 5000: '5000',
                                                                                                        7500: '7500', 10000: '10000'},
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart'))])

# TASK 2: Add a callback function for site-dropdown as input and success-pie-chart as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class', names='Launch Site', title="Total Successful Launches by Site")
        return fig
    else:
        filtered_df = spacex_df.loc[spacex_df['Launch Site'] == entered_site]
        fig = px.pie(filtered_df, names='class', title=f"Total Successful Launches for Site {entered_site}")
        return fig

# TASK 4: Add a callback function for site-dropdown and payload-slider as inputs and success-payload-scatter-chart as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value')])

def get_scatter_chart(entered_site, payload_range):
    filtered_df = spacex_df
    min_range = int(payload_range[0])
    max_range = int(payload_range[1])
    if entered_site == 'ALL':
        filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= min_range) & (spacex_df['Payload Mass (kg)'] <= max_range)]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category', title="Correlation Between Payload and Success for All Sites")
        return fig
    else:
        filtered_df = spacex_df.loc[(spacex_df['Launch Site'] == entered_site)]
        filtered_df = filtered_df[(spacex_df['Payload Mass (kg)'] >= min_range) & (spacex_df['Payload Mass (kg)'] <= max_range)]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category', title=f"Correlation Between Payload and Success for Site {entered_site}")
        return fig

# run app
if __name__ == '__main__':
    app.run_server()
