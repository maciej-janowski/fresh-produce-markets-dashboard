import dash
import dash_bootstrap_components as dbc


# initiating our Dash app (separate file)
# as stylesheets we use additional two which give us font awesome and bootstrap capabilities
app = dash.Dash(__name__,external_stylesheets=['https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css',
"https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"],
meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}],suppress_callback_exceptions=True)