import os
import pandas as pd
import cufflinks as cf
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import plotly.graph_objects as go

px.set_mapbox_access_token(os.environ.get('TOKEN'))
dff = pd.read_excel('data/dff.xlsx')
dff.drop(columns=['Unnamed: 0', 'Area Code', 'Item Code', 'Element Code'],
         inplace=True)
dff.drop_duplicates(subset=['Y2014', 'Y2015', 'Y2016', 'Y2017', 'Y2018'],
                    inplace=True)
area = dff[dff['Element'] == 'Area harvested']
yield1 = dff[dff['Element'] == 'Yield']
prod = dff[dff['Element'] == 'Production']
world = pd.read_excel('data/world.xlsx')
drop = ['Unnamed: 0', 'Area Code', 'Area', 'Item Code', 'Element Code',
        'Y1961', 'Y1962', 'Y1963', 'Y1964', 'Y1965', 'Y1966', 'Y1967',
        'Y1968', 'Y1969', 'Y1970', 'Y1971', 'Y1972', 'Y1973', 'Y1974',
        'Y1975', 'Y1976', 'Y1977', 'Y1978', 'Y1979', 'Y1980', 'Y1981',
        'Y1982', 'Y1983', 'Y1984', 'Y1985', 'Y1986', 'Y1987', 'Y1988',
        'Y1989', 'Y1990', 'Y1991', 'Y1992', 'Y1993', 'Y1994', 'Y1995',
        'Y1996', 'Y1997', 'Y1998', 'Y1999', 'Y2000', 'Y2001', 'Y2002',
        'Y2003', 'Y2004', 'Y2005', 'Y2006', 'Y2007', 'Y2008', 'Y2009',
        'Y2010', 'Y2011', 'Y2012', 'Y2013']


def confirm_option_value(value, dataframe):
    if value == 'area':
        return dataframe[dataframe['Element'] == 'Area harvested']
    elif value == 'yield':
        y = dataframe[dataframe['Element'] == 'Yield']
        y['Total'] = y['Total'] / 10000
        return y
    elif value == 'production':
        return dataframe[dataframe['Element'] == 'Production']


def world_clean(value, drop=drop):
    world1 = world.drop(drop, axis=1)
    total = world1.sum(axis=1)
    world1['Total'] = total
    return confirm_option_value(value, world1)


ar = world_clean('area', drop=drop)
pdd = world_clean('production', drop=drop)
yy = world_clean('yield', drop=drop)


def country_info(country, item=None):
    '''Function for producing country information
    '''
    # Selecting specific country
    som = dff[dff['Area'] == country]
    lat = som['Lat']
    lon = som["Lon"]
    somm = som.drop(['Lat', 'Lon'], axis=1)
    # Summing up the totals
    total = somm.sum(axis=1)
    somm['Total'] = total
    somm['Lat'] = lat
    somm['Lon'] = lon
    # ruling out specific item
    itm = somm[somm['Item'] == item]
    years = ['Y2014', 'Y2015', 'Y2016', 'Y2017', 'Y2018']
    new_df = itm.groupby('Element')[years].sum().transpose()
    new_df['Years'] = years
    new_df['Yield'] = new_df['Yield'] / 10000
    return new_df


def total_element(value, item=None):
    '''Function for producing crop information
    '''
    # Selecting specific item
    lot = dff[dff['Item'] == item]
    lat = lot['Lat']
    lon = lot["Lon"]
    ittem = lot.drop(['Lat', 'Lon'], axis=1)
    # Summing up the totals
    total = ittem.sum(axis=1)
    ittem['Total'] = total
    ittem['Lat'] = lat
    ittem['Lon'] = lon
    # Filtering elements
    return confirm_option_value(value, ittem)

    
data = pd.read_csv('data/cane.csv')
colors = ['#ECC61D','#914F9A','#4386AE','#6E2E63','#17161A']
fig = go.Figure()

fig.add_trace(go.Indicator(
    mode = "number+delta",
    value = ar[ar['Item'] == 'Sugar cane'].Y2018.sum(),
    title = {
        "text": "Area Harvested<br><span style='font-size\
                :0.8em;color:gray'>in</span><br><span style='font-size\
                :0.8em;color:gray'>Hectares</span>"
    },
    delta = {
        'reference': ar[ar['Item'] == 'Sugar cane'].Y2017.sum(),\
            'relative': True
    },
    domain = {'x': [0, 0.5], 'y': [0.5, 0]}))

fig.add_trace(go.Indicator(
    mode = "number+delta",
    value = pdd[pdd['Item'] == 'Sugar cane'].Y2018.sum(),
    title = {
        "text": "Production<br><span style='font-size:0.8em;\
                color:gray'>in</span><br><span style='font-size\
                :0.8em;color:gray'>Tonnes</span>"
    },
    delta = {
        'reference': pdd[pdd['Item'] == 'Sugar cane'].Y2017.sum(),\
            'relative': True
    },
    domain = {'x': [0.5, 1], 'y': [0, 1]}))

