import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from app import app

# Importing each fresh market page
from bronisze import bronisze_layout
from elizowka import elizowka_layout
from zjazdowa import zjazdowa_layout


# ------------------------------------------------------------------------------
# Tabs for app
app_tabs = html.Div(
    [
        dbc.Tabs(
            [
                dbc.Tab(label="Bronisze", tab_id="tab-bronisze", labelClassName="font-weight-bold label_styling",
                 activeLabelClassName="text-danger"),
                dbc.Tab(label="Elizowka", tab_id="tab-elizowka", labelClassName="font-weight-bold label_styling",
                 activeLabelClassName="text-danger"),
                dbc.Tab(label="Zjazdowa", tab_id="tab-zjazdowa", labelClassName="font-weight-bold label_styling",
                 activeLabelClassName="text-danger"),
            ],
            id="tabs",
            active_tab="tab-bronisze",
        ),
    ], className="mt-3"
)

# ------------------------------------------------------------------------------
# General layout
app.layout = dbc.Container([
    dbc.Row(dbc.Col(html.H1("Fresh Markets Analytics Dashboard",
                            style={"textAlign": "center",'color':"white",
                            'backgroundColor': 'rgba(0, 0, 0, 0.7)','paddingBottom':"20px"}), width=12)),
    html.Hr(),
    dbc.Row(dbc.Col(app_tabs, width=12), className="mb-3"),
    html.Div(id='content', children=[])

])



# ------------------------------------------------------------------------------
# CALLBACKS
# allowing users to switch between tabs
@app.callback(
    Output("content", "children"),
    [Input("tabs", "active_tab")]
)
def switch_tab(tab_chosen):
    if tab_chosen == "tab-bronisze":
        return bronisze_layout
    elif tab_chosen == "tab-elizowka":
        return elizowka_layout
    elif tab_chosen == "tab-zjazdowa":
        return zjazdowa_layout
   

# ------------------------------------------------------------------------------
# TO RUN THE APP
if __name__ == '__main__':
    app.run_server(debug=True)
