import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State

from components import (content, sidebar)
from layout import background_page

FA = "https://use.fontawesome.com/releases/v5.12.1/css/all.css"
FG = "https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500&display=swap"
FC = "assets/sidebar.css"

# Dash app
app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.BOOTSTRAP, FA, FG, FC],
                external_scripts=['https://code.jquery.com/jquery-3.3.1.min.js',
                                  "https://platform.twitter.com/widgets.js"],
                meta_tags=[
                    {"name": "viewport", "content": "width=device-width, initial-scale=1"}
                ])

# Server
server = app.server
app.config.suppress_callback_exceptions = True
app.title = 'Moonpass App'

app.layout = html.Div(style={'backgroundColor': background_page}, children=[dcc.Location(id="url"), sidebar, content])


@app.callback(
    Output("sidebar", "className"),
    [Input("sidebar-toggle", "n_clicks")],
    [State("sidebar", "className")],
)
def toggle_class_name(n, class_name):
    if n and class_name == "":
        # , {"paddingLeft": "80px", 'transition': 'margin 0.3s ease-in-out, padding 0.3s ease-in-out'}
        return "collapsed"
    # , {"paddingLeft": "20rem", 'transition': 'margin 0.3s ease-in-out, padding 0.3s ease-in-out'}
    return ""


@app.callback(
    Output("collapse", "is_open"),
    [Input("navbar-toggle", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


def did_component_trigger_callback(component_name: str, component_property: str):
    """
    Uses dash utils to check whether a component triggered callback or not.
    Why is this necessary? Sometimes callback are tied to multiple Inputs and the behavior of the callback
    has to be dependent on which Input triggered callback.
    Args:
        component_name: component_name (first argument of Input)
        component_property: component_property (second argument of Input)

    Returns:

    """
    ctx = dash.callback_context
    for item in ctx.triggered.__iter__():
        if f"{component_name}.{component_property}" == item["prop_id"]:
            return True
    return False


@app.callback(Output('project_page_id', 'style'),
              [Input("url", "pathname")])
def render_page_content(pathname):
    print(f"pathname is {pathname}")
    if pathname == "/":
        return {'display': 'block'}

    # elif pathname == "{0}".format(pathname):
    #     return {'display': 'none'}, {'display': 'block'}

    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


if __name__ == '__main__':
    app.run_server(host="0.0.0.0")
