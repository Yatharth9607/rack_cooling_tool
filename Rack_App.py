# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 14:13:55 2019

@author: SESA539950
"""

import numpy as np
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import base64
import Rack_solver
import os

Q_id = ['Q_IT', 'Q_AC', 'Q_SP', 'Q_L', 'Q_FD', 'Q_FP', 'Q_RD', 'Q_RP', 'Q_VF_f', 'Q_VF_r']
y_axis = ['Server<Br>Plane', 'Overall<Br>Leakage']

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
# Loading screen CSS
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/brPBPO.css"})
# Title of the browser tab
app.title = 'MDC Cooling Calculator'

colors = {
    'background': '#ffffff',
    'text': 'darkgrey',
    'dark grey': '#626469',
    'anthracite grey': '3333333'
}

image_filename = 'schneider_LIO_White_RGB.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())
src = 'data:image/png;base64,{}'.format(encoded_image.decode())
schematic = base64.b64encode(open('schematic.png', 'rb').read())
life_green = '#3DCD58'


def title_header():
    return html.Div(children=[html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()),
                                       style={'width': 200, 'height': 55.1428571429}),
                              html.Div(style={"flexGrow": 10},
                                       children=[html.H1(
                                           children='Micro Data Center Cooling Calculator',
                                           style={
                                               'textAlign': 'left',
                                               'color': 'white',
                                               'margin': 0,
                                               'padding-left': '10%'
                                           })]
                                       )
                              ],
                    style={'display': 'flex',
                           'backgroundColor': life_green,
                           'padding': '1rem 0.5rem 1rem 0.5rem',
                           'marginBottom': '2rem'})


simulation = ['AC Unit', 'Ventilation Fans (Economizer Mode)']
simulation_options = ['AC Fans on UPS', 'Vent Fans on UPS', 'Turn on Vent Fans (on UPS)']

simulation01 = ['AC Unit', 'Front Ventilation Fan (Economizer Mode)',
                'Rear Ventilation Fan (Economizer Mode)', 'Both Ventilation Fans (Economizer Mode)']
simulation_options01 = ['AC Fans (on UPS)', 'Front Ventilation Fan (on UPS)',
                        'Rear Ventilation Fan (on UPS)',
                        'Front Ventilation Fan (on UPS)', 'Rear Ventilation Fan (on UPS)', 'Both Ventilation Fans (on UPS)']

app.layout = html.Div(children=[

    # TITLE
    title_header(),

    html.Div(className='row',
             children=[

                 html.H5(
                     'Error!! The size of rack must be greater than the sum of total IT population, number of blanking panels, UPS size and AC Unit size',
                     id='error-id',
                     style={'display': 'none'}),

                 html.Div(className='row',
                          children=[

                              # RACK CONFIGURATION

                              html.Div(style={'style': 'flex', 'flex-direction': 'column', 'padding-left': '4%'},
                                       children=[

                                           html.H5(children='Rack',
                                                   style={'textAlign': 'left', 'color': 'grey',
                                                          'borderBottom': 'solid 1px grey'}),

                                           html.Div(children=[
                                               html.Label(children='Rack Size (U)',
                                                          style={'display': 'inline-block', 'padding-left': '10px',
                                                                 'padding-right': '10px'}),
                                               dcc.Dropdown(id='size_rack-id', value=24,
                                                            options=[{'label': 24, 'value': 24},
                                                                     {'label': 42, 'value': 42},
                                                                     {'label': 48, 'value': 48}],
                                                            style={'display': 'inline-block', 'margin-right': '10px',
                                                                   'width': '75px', 'text-align': 'center'})],
                                               style={'display': 'flex', 'justify-content': 'space-between',
                                                      'padding-right': '20px'}),

                                           html.Div(children=[
                                               html.Label(children='Total IT Population in Rack (U)',
                                                          style={'display': 'inline-block', 'padding-left': '10px',
                                                                 'padding-right': '10px'}),
                                               dcc.Dropdown(id='n_IT-id', value=10,
                                                            style={'display': 'inline-block', 'margin-right': '10px',
                                                                   'width': '75px', 'text-align': 'center'})],
                                               style={'display': 'flex', 'justify-content': 'space-between',
                                                      'padding-right': '20px'}),

                                           html.Div(children=[
                                               html.Label(children='Total IT Power (kW)',
                                                          style={'display': 'inline-block', 'padding-left': '10px',
                                                                 'padding-right': '10px'}),
                                               dcc.Input(id='q_IT-id', value=3.5, type='number', min=0.5, max=99,
                                                         step=0.5,
                                                         style={'display': 'inline-block', 'margin-right': '10px',
                                                                'width': '75px', 'text-align': 'center'})],
                                               style={'display': 'flex', 'justify-content': 'space-between',
                                                      'padding-right': '20px'}),

                                           html.Div(children=[
                                               html.Label(children='Number of Blanking Panels in Rack (U)',
                                                          style={'display': 'inline-block', 'padding-left': '10px',
                                                                 'padding-right': '10px'}),
                                               dcc.Dropdown(id='n_BP-id', value=0,
                                                            style={'display': 'inline-block', 'margin-right': '10px',
                                                                   'width': '75px', 'text-align': 'center'})],
                                               style={'display': 'flex', 'justify-content': 'space-between',
                                                      'padding-right': '20px', 'padding-top': '2%'}),

                                           # ADVANCED OPTIONS

                                           html.Div(children=[
                                               html.Button(children='Advanced',
                                                           id='button',
                                                           n_clicks=0,
                                                           style={'display': 'flex', 'justify-content': 'center',
                                                                  'width': '120px',
                                                                  'border-radius': '50%'}), ],
                                               style={'display': 'flex', 'justify-content': 'center'}),

                                           html.Div(style={'padding-top': '2%'}),

                                           html.Div(className='twelve columns',
                                                    id='advanced-id',
                                                    children=[
                                                        html.Div(children=[
                                                            html.Label('Rack leakage resistance multiplier:'),
                                                            html.Div(style={'padding-top': '2%'}),

                                                            html.Div(id='front_leakage-id',
                                                                     children=[
                                                                         html.Label(children='Front Leakage Resistance',
                                                                                    style={'display': 'inline-block',
                                                                                           'textAlign': 'center',
                                                                                           'font-weight': 'bold'}),
                                                                         html.Div(children=[
                                                                             dcc.Slider(id='slider-1', min=-2, max=2,
                                                                                        step=0.01, value=0,
                                                                                        updatemode='drag',
                                                                                        marks={'-2': '0.01',
                                                                                               '-1': '0.1',
                                                                                               '0': '1', '1': '10',
                                                                                               '2': '100'},
                                                                                        included=False)],
                                                                             style={'padding-left': '10%',
                                                                                    'padding-right': '10%'}),
                                                                         html.Div(children=[
                                                                             html.Label(children='less sealed',
                                                                                        style={
                                                                                            'display': 'inline-block',
                                                                                            'float': 'left'}),
                                                                             html.Label(children='highly sealed',
                                                                                        style={
                                                                                            'display': 'inline-block',
                                                                                            'float': 'right'})],
                                                                             className='twelve columns',
                                                                             style={'padding-top': '5%',
                                                                                    'padding-right': '2%'})]),

                                                            html.Div(id='rear_leakage-id',
                                                                     style={'padding-top': '5%'},
                                                                     children=[
                                                                         html.Label(children='Rear Leakage Resistance',
                                                                                    style={'display': 'inline-block',
                                                                                           'textAlign': 'center',
                                                                                           'font-weight': 'bold'}),
                                                                         html.Div(children=[
                                                                             dcc.Slider(id='slider-2', min=-2, max=2,
                                                                                        step=0.01, value=0,
                                                                                        updatemode='drag',
                                                                                        marks={'-2': '0.01',
                                                                                               '-1': '0.1',
                                                                                               '0': '1', '1': '10',
                                                                                               '2': '100'},
                                                                                        included=False)],
                                                                             style={'padding-left': '10%',
                                                                                    'padding-right': '10%'}),
                                                                         html.Div(children=[
                                                                             html.Label(children='less sealed',
                                                                                        style={
                                                                                            'display': 'inline-block',
                                                                                            'float': 'left'}),
                                                                             html.Label(children='highly sealed',
                                                                                        style={
                                                                                            'display': 'inline-block',
                                                                                            'float': 'right'})],
                                                                             className='twelve columns',
                                                                             style={'padding-top': '5%',
                                                                                    'padding-right': '2%'})]),
                                                        ],
                                                            style={'padding-left': '2%', 'padding-top': '2%',
                                                                   'padding-right': '2%', 'padding-bottom': '2%'}),
                                                    ]),
                                           # UPS CONFIGURATION

                                           html.H5(children='UPS',
                                                   style={'textAlign': 'left', 'color': 'grey',
                                                          'borderBottom': 'solid 1px grey'}),

                                           html.Div(children=[
                                               html.Label(children='UPS Size (U)',
                                                          style={'display': 'inline-block', 'padding-left': '10px',
                                                                 'padding-right': '10px'}),
                                               dcc.Dropdown(id='size_UPS-id', value=1,
                                                            style={'display': 'inline-block', 'margin-right': '10px',
                                                                   'width': '75px', 'text-align': 'center'})],
                                               style={'display': 'flex', 'justify-content': 'space-between',
                                                      'padding-right': '20px'}),

                                           html.Div(children=[
                                               html.Label(children='UPS Power Rating (kW)',
                                                          style={'padding-left': '10px', 'padding-right': '10px'}),
                                               dcc.Input(id='q_UPS-id', value=5, type='number', min=0.5, max=99,
                                                         step=0.5,
                                                         style={'margin-right': '10px', 'width': '75px',
                                                                'text-align': 'center'})],
                                               style={'display': 'flex', 'justify-content': 'space-between',
                                                      'padding-right': '20px'}),

                                           html.Div(children=[
                                               html.Label(children='UPS Run Time (min)',
                                                          style={'padding-left': '10px', 'padding-right': '10px'}),
                                               dcc.Input(id='t_UPS-id', value=5, type='number', min=1, max=99,
                                                         style={'margin-right': '10px', 'width': '75px',
                                                                'text-align': 'center'})],
                                               style={'display': 'flex', 'justify-content': 'space-between',
                                                      'padding-right': '20px', 'padding-top': '2%'}),

                                       ],
                                       className='four columns'),

                              # COOLING SYSTEM CONFIGURATION

                              html.Div(style={'style': 'flex', 'flex-direction': 'column', 'padding-right': '0%'},
                                       children=[
                                           html.H5(children='Cooling Source',
                                                   style={'textAlign': 'left', 'color': 'grey',
                                                          'borderBottom': 'solid 1px grey'}),

                                           html.Div(children=[
                                               html.Label(children='Before Power Failure:',
                                                          style={'display': 'inline-block',
                                                                 'padding-left': '10px',
                                                                 'padding-right': '10px',
                                                                 'font-weight': 'bold'}),
                                               dcc.Dropdown(id='case',
                                                            style={'display': 'inline-block',
                                                                   'padding-right': '0px',
                                                                   'width': '300px',
                                                                   'text-align': 'center'},
                                                            options=[{'label': k, 'value': k} for k
                                                                     in simulation01],
                                                            value=simulation01[0])],
                                               style={'display': 'flex',
                                                      'justify-content': 'space-between',
                                                      'padding-right': '0px',
                                                      'padding-top': '2%'}),

                                           html.Div(children=[
                                               html.Label(children='After Power Failure:',
                                                          style={'display': 'inline-block',
                                                                 'padding-left': '10px',
                                                                 'padding-right': '10px',
                                                                 'vertical-align': 'top',
                                                                 'font-weight': 'bold'}),
                                               html.Div(children=[
                                                   dcc.Checklist(id='AC_option',
                                                                 options=[
                                                                     {'label': simulation_options01[0],
                                                                      'value': simulation_options01[0]}],
                                                                 values=[]),
                                                   dcc.Checklist(id='VF_option',
                                                                 # options=[
                                                                 #     {'label': simulation_options01[1],
                                                                 #      'value': simulation_options01[1]}],
                                                                 values=[])],
                                                   style={'textAlign': 'left', 'display': 'inline-block',
                                                          'padding-left': '10%'}
                                               )],
                                               style={'justify-content': 'space-between',
                                                      'display': 'inlilne-block'}),

                                           html.Div(children=[
                                               html.Label(className='column',
                                                          children='Ambient Temperature (\u00B0F)',
                                                          style={'padding-left': '10px', 'padding-right': '10px'}),
                                               dcc.Input(id='T_amb-id', value=70, type='number', min=0, max=999,
                                                         style={'margin-right': '22.5px', 'width': '75px',
                                                                'text-align': 'center'})],
                                               style={'display': 'flex', 'justify-content': 'space-between',
                                                      'padding-top': '4%'}),

                                           html.Div(children=[
                                               html.Label(className='column',
                                                          children='Cooling System:',
                                                          style={'padding-left': '0px',
                                                                 'padding-right': '10px',
                                                                 'font-weight': 'bold'}),
                                               dcc.Input(id='Fake-id1', value='AC', type='text',
                                                         readOnly=True,
                                                         style={'margin-right': '35px', 'width': '50px',
                                                                'font-weight': 'bold',
                                                                'text-align': 'center', 'border': 'none'}),
                                               dcc.Input(id='Fake-id2', value='Vent Fans', type='text',
                                                         readOnly=True,
                                                         style={'margin-right': '10px', 'width': '100px',
                                                                'font-weight': 'bold',
                                                                'text-align': 'center',
                                                                'border': 'none'})],
                                               style={'display': 'flex',
                                                      'justify-content': 'space-between',
                                                      'padding-top': '2%'}),

                                           html.Div(id='unit_size-id',
                                                    children=[
                                                        html.Label(className='column',
                                                                   children='Unit Size (U)',
                                                                   style={'display': 'inline-block',
                                                                          'padding-left': '0px',
                                                                          'padding-right': '10px'}),
                                                        dcc.Dropdown(id='size_AC-id', value=5,
                                                                     style={'display': 'inline-block',
                                                                            'margin-right': '35px',
                                                                            'width': '75px',
                                                                            'text-align': 'center'}),
                                                        dcc.Input(id='Fake-id3', value='N/A', type='text',
                                                                  readOnly=True,
                                                                  style={'margin-right': '22.5px',
                                                                         'width': '75px',
                                                                         'text-align': 'center',
                                                                         'border': 'none'})],
                                                    style={'display': 'flex',
                                                           'justify-content': 'space-between',
                                                           'padding-top': '2%'}),

                                           html.Div(children=[
                                               html.Label(className='column',
                                                          children='Open Flow Rate (cfm)',
                                                          style={'padding-left': '0px',
                                                                 'padding-right': '10px'}),
                                               dcc.Input(id='Q_AC_max-id', value=726.8, type='number',
                                                         min=0, max=10000,
                                                         style={'margin-right': '10px', 'width': '100px',
                                                                'text-align': 'center'}),
                                               dcc.Input(id='Q_VF_max-id', value=684, type='number', min=0,
                                                         max=10000,
                                                         style={'margin-right': '10px', 'width': '100px',
                                                                'text-align': 'center'})],
                                               style={'display': 'flex',
                                                      'justify-content': 'space-between',
                                                      'padding-top': '0%'}),

                                           html.Div(children=[
                                               html.Label(className='column',
                                                          children='Stagnation Pressure (inH\u2082O)',
                                                          style={'padding-left': '0px',
                                                                 'padding-right': '10px'}),
                                               dcc.Input(id='P_AC_stag-id', value=42, type='number', min=0,
                                                         max=99999,
                                                         style={'margin-right': '10px', 'width': '100px',
                                                                'text-align': 'center'}),
                                               dcc.Input(id='P_VF_stag-id', value=0.87, type='number',
                                                         min=0, max=99999,
                                                         style={'margin-right': '10px', 'width': '100px',
                                                                'text-align': 'center'})],
                                               style={'display': 'flex',
                                                      'justify-content': 'space-between',
                                                      'padding-top': '2%'}),

                                           html.Div(id='set_point-id',
                                                    children=[
                                                        html.Label(className='column',
                                                                   children='Set Point Temperature (\u00B0F)',
                                                                   style={'padding-left': '0px',
                                                                          'padding-right': '10px'}),
                                                        dcc.Input(id='T_AC-id', value=70, type='number',
                                                                  min=0, max=999,
                                                                  style={'margin-right': '35px',
                                                                         'width': '75px',
                                                                         'text-align': 'center'}),
                                                        dcc.Input(id='Fake-id5', value='N/A', type='text',
                                                                  readOnly=True,
                                                                  style={'margin-right': '22.5px',
                                                                         'width': '75px',
                                                                         'text-align': 'center',
                                                                         'border': 'none'})],
                                                    style={'display': 'flex',
                                                           'justify-content': 'space-between',
                                                           'padding-top': '0%'}),

                                           # html.Div(children=[
                                           #     html.Label(children='Airflow rate values (cfm)'),
                                           #     html.Label(id='Q_values-id',
                                           #                style={'display': 'flex', 'justify-content': 'space-between'}
                                           #                )
                                           # ]),
                                           #
                                           # html.Div(children=[
                                           # html.Label(children='Temperature values (K)'),
                                           # html.Label(id='T_values-id',
                                           #            style={'display': 'flex', 'justify-content': 'space-between'}
                                           #            )
                                           # ])

                                       ], className='four columns'),

                              html.Div(style={'style': 'flex', 'flex-direction': 'column', 'padding-right': '4%'},
                                       children=[

                                           html.Div(style={'style': 'flex', 'flex-direction': 'column'},
                                                    children=[

                                                        # SCHEMATIC DIAGRAM

                                                        html.H5(children='Schematic',
                                                                style={'textAlign': 'left', 'color': 'grey',
                                                                       'borderBottom': 'solid 1px grey'}),
                                                        html.Div(children=[
                                                            html.Img(id='schematic-id',
                                                                     src='data:image/png;base64,{}'.format(
                                                                         schematic.decode()),
                                                                     style={'display': 'inline-block',
                                                                            'height': '340px'},
                                                                     className='eight columns'),
                                                            dcc.Graph(id='rack_graph',
                                                                      style={'display': 'inline-block',
                                                                             'height': '330px'},
                                                                      config={'displayModeBar': False},
                                                                      className='four columns'),
                                                        ]),
                                                    ], className='twelve columns'),
                                       ], className='four columns'),
                          ]),

                 html.Hr(
                     style={'display': 'block', 'border-style': 'dashed', 'margin-top': '5px', 'margin-bottom': '0'}
                 ),
                 html.Div(className='row',
                          children=[

                              # RESULTS TO PRINT

                              html.Div(className='three columns',
                                       children=[
                                           html.Div(className='twelve columns',
                                                    style={'display': 'flex', 'flex-direction': 'column',
                                                           'padding-left': '5%'},
                                                    children=[
                                                        html.H5(children='Results',
                                                                style={'textAlign': 'left', 'color': 'grey',
                                                                       'borderBottom': 'solid 1px grey'}),
                                                        html.Label('Global Air Ratio'),

                                                        html.Div(style={'display': 'flex', 'padding-top': '5%',
                                                                        'justify-content': 'space-between'},
                                                                 children=[
                                                                     html.Label(children='Before Power Failure',
                                                                                className='seven columns',
                                                                                style={'padding-left': '5%'}),
                                                                     html.Label(id="global_ar_ss-id",
                                                                                children='-',
                                                                                style={'display': 'inline-block',
                                                                                       'color': 'green',
                                                                                       'font-weight': 'bold',
                                                                                       'textAlign': 'center'},
                                                                                className='four columns')]),
                                                        html.Div(style={'display': 'flex', 'padding-top': '5%',
                                                                        'justify-content': 'space-between'},
                                                                 children=[
                                                                     html.Label(children='After Power Failure',
                                                                                className='seven columns',
                                                                                style={'padding-left': '5%'}),
                                                                     html.Label(id="global_ar_tr-id",
                                                                                children='-',
                                                                                style={'display': 'inline-block',
                                                                                       'color': 'green',
                                                                                       'font-weight': 'bold',
                                                                                       'textAlign': 'center'},
                                                                                className='four columns')]),
                                                    ]), ]),

                              # AIRFLOW RATE GRAPH

                              html.Div(className='five columns',
                                       children=[
                                           html.Div(className='twelve columns',
                                                    style={'display': 'flex', 'flex-direction': 'column',
                                                           'padding-left': '0%'},
                                                    children=[
                                                        html.H5(children='Airflow',
                                                                style={'textAlign': 'left', 'color': 'grey',
                                                                       'borderBottom': 'solid 1px grey'}),
                                                        dcc.Dropdown(id='Q_graph_layout-id',
                                                                     options=[
                                                                         {'label': 'Before Power Failure', 'value': 1},
                                                                         {'label': 'After Power Failure', 'value': 2}],
                                                                     value=2,
                                                                     style={'display': 'block'}),
                                                        html.Div(style={'style': 'flex'},
                                                                 children=[
                                                                     dcc.Graph(id='Q_graph',
                                                                               style={'style': 'flex',
                                                                                      'height': '250px'},
                                                                               config={'displayModeBar': False})]),
                                                        html.Label(id='Q_values',
                                                                   style={'style': 'flex'})]), ]),

                              # TEMPERATURE GRAPH

                              html.Div(className='four columns',
                                       children=[
                                           html.Div(
                                               style={'padding-left': '0%', 'padding-right': '5%'},
                                               children=[
                                                   html.H5(children='Temperature',
                                                           style={'textAlign': 'left', 'color': 'grey',
                                                                  'borderBottom': 'solid 1px grey'}),
                                                   html.Label('Temperature Range:',
                                                              style={'display': 'inline-block',
                                                                     'vertical-align': 'top'}),
                                                   dcc.RadioItems(id='Temp_range-id',
                                                                  options=[
                                                                      {'label': 'Fixed',
                                                                       'value': 'Fixed Range'},
                                                                      {'label': 'Auto',
                                                                       'value': 'Auto Range'}],
                                                                  value='Fixed Range',
                                                                  style={'display': 'inline-block',
                                                                         'padding-left': '5%'}),
                                                   # dcc.Dropdown(id='Temp_range-id2',
                                                   #              options=[
                                                   #                  {'label': 'Fixed',
                                                   #                   'value': 'Fixed Range'},
                                                   #                  {'label': 'Auto',
                                                   #                   'value': 'Auto Range'}],
                                                   #              value='Fixed Range',
                                                   #              style={'display': 'inline-block', 'padding-left': '5%',
                                                   #                     'width': '75px', 'textAlign': 'center'}),
                                                   dcc.Graph(id='T_graph',
                                                             style={'display': 'block',
                                                                    'height': '290px'},
                                                             config={'displayModeBar': False})
                                               ])]),
                          ])])])


# Advanced Popup
@app.callback(
    Output('advanced-id', 'style'),
    [Input('button', 'n_clicks')])
def advanced_popup(n_clicks):
    if n_clicks % 2 == 0:
        return {'display': 'none'}
    else:
        return {'display': 'block', 'border-style': 'dashed', 'border-width': 'thin'}


# Change to default values when Steady State is changed
@app.callback(
    [Output('AC_option', 'values'), Output('VF_option', 'values')],
    [Input('case', 'value')])
def default_AC(ss_condition):
    if ss_condition == simulation01[1]:
        return [[], []]
    else:
        return [[], []]


# Dynamic display for Cooling system (Hide AC configuration inputs depending upon steady state)
@app.callback(
    [Output('AC_option', 'style'), Output('Fake-id1', 'style'), Output('unit_size-id', 'style'),
     Output('Q_AC_max-id', 'style'), Output('P_AC_stag-id', 'style'), Output('set_point-id', 'style'),
     Output('VF_option', 'options')],
    [Input('case', 'value'), Input('VF_option', 'values')])
def AC_hide(ss_condition, VF_option):
    if ss_condition != simulation01[0]:
        return [{'display': 'none'}, {'display': 'none'}, {'display': 'none'},
                {'display': 'none'}, {'display': 'none'}, {'display': 'none'},
                [{'label': simulation_options01[simulation01.index(ss_condition) + 2],
                  'value': simulation_options01[simulation01.index(ss_condition) + 2]}]]
    elif not VF_option:
        return [{'display': 'inline-block'},
                {'margin-right': '145px', 'width': '50px', 'font-weight': 'bold', 'text-align': 'center',
                 'border': 'none'},
                {'margin-right': '97.5px', 'display': 'flex', 'justify-content': 'space-between', 'padding-top': '2%'},
                {'margin-right': '120px', 'width': '100px', 'text-align': 'center'},
                {'margin-right': '120px', 'width': '100px', 'text-align': 'center'},
                {'margin-right': '97.5px', 'display': 'flex', 'justify-content': 'space-between', 'padding-top': '2%'},
                [{'label': simulation_options01[1], 'value': simulation_options01[1]},
                 {'label': simulation_options01[2], 'value': simulation_options01[2]}]]
    else:
        return [{'display': 'block'},
                {'margin-right': '35px', 'width': '50px', 'font-weight': 'bold', 'text-align': 'center',
                 'border': 'none'},
                {'display': 'flex', 'justify-content': 'space-between', 'padding-top': '2%'},
                {'margin-right': '10px', 'width': '100px', 'text-align': 'center'},
                {'margin-right': '10px', 'width': '100px', 'text-align': 'center'},
                {'display': 'flex', 'justify-content': 'space-between', 'padding-top': '2%'},
                [{'label': simulation_options01[1], 'value': simulation_options01[1]},
                 {'label': simulation_options01[2], 'value': simulation_options01[2]}]]


# Dynamic display for Cooling system (Hide VF Configuration inputs depending upon the Steady State and Transient)
@app.callback(
    [Output('Fake-id2', 'style'), Output('Fake-id3', 'style'), Output('Q_VF_max-id', 'style'),
     Output('P_VF_stag-id', 'style'), Output('Fake-id5', 'style')],
    [Input('VF_option', 'values'), Input('case', 'value')])
def VF_hide(VF_option, ss_condition):
    if not VF_option and ss_condition == simulation01[0]:
        return [{'display': 'none'}, {'display': 'none'}, {'display': 'none'},
                {'display': 'none'}, {'display': 'none'}]
    else:
        return [
            {'margin-right': '10px', 'width': '100px', 'font-weight': 'bold', 'text-align': 'center', 'border': 'none'},
            {'margin-right': '22.5px', 'width': '75px', 'text-align': 'center', 'border': 'none'},
            {'margin-right': '10px', 'width': '100px', 'text-align': 'center'},
            {'margin-right': '10px', 'width': '100px', 'text-align': 'center'},
            {'margin-right': '22.5px', 'width': '75px', 'text-align': 'center', 'border': 'none'}]


# Set minima for the power rating of UPS (q_UPS_min = q_IT)
@app.callback(
    Output('q_UPS-id', 'min'),
    [Input('q_IT-id', 'value')])
def min_q_UPS(q_IT):
    return q_IT


# Dynamic dropdown options for IT Population
@app.callback(
    Output('n_IT-id', 'options'),
    [Input('size_rack-id', 'value'), Input('n_BP-id', 'value'), Input('size_AC-id', 'value'),
     Input('size_UPS-id', 'value')])
def IT_population_options(size_rack, blanking_panels, size_AC, size_UPS):
    return [{'label': i, 'value': i} for i in range(1, size_rack - blanking_panels - size_AC - size_UPS + 1)]


# Dynamic dropdown options for Blanking Panels
@app.callback(
    Output('n_BP-id', 'options'),
    [Input('size_rack-id', 'value'), Input('n_IT-id', 'value'), Input('size_AC-id', 'value'),
     Input('size_UPS-id', 'value')])
def Blanking_panel_options(size_rack, IT_population, size_AC, size_UPS):
    return [{'label': i, 'value': i} for i in range(0, size_rack - IT_population - size_AC - size_UPS + 1)]


# Dynamic dropdown options for AC size
@app.callback(
    Output('size_AC-id', 'options'),
    [Input('size_rack-id', 'value'), Input('n_IT-id', 'value'), Input('n_BP-id', 'value'),
     Input('size_UPS-id', 'value')])
def AC_size_options(size_rack, IT_population, blanking_panels, size_UPS):
    return [{'label': i, 'value': i} for i in
            range(1, min(11, size_rack - IT_population - blanking_panels - size_UPS + 1))]


# Dynamic dropdown options for UPS size
@app.callback(
    Output('size_UPS-id', 'options'),
    [Input('size_rack-id', 'value'), Input('n_IT-id', 'value'), Input('n_BP-id', 'value'),
     Input('size_AC-id', 'value')])
def UPS_size_options(size_rack, IT_population, blanking_panels, size_AC):
    return [{'label': i, 'value': i} for i in range(1, size_rack - IT_population - blanking_panels - size_AC + 1)]


# Error message when rack size is less than the sum of the n_IT, n_BP, n_UPS, n_AC
@app.callback(
    Output('error-id', 'style'),
    [Input('size_rack-id', 'value'), Input('n_IT-id', 'value'), Input('n_BP-id', 'value'),
     Input('size_UPS-id', 'value'), Input('size_UPS-id', 'value')])
def show_error(size_rack, IT_population, blanking_panels, size_UPS, size_AC):
    if size_rack < IT_population + blanking_panels + size_UPS + size_AC:
        return {'display': 'block', 'textAlign': 'center', 'color': 'red'}
    else:
        return {'display': 'none'}


# Rack size distribution graph
@app.callback(
    Output('rack_graph', 'figure'),
    [Input('size_rack-id', 'value'), Input('n_IT-id', 'value'), Input('n_BP-id', 'value'), Input('size_AC-id', 'value'),
     Input('size_UPS-id', 'value')])
def rack_graph_update(size_rack, IT_population, blanking_panels, size_AC, size_UPS):
    return {'data': [
        go.Bar(y=[size_rack], width=0.14, marker={'color': 'blue'}, hoverinfo='text+name', text=[size_rack],
               name='(Rack Size)', base=[0]),
        go.Bar(y=[IT_population], width=0.08, marker={'color': 'green'}, hoverinfo='text+name', text=[IT_population],
               name='(IT Population)',
               base=[size_AC + size_UPS]),
        go.Bar(y=[blanking_panels], width=0.08, marker={'color': 'orange'}, hoverinfo='text+name',
               text=[blanking_panels], name='(Blanking Panels)',
               base=[size_AC + size_UPS + IT_population]),
        go.Bar(y=[size_AC], width=0.08, marker={'color': 'purple'}, hoverinfo='text+name', text=[size_AC],
               name='(AC Unit)', base=[0]),
        go.Bar(y=[size_UPS], width=0.08, marker={'color': 'red'}, hoverinfo='text+name', text=[size_UPS],
               name='(UPS Unit)', base=[size_AC]),
    ],
        'layout': {'title': {'text': 'Rack size<Br>distribution (U)', 'x': 0, 'y': 0.96, 'font': {'size': '15'}},
                   'xaxis': {'range': [-0.25, 0.5], 'showgrid': False, 'showticklabels': False,
                             'showline': False, 'zeroline': False},
                   'yaxis': {'showgrid': False, 'showticklabels': False, 'showline': False,
                             'zeroline': False},
                   'showlegend': False,
                   # 'legend': {'x': 0, 'y': 0.7, 'orientation': 'h'},
                   'margin': {'l': '0', 'b': '15', 'r': '0', 't': '40'},
                   'barmode': 'overlay',
                   'hovermode': 'x'}
    }


# Airflow and Temperature Graphs
@app.callback(
    [Output('Q_graph', 'figure'), Output('T_graph', 'figure'),
     # Output('Q_values-id', 'children'), Output('T_values-id', 'children'),
     Output('global_ar_ss-id', 'children'), Output('global_ar_tr-id', 'children')],
    [Input('case', 'value'), Input('AC_option', 'values'), Input('VF_option', 'values'),
     Input('size_rack-id', 'value'), Input('n_IT-id', 'value'), Input('q_IT-id', 'value'),
     Input('n_BP-id', 'value'), Input('T_AC-id', 'value'), Input('T_amb-id', 'value'), Input('size_UPS-id', 'value'),
     Input('q_UPS-id', 'value'), Input('t_UPS-id', 'value'), Input('size_AC-id', 'value'),
     Input('Q_AC_max-id', 'value'), Input('Q_VF_max-id', 'value'),
     Input('P_AC_stag-id', 'value'), Input('P_VF_stag-id', 'value'),
     Input('slider-1', 'value'), Input('slider-2', 'value'),
     Input('Q_graph_layout-id', 'value'), Input('Temp_range-id', 'value')])
def update_graph(ss_condition, AC_option, VF_option, size_rack, n_IT, q_IT, n_BP, T_AC, T_amb, size_UPS, q_UPS,
                 t_max, size_AC, Q_AC_max, Q_VF_max, P_AC_stag, P_VF_stag, a_FL, a_RL, Q_graph_layout, Temp_range):
    solveFNM = Rack_solver.FNMsolver(ss_condition, AC_option, VF_option, size_rack, n_IT, q_IT, n_BP, T_AC, T_amb,
                                     size_UPS, q_UPS, t_max, size_AC, Q_AC_max, Q_VF_max, P_AC_stag, P_VF_stag,
                                     a_FL, a_RL)

    Q_ss, P, gr_ss = solveFNM.calcAirflow_ss()
    Q_tr, P, gr_tr = solveFNM.calcAirflow_tr()

    if Q_graph_layout == 2:
        Q = Q_tr
    else:
        Q = Q_ss

    Q = Q / 0.0004719474
    Q_net = np.round(Q[0] - Q[1] + Q[2], 2)
    Q = np.round_(Q, 2)

    Q1 = np.round_(Q * 0.0004719474, 4)

    T_IT_inlet, T_rec, t = solveFNM.calcTemp()
    T_IT_inlet = np.round_(T_IT_inlet, 2)

    if Temp_range == 'Fixed Range':
        T_range = [50, 160]

    else:
        T_range = []

    return [
        {'data': [
            go.Bar(x=[0, -(Q[3] - Q[5])], y=y_axis, orientation='h', width=0.3, marker={'color': 'purple'},
                   hoverinfo='text',
                   text=[0, round(abs(Q[3] - Q[5]), 2)], name='Rear Leakage', base=[0, -6*np.sign(Q[3]-Q[5])]),
            go.Bar(x=[0, Q[3] - Q[4]], y=y_axis, orientation='h', width=0.3, marker={'color': 'darkorange'},
                   hoverinfo='text',
                   text=[0, round(abs(Q[3] - Q[4]), 2)], name='Front Leakage', base=[0, 6*np.sign(Q[3]-Q[4]) + max(Q[3]-Q[5],0)*min(Q[3]-Q[4],0)/abs(Q[3]-Q[4]) - min(Q[3]-Q[5],0)*max(Q[3]-Q[4],0)/abs(Q[3]-Q[4])]),
            go.Bar(x=[0, -Q[5]], y=y_axis, orientation='h', width=0.3, marker={'color': 'mediumslateblue'},
                   hoverinfo='text',
                   text=[0, abs(Q[5])], name='Rear Vent Fan Airflow',
                   base=[0, -6*np.sign(Q[5]) + (-max(Q[3]-Q[5],0) + min(Q[3]-Q[4],0))*max(Q[5],0)/abs(Q[5]) + (min(Q[3]-Q[5],0) - max(Q[3]-Q[4],0))*min(Q[5],0)/abs(Q[5])]),
            go.Bar(x=[0, Q[4]], y=y_axis, orientation='h', width=0.3, marker={'color': 'red'},
                   hoverinfo='text', text=[0, abs(Q[4])], name='Front Vent Fan Airflow',
                   base=[0, 6*np.sign(Q[4]) + (max(Q[3]-Q[5],0) - min(Q[3]-Q[4],0) + max(Q[5],0))*min(Q[4],0)/abs(Q[4]) + (-min(Q[3]-Q[5],0) + max(Q[3]-Q[4],0) - min(Q[5],0))*max(Q[4],0)/abs(Q[4])]),

            go.Bar(x=[0], y=y_axis, marker={'color': 'white'}, name='- - - - - - - - - -'),

            go.Bar(x=[8], y=y_axis, orientation='h', width=0.6, marker={'color': 'black'}, hoverinfo='text',
                   showlegend=False, text=[abs(Q_net)], name='Net Positive Airflow',
                   base=[(2 + Q_net) * np.sign(Q_net)]),
            go.Bar(x=[Q[0]], y=y_axis, orientation='h', width=0.3, marker={'color': 'blue'}, hoverinfo='text',
                   text=[abs(Q[0])], name='IT Airflow', base=[6]),
            go.Bar(x=[-Q[1]], y=y_axis, orientation='h', width=0.3, marker={'color': 'green'}, hoverinfo='text',
                   text=[abs(Q[1])], name='AC Airflow',
                   base=[-6 * np.sign(Q[1]) - Q[0] * min(Q[1], 0) / abs(Q[1])]),
            go.Bar(x=[Q[2]], y=y_axis, orientation='h', width=0.3, marker={'color': 'darkgrey'}, hoverinfo='text',
                   text=[abs(Q[2])], name='Server Plane Leakage',
                   base=[6 * np.sign(Q[2]) + (
                           (Q[0] - min(Q[1], 0)) * max(Q[2], 0) / abs(Q[2]) + (max(Q[1], 0) * min(Q[2], 0)) / abs(
                       Q[2]))]),
        ],
            'layout': {'xaxis': {'title': 'Airflow rates (cfm)', 'showgrid': True},
                       'margin': {'l': '55', 'b': '40', 'r': '0', 't': '0'}, 'barmode': 'overlay',
                       'hovermode': 'closest'}},
        {'data': [
            go.Scatter(x=t, y=T_IT_inlet, marker={'color': 'red'}, mode='lines', name='IT Inlet Temperature'),
            go.Scatter(x=t, y=T_rec, marker={'color': 'green'}, mode='lines', name='ASHRAE Recommended')],
            'layout': {'xaxis': {'title': 'Time After Power Failure (s)'},
                       'yaxis': {'title': 'Temperature (\u00B0F)', 'range': T_range, 'nticks': 6},
                       'legend': {'x': 0.5, 'y': 1.2}, 'margin': {'l': '50', 'b': '40', 'r': '20', 't': '0'}}},

        # ['Q_IT= ', Q1[0], ', Q_AC= ', Q1[1], ', Q_SP= ', Q1[2], ', Q_L_total= ', round(Q1[3], 2), ', Q_VF_f= ', Q1[4],
        #  ', Q_VF_r=', Q1[5]],
        # ['T_IT= ', T[0], ', T_F= ', T[1], ', T_IT_out= ', T[2], ', T_AC= ', T[3], ', T_R= ', T[4], ', T_AC_out= ', T[5]],

        f'{gr_ss:.2f}',
        f'{gr_tr:.2f}'
    ]


if __name__ == '__main__':
    port = 8071
    if 'PORT' in os.environ:
        port = os.environ['PORT']

    app.run_server(debug=True, host='0.0.0.0', port=port)