fig.add_trace(go.Indicator(
    mode = "number+delta",
    value = yy[yy['Item'] == 'Sugar cane'].Y2018.sum() / 10000,
    title = {
        "text": "Yield<br><span style='font-size:0.8em\
                ;color:gray'>in</span><br><span style='font-size:0.8em\
                ;color:gray'>Tonne per Hectare</span>"
    },
    delta = {
        'reference': yy[yy['Item'] == 'Sugar cane'].Y2017.sum()/10000,\
            'relative': True
    },
    domain = {'x': [0.5, 0], 'y': [1, 0.5]}))


def bar_graph(x=None, y=None, xTitle=None, yTitle=None, title=None, how=None,
              colors=None):
    df = country_info('Somalia', item='Sugar cane')
    fig = df.iplot(asFigure=True, kind='bar', x=x, y=y, yTitle=yTitle,
                   xTitle=xTitle, theme='polar', subplots=True,
                   subplot_titles=True, title=title, colors=colors,
                   orientation=how)
    return fig


def line_graph(x=None, y=None, xTitle=None, yTitle=None, title=None, mode=None,
               colors=None, scale=None, how=None):
    df = country_info('Somalia', item='Sugar cane')
    fig = df.iplot(asFigure=True, kind='scatter', mode=mode, x=x, y=y, xTitle=xTitle,
                   yTitle=yTitle, subplots=True, subplot_titles=True, theme='polar',
                   interpolation=how, title=title, colorscale=scale)
    return fig


fig1 = bar_graph(x='Years', y='Area harvested', xTitle='Area harvested', yTitle='Years',
                 title='Area Harvested (Hectares)', how='h', colors='#4386AE')

fig2 = line_graph(x='Years', y='Production', xTitle='Years', yTitle='Tonnes',
                  colors='#914F9A',how='spline', mode='lines',
                  title='Sugar cane Production in Somalia from 2014 - 2018')

fig3 = px.scatter_mapbox(total_element('production', 'Sugar cane'), lat='Lat',
                         lon='Lon', color='Total', hover_name='Area', size = 'Total',
                         hover_data={'Lat':False, 'Lon':False}, labels = {'Area':'Element'},
                         color_continuous_scale=colors, zoom=1.4, width=1900, height=700,
                         template='presentation', center=None, mapbox_style='light',
                         title='Global Sugar cane Production in Tonnes(2014-2018)')

fig4 = data[data['Element'] == 'Production'].iplot(asFigure=True, kind='pie',
                                                   labels='Area', values='Y2018',
                                                   legend=False,textinfo='label+percent',
                                                   theme='polar', hole=.6, linecolor='white',
                                                   colors=colors, linewidth=.5,
                                                   title='Sugar cane Production in Africa as at 2018')

fig5 = line_graph(x='Years', y='Yield', xTitle='Years', yTitle='Tonne per hectare',
                  title='Sugar cane Yield for Somalia (2014 - 2018)', mode='lines+markers',
                  scale='puor', how='spline')

layout = html.Div([
    dbc.Container([
        dbc.Row([
                dbc.Col(html.H1('World Sugar Cane Statistics as at 2018', className='text-center'), className='mb-4 mt-5')
            ]),
        dbc.Row(
            dbc.Col(html.Div([
                    dcc.Graph(id = 'Chart30',
                            figure = fig,
                            animate = True,
                            responsive = True,
                            config = {
                                'showTips': True,
                                'displaylogo': False
                            })], style = {'font-variant':'small-caps','font-weight':'bold'}), width = 12, align='center')
        )
    ], fluid=True),
        dbc.Row(
            dbc.Col(html.Div([
                    dcc.Graph(id = 'Chart31',
                            figure = fig3,
                            responsive = 'auto',
                            animate = True,
                            config = {
                                'showTips':True,
                                'displaylogo':False,
                                'scrollZoom':False
                            })], style = {'font-variant':'small-caps','font-weight':'bold'}),width=12), style={'font-variant':'small-caps','font-weight':'bold'}),
        dbc.Row([
            dbc.Col(html.Div([
                        dcc.Graph(id = 'Chart32',
                                figure = fig2,
                                responsive = True,
                                animate = True,
                                config = {
                                    'showTips':True,
                                    'displaylogo':False
                                })
            ], style = {'font-variant':'small-caps','font-weight':'bold'}), width=6, align='center'),
            dbc.Col(html.Div([
                        dcc.Graph(id = 'Chart33',
                                figure = fig4,
                                responsive = True,
                                animate = True,
                                config = {
                                    'showTips': True,
                                    'displaylogo': False
                                })
            ], style = {'font-variant':'small-caps','font-weight':'bold'}), width=6, align = 'center'),
        ], className='row'),
        html.Hr(),

        dbc.Row([
            dbc.Col(html.Div([
                        dcc.Graph(id = 'Chart34',
                                figure = fig1,
                                responsive = True,
                                animate = True,
                                config = {
                                    'showTips':False,
                                    'displaylogo':False
                                })
            ], style = {'font-variant':'small-caps','font-weight':'bold'}), width=6),
            dbc.Col(html.Div([
                        dcc.Graph(id = 'Chart35',
                                figure = fig5,
                                responsive = True,
                                animate = True,
                                config = {
                                    'showTips':True,
                                    'displaylogo': False
                                })
            ], style = {'font-variant':'small-caps','font-weight':'bold'}), width=6),
        ], className='row')


])