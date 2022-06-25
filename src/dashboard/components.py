import dash_bootstrap_components as dbc
import dash_html_components as html

from layout import moonpass_colors, font_family, CONTENT_STYLE

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
                    # TODO: Add hovering for project selection
                    #  Add dynamically many buttons
                    dbc.NavLink([html.I(className=""), "Solana"],
                                href="/solana", # active="exact",
                                style={'paddingTop': "0px",
                                       "color": "white"
                                       }),

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

landing_page_children = html.Div([
    dbc.Row(
        dbc.Col(
            html.H2(children='Moonpass App',
                    style={
                        'textAlign': 'left',
                        'color': moonpass_colors["purple"]
                    }
                    ), width="auto"
        )
    ),

    dbc.Row(
        dbc.Col(html.Hr())
    ),

    dbc.Row(
        [
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardBody(
                            [
                                html.H4("Analyze fully a web3 project", className="card-title",
                                        style={"color": moonpass_colors["purple"]}),
                                html.P("Understand whether a project is good to invest based on social data",
                                       className="card-text", style={"color": moonpass_colors["purple"]})
                            ]
                        ),
                        dbc.CardImg(src="assets/projects.png", top=True, style={"width": "60%", "height": "60%"},
                                    className = 'align-self-center'),
                        # TODO: Add functionality to button
                        dbc.Button("Top web3 projects 🚀", color="primary", outline=True,
                                   className="card-footer text-center")
                    ]
                ),
                width=6
            ),

            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardBody(
                            [
                                html.H4("Discover the newest projects", className="card-title",
                                        style={"color": moonpass_colors["pink"]}),
                                html.P("Never miss the coolest projects and what the community is talking about them",
                                       className="card-text", style={"color": moonpass_colors["pink"]})
                            ]
                        ),
                        dbc.CardImg(src="assets/rocket.png", top=True, style={"width": "60%", "height": "60%"},
                                    className = 'align-self-center'),
                        dbc.Button("Trending web3 projects 🔥", color="secondary", outline=True, disabled=True,
                                   className="card-footer text-center")
                    ],
                ),
                width=6
            )
        ]
    )
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
content = html.Div(
    id="page-content", style=CONTENT_STYLE, children=[
        html.Div(id='landing_page_id', children=landing_page_children),
        html.Div(id='project_page_id', children=project_page_children),
        html.Footer([
            html.I(className="far fa-copyright"), "2022 moopass.ai"],
            style={"position": "absolute", "bottom": "1", "right": "0", "marginRight": "15px", "marginTop": "15px",
                   "fontSize": "80%"})
    ]
)
