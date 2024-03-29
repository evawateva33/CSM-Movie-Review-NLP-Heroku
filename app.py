import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
# !pip install dash_building_blocks
import dash_core_components as dcc
import dash_html_components as html
import dash_building_blocks as dbb
import plotly.express as px
import base64
import pickle
import pandas as pd  #Pandas for data pre-processing
import joblib

import flask
import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import os
import psycopg2
import datetime

import dash_table

from flask import Flask
import logging
image_filename = 'Screen Shot 2021-06-04 at 11.36.51 AM.png' # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())



DATABASE_URL = os.environ['DATABASE_URL']

colors = {
    'background': '#339933',
    'text': '#111111'
}

con = psycopg2.connect(DATABASE_URL)

#  create a new cursor
cur = con.cursor()
# query the entire csv from postgres database
query = f"""SELECT *
            FROM tweet_dbs
            """
# return results as a dataframe
ex3 = pd.read_sql(query, con)
ex3 = ex3.to_dict()
#convert to df
ex3 = pd.DataFrame.from_dict(ex3)


ex3['text'] = ex3['count_racist'].astype(str)
ex3['datetime'] =  pd.to_datetime(ex3['datetime'].str[:18], errors = 'coerce',  format='%Y-%m-%d %H:%M:%S')
ex3['count_yellowface'] = ex3['text'].str.count('yellowface')
ex3['count_blackface'] = ex3['text'].str.count('blackface')
ex3['count_bias'] = ex3['text'].str.count('bias')
ex3['count_anti-Semitic'] = ex3['text'].str.count('anti-Semitic')
ex3['count_discrimination'] = ex3['text'].str.count('discrimination')
ex3['count_bigot'] = ex3['text'].str.count('bigot')
ex3['count_offensive'] = ex3['text'].str.count('offensive')
ex3['count_stereotypes'] = ex3['text'].str.count('stereotype')
ex3['count_caricature'] = ex3['text'].str.count('caricature')
ex3['count_racist'] = ex3['text'].str.count('racist')
ex3['count_sexist'] = ex3['text'].str.count('sexist')
ex3['count_stigma'] = ex3['text'].str.count('stigma')
ex3['count_stereotypes'] = ex3['text'].str.count('stereotype')
ex3['count_problematic'] = ex3['text'].str.count('problematic')
ex3 = ex3.dropna()
ex3 = ex3.reset_index()
fig_names = ex3.movie.unique()
ex1 = pd.DataFrame(ex3.groupby(['movie'], sort=True)['count_racist',
                                                'count_sexist',
                                                'count_problematic',
                                             'count_stigma',
                                             'count_yellowface' ,
                                            'count_blackface',
                                            'count_stereotypes',
                                              'count_discrimination',
                                              'count_caricature',
                                              'count_offensive',
                                              'count_bigot',
                                              'count_bias',
                                            ].sum())

ex1 = ex1.reset_index()
ex3['text'] = ex3['text'].astype(str)
ex3['text'] = ex3['text'].str.wrap(30)
ex3['text'] = ex3['text'].apply(lambda x: x.replace('\n', '<br>'))

