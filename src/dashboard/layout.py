import dash_bootstrap_components as dbc
import dash_html_components as html

storage_type = 'session'

DEFAULT_PLOTLY_COLORS = ['rgb(31, 119, 180)', 'rgb(255, 127, 14)',
                         'rgb(44, 160, 44)', 'rgb(214, 39, 40)',
                         'rgb(148, 103, 189)', 'rgb(140, 86, 75)',
                         'rgb(227, 119, 194)', 'rgb(127, 127, 127)',
                         'rgb(188, 189, 34)', 'rgb(23, 190, 207)']

moonpass_colors = {
    'purple': 'rgb(121, 71, 247)',
    'pink': 'rgb(231, 82, 117)',
    'light_blue': 'rgb(30, 155, 215)',
    'white': 'rgb(255, 255, 255)',
    'very light blue': 'rgb(148, 228, 255)',
    'dark_blue': 'rgb(19, 29, 51)'
}


def color_gradient(gradient_factor: float, col: tuple):
    """
    Returns a rgb color in the blue family

    Args:
        gradient_factor: float of how strong the blue color shall be changed, max is 2
        col:
    Returns:
        rgb color in blue family
    """

    _red = col[0]
    _green = col[1]
    _blue = col[2]

    if gradient_factor < 1:
        _red = _red * gradient_factor
        _green = _green * gradient_factor
        _blue = _blue * gradient_factor
    elif gradient_factor >= 1:
        _red = _red + ((gradient_factor - 1) * (255 - _red))
        _green = _green + ((gradient_factor - 1) * (255 - _green))
        _blue = _blue + ((gradient_factor - 1) * (255 - _blue))

    result = "rgb({red}, {green}, {blue})".format(red=_red, green=_green, blue=_blue)
    return result


# COLORS
main_color_tuple = (0, 123, 255)
background_page = color_gradient(1.98, main_color_tuple)  # "rgb(244, 244, 251)"
font_color = 'grey'
font_family = 'Poppins'  # "https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500&display=swap"

sidebar_header = dbc.Row(
    [
        dbc.Col(html.Label(dbc.CardImg(src='assets/logo_moonpass_white.png',
                                       style={'height': "100%", 'width': '100%', "maxHeight": "200px",
                                              "maxWidth": "200px", "borderRadius": "15px"}),
                           className="display-4"), style={"fontFamily": font_family}),

        dbc.Col(
            [
                html.Button(
                    html.Span(className="navbar-toggler-icon"),
                    className="navbar-toggler",
                    style={
                        "color": moonpass_colors["pink"],
                        "borderColor": moonpass_colors["white"],
                    },
                    id="navbar-toggle",
                ),
                html.Button(
                    # use the Bootstrap navbar-toggler classes to style
                    html.Span(className="navbar-toggler-icon"),
                    className="navbar-toggler",
                    # the navbar-toggler classes don't set color
                    style={
                        "color": moonpass_colors["pink"],
                        "borderColor": moonpass_colors["white"],
                    },
                    id="sidebar-toggle",
                ),
            ],
            # the column containing the toggle will be only as wide as the toggle
            width="auto",
            align="center",
        ),
    ]
)

sidebar = html.Div(
    [
        sidebar_header,
        # we wrap the horizontal rule and short blurb in a div that can be hidden on a small screen
        html.Div(
            [
                html.Hr(style={"backgroundColor": "white"}),
                html.P(
                    "Web3 Projects",
                    className="lead",
                    style={"fontFamily": font_family}
                ),
            ],
            id="blurb",
        ),
        # use the Collapse component to animate hiding / revealing links
        dbc.Collapse(
            dbc.Nav(
                [

                    dbc.NavLink([html.I(className=""), "Solana"],
                                href="/solana", active="exact",
                                style={'paddingTop': "0px"}),

                    dbc.NavLink([html.I(className=""), "StepN"],
                                href="/stepn", disabled=True,
                                style={'paddingTop': "0px"}),

                    dbc.NavLink([html.I(className=""), "Staratlas"],
                                href="/staratlas", disabled=True,
                                style={'paddingTop': "0px"}),

                    dbc.NavLink([html.I(className=""), "BAYC"],
                                href="/bayc", disabled=True,
                                style={'paddingTop': "0px"}),

                    dbc.NavLink([html.I(className=""), "Moonbirds"],
                                href="/moonbirds", disabled=True,
                                style={'paddingTop': "0px"}),
                ],
                vertical=True,
                pills=True,
            ),
            id="collapse",
            style={"fontFamily": font_family}
        ),
    ],
    id="sidebar",
)

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    # "margin-left": "18rem",
    # "margin-right": "2rem",
    "padding": "2rem 1rem",
    'color': font_color,
    'fontFamily': font_family
}

landing_page_children = html.Div([
    dbc.Row(
        dbc.Col(
            html.H2(children='Moonpass App',
                    style={
                        'textAlign': 'left',
                        'color': '#000080'
                    }
                    ), width="auto"
        )
    ),

    dbc.Row(
        dbc.Col(html.Hr())
    ),
])

project_page_children = html.Div([
    dbc.Row(
        dbc.Col(
            html.H2(children='Project Overview',
                    style={
                        'textAlign': 'left',
                        'color': '#000080'
                    }
                    ), width="auto"
        )
    ),

    dbc.Row(
        dbc.Col(html.Hr())
    ),
])

# Content Page
content = html.Div(id="page-content", style=CONTENT_STYLE, children=[
    html.Div(id='landing_page_id', children=landing_page_children),
    html.Div(id='project_page_id', children=project_page_children),
    html.Div([html.I(className="far fa-copyright"), "    2022 moopass.ai"],
             style={"position": "absolute", "bottom": "1", "right": "0", "marginRight": "15px", "fontSize": "80%"})
])
