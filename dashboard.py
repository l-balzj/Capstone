import pandas as pd 
import numpy as np
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go 

df = pd.read_csv('spacex_launch_dash.csv')
max_payload = df['Payload Mass (kg)'].max()
min_payload = df['Payload Mass (kg)'].min()

# Create the app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard', style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),

    # Dropdown manu for launch site selection
    dcc.Dropdown(np.append('All sites', df['Launch Site'].unique()), value='All', id='site-dropdown'),

    html.Br(),

    # Pie chart for success
    html.Div([], id='success-pie-chart'),

    html.Br(),

    # Slicer for the payload range
    html.P('Payload range (kg): '),
    dcc.RangeSlider(min_payload, 
                    max_payload, 
                    100, 
                    value=[min_payload, max_payload], 
                    marks={min_payload: str(min_payload), max_payload: str(max_payload)},
                    tooltip={'placement': 'bottom', 'always-visible': True},
                    id='payload-slider'),

    # Scatter chart, correlation payload and launch success
    html.Div([], id='success-payload-scatter-chart')
])

@app.callback(Output(component_id='success-pie-chart', component_property='children'), Input(component_id='site-dropdown', component_property='value'))

def pie_chart(launch_site):
    if launch_site == 'All sites':

        data = df[df['class'] == 1]
        fig1 = px.pie(data, names='Launch Site', values='class', title='Distribution of successful launches')

    else:
        data = df[df['Launch Site'] == launch_site]

        fig1 = px.pie(data, names='class', title=f'Successful vs unsuccesful launches in {launch_site}')

    return dcc.Graph(figure=fig1)


@app.callback(Output(component_id='success-payload-scatter-chart', component_property='children'), Input(component_id='payload-slider', component_property='value'))

def scatter_chart(payload_range):
    data = df[(df['Payload Mass (kg)'] > payload_range[0]) & (df['Payload Mass (kg)'] < payload_range[1])]

    fig2 = px.scatter(data, x='Payload Mass (kg)', y='class', color='Booster Version Category')

    return dcc.Graph(figure=fig2)


# Run the app
if __name__ == '__main__':
    app.run_server()