class Graph(dbb.Block):
    def layout(self):
        return html.Div([
         html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()), style={'height':'20%', 'width':'20%', 'position': 'relative',
                                                                                           'text-align': 'right'}),
    html.Div(style={'backgroundColor': colors['background']},
        className="app-header",
        children=[
            html.H1('Welcome to the Common Sennse Media Twitter Review Tool',
             className="app-header--title",   style={
            'textAlign': 'center',
            'color': '#FFFFFF'
        }),
        html.H5('IF GRAPHS BELOW DO NOT LOAD: PRESS "COMMAND+SHIFT+R", THEN Refresh the Page, THEN wait 10-20 Seconds, REPEAT if needed',
         className="app-header--title",   style={
        'textAlign': 'center',
        'color':  '#FFFFFF'
    })
        ]
    ), html.Div(
        children=html.Div([
            html.H3('How To Use This Tool:',   style={
            'color': '#808080'
        }),
            html.H4('''
                First: Click the Dropdown Menus Below and Choose a Movie to Search Twitter Press TAB to Submit Movie Choice''',   style={

            'color': '#808080'
        }),
        html.H4('''
            Second [OPTIONAL]: Input a unique word you wish to search for that was mentioned in tweets PRESS TAB to Submit''',   style={

        'color': '#808080'
    }),
    html.H4('''
        Third: Click the Second Dropdown Menu and Choose a Word that You Wish to Search for PRESS TAB to Submit''',   style={

    'color': '#808080'
}),
        ])
    ),

    dcc.Dropdown(
                id=self.register('dropdown'),
                options=self.data.options,
                value="Breakfast at Tiffany's",
                placeholder='Select specific movie to search'
            ),


        dcc.Input(id=self.register("input1"),value = 'bad',  type="text", placeholder="Input word to search",),
        #dcc.Input(id=self.register("input2"), type="text", placeholder="", debounce=True),

     dcc.Dropdown( id =self.register('dropdown2'),
        options = [
            {'label':'count_racist', 'value':'count_racist' },
            {'label': 'count_sexist', 'value':'count_sexist'},
            {'label': 'count_problematic', 'value':'count_problematic'},
            {'label': 'count_whitewashing', 'value':'count_whitewashing'},
            {'label': 'count_stigma', 'value':'count_stigma'},
            {'label': 'count_stereotypes', 'value':'count_stereotypes'},
            {'label': 'count_yellowface', 'value':'count_yellowface'},
            {'label': 'count_blackface', 'value':'count_blackface'},
            {'label': 'count_bias', 'value':'count_bias'},
            {'label': 'count_bigot', 'value':'count_bigot'},
            {'label': 'count_discrimination', 'value':'count_discrimination'},
            # {'label': 'count_anti_Semitic', 'value':'count_anti_Semitic'},
            {'label': 'count_offensive', 'value':'count_offensive'},
            {'label': 'count_caricature', 'value':'count_caricature'},



            ],
        value = 'count_racist', placeholder="Select a word to see frequency of mentions"),
      dash_table.DataTable(
                id=self.register('table'),
                  style_cell_conditional=[
        {'if': {'column_id': 'title'},
         'width': '200px'},
        {'if': {'column_id': 'post'},
         'width': '670px'
         ,'height':'auto'}
    ]
    ,style_cell={
        'overflow': 'hidden',
        'textOverflow': 'ellipsis',
        'maxWidth': '50px'
    }
    , style_table={
        'maxHeight': '300px'
        ,'overflowY': 'scroll'
    },
    style_data_conditional=[
        {
            'if': {
                'column_id': 'count_racist',
                'filter_query': '{count_racist} gt 10'
            },
            'backgroundColor': '#B20000',
            'color': 'white',
        }
        ,{
            'if': {
                'column_id': 'count_problematic',
                'filter_query': '{count_problematic} gt 10'
            },
            'backgroundColor': '#B20000',
            'color': 'white',
        }
        ,{
            'if': {
                'column_id': 'count_sexist',
                'filter_query': '{count_sexist} gt 10'
},
            'backgroundColor': '#B20000',
            'color': 'white',
        }
        ,{
            'if': {
                'column_id': 'count_stigma',
                'filter_query': '{count_stigma} gt 10'
},
            'backgroundColor': '#B20000',
            'color': 'white',
        }
        ,
       {
            'if': {
                'column_id': 'count_discrimination',
                'filter_query': '{count_discrimination} gt 10'
},
            'backgroundColor': '#B20000',
            'color': 'white',
        },
       {
            'if': {
                'column_id': 'count_yellowface',
                'filter_query': '{count_yellowface} gt 10'
},
            'backgroundColor': '#B20000',
            'color': 'white',
        },
       {
            'if': {
                'column_id': 'count_blackface',
                'filter_query': '{count_blackface} gt 10'
},
            'backgroundColor': '#B20000',
            'color': 'white',
        },
         {
              'if': {
                  'column_id': 'count_caricature',
                  'filter_query': '{count_caricature} gt 10'
  },
              'backgroundColor': '#B20000',
              'color': 'white',
          },
           {
                'if': {
                    'column_id': 'count_bias',
                    'filter_query': '{count_bias} gt 10'
    },
                'backgroundColor': '#B20000',
                'color': 'white',
            },
            {
                 'if': {
                     'column_id': 'count_bigot',
                     'filter_query': '{count_bigot} gt 10'
     },
                 'backgroundColor': '#B20000',
                 'color': 'white',
             },
                 {
                      'if': {
                          'column_id': 'count_offensive',
                          'filter_query': '{count_offensive} gt 10'
          },
                      'backgroundColor': '#B20000',
                      'color': 'white',
                  },
           #        {
           #             'if': {
           #                 'column_id': 'count_anti_Semitic',
           #                 'filter_query': '{count_anti_Semitic} gt 10'
           # },
           #             'backgroundColor': '#B20000',
           #             'color': 'white',
           #         },
                     {
                          'if': {
                              'column_id': 'count_stereotypes',
                              'filter_query': '{count_stereotypes} gt 10'
              },
                          'backgroundColor': '#B20000',
                          'color': 'white',
                      }


    ],
                columns= [{"name": i, "id": i} for i in ex1.columns],
                data=ex1.to_dict("records"),
                                    ),

        dcc.Graph(id=self.register('graph2')),
        dcc.Graph(id=self.register('graph')),
        dcc.Graph(id=self.register('graph3'))

        ], style={'width': '500'})

    def callbacks(self):
        @self.app.callback(
            self.output('table', 'data'),
            self.output('graph', 'figure'),
            self.output('graph2', 'figure'),
            self.output('graph3', 'figure'),
            [self.input("input1", "value")],

            [self.input('dropdown', 'value')],
     [self.input(component_id='dropdown2', component_property= 'value')]
        )
        def update_graph(input1, selected_dropdown_value , selected_dropdown_value2):
            stringy2 = str(selected_dropdown_value2)
            stringy1 = str(selected_dropdown_value)
            inputy = str(input1)
            ex3['count '+'{}'.format(inputy)] = ex3['text'].str.count(inputy)
            ex33 = ex3[ex3['movie'] == str(selected_dropdown_value)]

            dif0= px.scatter(ex3, x='datetime', y = ex3['{}'.format(stringy2)],
                            color='movie', title = '<b>All Movie Tweets Mentions with a ' +'{}'.format(stringy2) )
            figgs = px.line(ex33, x='datetime',y = ex33['count '+'{}'.format(inputy)],
                        hover_data=["text"],color='score',
                        title= "<b>"+'{}'.format(stringy1)+ " Movie Tweet Mentions with a "+'count '+'{}'.format(inputy))
            figgz = px.line(ex33, x='datetime', y = ex33['{}'.format(stringy2)],
                        hover_data=["text"] , color = 'score',
                        title= "<b>"+'{}'.format(stringy1)+ " Movie Tweet Mentions with a "+'{}'.format(stringy2))
            dif0.update_layout(
                title={
                    'y':0.9,
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'})
            figgs.update_layout(
                title={
                    'y':0.9,
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'})
            figgz.update_layout(
                title={
                    'y':0.9,
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'})
            return   ex1.to_dict("records"), figgz, dif0, figgs

# app = dash.Dash(__name__, suppress_callback_exceptions=True)



from flask import Flask
import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server)
server = app.server
#fig_names = ex3.movie.unique()
options=[{'label': x, 'value': x} for x in fig_names]
data = {
    'options': options,
    'value': None
}
n_graphs =1
graphs = [Graph(app, data) for _ in range(n_graphs)]

app.layout = html.Div(children=
    [html.Div(graph.layout, className='six columns')
    for graph in graphs],
    className='container'
)

app.config.suppress_callback_exceptions = True

for graph in graphs:
    graph.callbacks()

if __name__ == '__main__':
    app.run_server(debug=True,dev_tools_ui=True,dev_tools_props_check=False)
