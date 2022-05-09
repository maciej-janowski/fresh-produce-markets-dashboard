import pandas as pd

import plotly.express as px 


import datetime

import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from app import app


zjazdowa = pd.read_csv('csv_database\ceny_zjazdowa.csv',parse_dates=[5])


# getting the different between today and latest updated
todey = datetime.date.today()
zjazdowa['date_diff'] = zjazdowa['date'].apply(lambda x:(todey - x.date()).days)

# getting the date in str for latest update
latest = zjazdowa['date_diff'].min()
latest_day = (todey - datetime.timedelta(days=int(latest))).strftime("%d-%m-%Y")

# getting dataframe with latest update
new_zjazdowa = zjazdowa[zjazdowa["date_diff"]==latest]

# getting cheapest product
cheapest_product = new_zjazdowa[new_zjazdowa['lowest_price']==new_zjazdowa['lowest_price'].min()].iloc[0]

cheap_product = cheapest_product['product']
cheap_measure = cheapest_product['quantity']
cheap_price = cheapest_product['lowest_price']


# getting most expensive product
expensive_product = new_zjazdowa[new_zjazdowa['highest_price']==new_zjazdowa['highest_price'].max()].iloc[0]
exp_product = expensive_product['product']
exp_measure = expensive_product['quantity']
exp_price = float(expensive_product['highest_price'])

combination = new_zjazdowa[['product','quantity']]

# getting products for dropdown

products =  [{'label':f'{x} {y}','value':x} for x,y in zip(zjazdowa['product'],zjazdowa['quantity'])]

products_for_cart  = [{'label':f'{x} {y}','value':x} for x,y in zip(combination['product'],combination['quantity'])]

# getting quantities for dropdown
quantites  = [{'label':x,'value':x }for x in list(range(20))]

# building layout
zjazdowa_layout = html.Div([
            html.H1(f'Prices in Zjazdowa fresh market (as of {latest_day})',
                    className='data-info-header'),

                    html.Div(className='score-cards',children=[
                        dbc.Card([
                            dbc.CardBody([
                                html.H6('Cheapest product in the market'),
                                html.H4(f'{cheap_product} {cheap_measure}'),
                                html.H2(id='poor', children=[f'{cheap_price} zł'])
                            ],style={'textAlign':'center'})
                            ],color="success", className='mx-4', inverse=True),
                        dbc.Card([
                            dbc.CardBody([
                                html.H6('Most expensive product in the market'),
                                html.H4(f'{exp_product} {exp_measure}'),
                                html.H2(id='expensive', children=[f'{exp_price} zł'])
                            ],style={'textAlign':'center'})
                            ],color="danger", className='mx-4', inverse=True),
                    ]), 
                      html.Div(className='graph_for_prices',children=[
                html.Br(),
                html.H1(f'Select products to see prices over time',
                    className='data-info-header'),
                dcc.Dropdown(id="dropdown_products",
                                options=products,
                                multi=True,
                                value=[],
                                placeholder="Select products...",
                                style={'width': "100%",'margin':'15px auto 15px'}
                                ),
                html.Div(id='graph_output_zjazdowa')
            ]),
            html.Br(),
            html.H3(className='shopping-cart-header',children=['Create your shopping cart by selecting products and quantities']),
            html.H4(className='shopping-cart-header',children=f'Cart will be calculated based on the latest data available ({latest_day})'),
            html.Div(className='shopping-list-zjazdowa',children=[
                
                dash_table.DataTable(
                    id='table_zjazdowa',
                    columns=[{'name': 'Product', 'id': 'Product', 'deletable': False, 'renamable': False},
                                {'name': 'Quantity', 'id': 'Quantity', 'deletable': False, 'renamable': False}],
                    data=[],
                    editable=False,                  # allows to edit data inside table
                    row_deletable=True,             # allows to delete rows
        
        
                ),
                html.Div(id='recipt',style={'marginTop':'20px'}),
                html.Div(id='dropdowns-zjazdowa',children=[
                                    dcc.Dropdown(id="dropdown_products_cart_zjazdowa",
                                                    options=products_for_cart,
                                                    multi=False,
                                                    # value=[],
                                                    placeholder="Select products...",
                                                    style={'width': "100%",'margin':'15px auto 15px'}
                                    ),
                                    dcc.Dropdown(id="quantity_products_cart_zjazdowa",
                                                    options=quantites,
                                                    multi=False,
                                                    # value=0,
                                                    placeholder="Select quantity...",
                                                    style={'width': "100%",'margin':'15px auto 15px'}
                                    ),
                ]),
                dbc.Button("Add product to cart", id='adding_zjazdowa', color="primary", className="mr-1",style={'marginBottom':'10px'},n_clicks=0),
                dbc.Button("Calculate cart", id='calculate_cart', color="success", className="mr-1",style={'marginBottom':'10px'},n_clicks=0),



            ]),


        ])


# ------------------------------------------
# CALLBACKS

# adding products to table
@app.callback(
    Output(component_id="table_zjazdowa", component_property="data"),
    Input(component_id="adding_zjazdowa", component_property="n_clicks"),
    [State(component_id="dropdown_products_cart_zjazdowa", component_property="value"),
    State(component_id="quantity_products_cart_zjazdowa", component_property="value"),
    State(component_id='table_zjazdowa',component_property='data'),
    State(component_id='table_zjazdowa',component_property='columns')]
)
def add_new_row(clicks, product,quantity,table,columns):

    if clicks >0:

        table.append({"Product":product,"Quantity":quantity})
        return table
    else:
        return table

# generating graph
@app.callback(
    Output(component_id="graph_output_zjazdowa", component_property="children"),
    Input(component_id="dropdown_products", component_property="value"),

)
def display_value(selected):

    filtered_data = zjazdowa[zjazdowa['product'].isin(selected)]

    line_contracted = px.line( 
            title="Prices of goods over time",
            data_frame=filtered_data,
            x='date',
            y='lowest_price',
            color='product',
            labels={'product':'product', 'date':'date','quantity':"quantity"},
            
            )
    line_contracted.update_traces(mode='markers+lines')


    figure = dcc.Graph(id='line_products',config={
                                'toImageButtonOptions':
                                    {
                                    'format': 'jpeg', 
                                    'filename': 'products graph',
                                    'height': 500,
                                    'width': 1200,
                                    'scale': 2 
                                    }
                                
                            },figure=line_contracted)


    return figure

# calculating price of the cart (based on products selected)
@app.callback(
    Output(component_id="recipt", component_property="children"),
    Input(component_id="calculate_cart", component_property="n_clicks"),
    State(component_id='table_zjazdowa',component_property='data')
)
def calculate_cart(button,data):

    if button >0:
        price = 0
        for item in data:
            price += new_zjazdowa[new_zjazdowa['product']==item['Product']]['lowest_price'].to_list()[0] * item['Quantity']
        return dbc.Card([
                    dbc.CardBody([
                        html.H4('Price for cart'),
                        html.H2(id='cart_pricing', children=[f'{price} zł'])
                    ],style={'textAlign':'center'})
                ],color="success", className='mx-4', inverse=True)