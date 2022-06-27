import pandas as pd
from dash import dcc
import dash_bootstrap_components as dbc
from dash import html
import plotly.express as px
import plotly.graph_objects as go

from layout import moonpass_colors, font_family, CONTENT_STYLE
from price_data import get_current_price_from_coingecko, get_historical_price_from_coingecko
from utils import get_color_and_symbol, join_two_dfs

token = "solana"

# Community Data
df_community = pd.read_csv("data/{0}_27_06.csv".format(token), sep=';', decimal=',',
                           index_col="dates", parse_dates=True)
df_community["tweet_count"] /= 1000
total_tweets = sum(df_community.tweet_count)
total_tweets /= 1000000
last_tweet_change = (df_community.tweet_count.iloc[-1] - df_community.tweet_count.iloc[-2]) / \
                    df_community.tweet_count.iloc[-2]
last_tweet_return = '{:.1%}'.format(last_tweet_change)

# FIXME: Change data
# TODO: Add tweets with positive and negative sentiment
df = px.data.gapminder().query("continent == 'Oceania'")
fig_sentiment = px.area(df, x="year", y="pop", color="country", line_group="country")

# Price data
current_price_data = get_current_price_from_coingecko(token=token)
last_price = current_price_data["usd"]
last_price_return = '{:.1%}'.format(current_price_data["daily_return"])
last_price_update = current_price_data["last_updated_at"]
price_color_return, price_symbol = get_color_and_symbol(number=current_price_data["daily_return"])
tweet_color_return, tweet_symbol = get_color_and_symbol(number=last_tweet_change)

df_price = get_historical_price_from_coingecko(token=token)

# TODO: Check if the join is necessary or working with two separate dfs is fine
df_price_community = join_two_dfs(df_price, df_community)
fig_price_community = px.bar(df_price_community, x="dates", y="tweet_count")
fig_price_community.add_trace(
    go.Scatter(x=df_price_community.dates, y=df_price_community.price, mode='lines', name="price")
)

# Style
style_arrows = {"marginRight": "5px"}

sidebar_header = dbc.Row(
    [
        # FIXME: Add return button
        dbc.Col(
            html.Label(
                dbc.CardImg(src='assets/logo_moonpass_white.png',
                            style={'height': "100%", 'width': '100%', "maxHeight": "200px",
                                   "maxWidth": "200px", "borderRadius": "15px"}),
                className="display-4"),
            style={"fontFamily": font_family}
        ),

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

# FIXME: Add button to return home
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
                                href="/solana",  # active="exact",
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
                                    className='align-self-center'),
                        # TODO: Add functionality to button
                        dbc.Button("Top web3 projects 🚀", color="primary", outline=True,
                                   className="card-footer text-center", id="button_web3_projects")
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
                                    className='align-self-center'),
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
            html.H2(children='Moonpass - Solana Project Overview',
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
                html.Div(
                    [
                        html.H5(children=[html.Span("Price: ${0}".format(last_price), id="price_id"), html.Span(
                            children=[html.I(className=price_symbol, style=style_arrows), last_price_return],
                            style={"color": price_color_return, "marginLeft": "10px"}, id="return_id")],
                                style={"color": moonpass_colors["purple"]}),

                        dbc.Tooltip(
                            "Fetched at {0}".format(last_price_update),
                            placement="bottom",
                            target="price_id",
                        ),

                        dbc.Tooltip(
                            "24 hours return",
                            placement="bottom",
                            target="return_id",
                        ),
                    ]
                )
            ),

            dbc.Col(
                [
                    html.Div(
                        [
                            html.I(className="fab fa-twitter", style={"paddingRight": "7px"}),
                            html.A(html.H5("Followers: 1.9M"), href="https://twitter.com/solana", target="_blank",
                                   style={"color": moonpass_colors["purple"]})
                        ],
                        style={"display": "flex"}
                    )
                    # html.A("Tweet", className="twitter-share-button", href="https://twitter.com/intent/tweet?text=Hello%20world")
                ]
            ),

            dbc.Col(
                [
                    dbc.ButtonGroup(
                        [
                            dbc.Button(children=["Website ", html.I(className="fas fa-globe")], outline=True,
                                       color="primary", href="https://solana.com/", target="_blank"),
                            dbc.Button(children=["Whitepaper ", html.I(className="fa fa-book")], outline=True,
                                       color="primary", href="https://solana.com/solana-whitepaper.pdf",
                                       target="_blank"),
                            dbc.Button(children=["GitHub ", html.I(className="fab fa-github")], outline=True,
                                       color="primary", href="https://github.com/solana-labs/solana", target="_blank"),
                        ], size="sm",
                    ),
                ], style={"display": "inline-block"}
            )
        ]
    ),

    dbc.Row(
        dbc.Col(html.Br())
    ),

    dbc.Row(
        [
            dbc.Col(
                [
                    html.H4("Community Growth", style={"color": moonpass_colors["pink"]}),
                    dcc.Graph(figure=fig_price_community),
                    # FIXME: Modify slider to buttons similar to CoinmarketCap
                    html.Div([
                        dcc.RangeSlider(min=0, max=20, value=[5, 15], id='community-range-slider'),
                        html.Div(id='community-slider-output-container')
                    ]),
                ], width=10
            ),

            dbc.Col(
                [
                    html.H5("Key metrics", style={"color": moonpass_colors["pink"]}),
                    dbc.ListGroup(
                        [
                            dbc.ListGroupItem(children=["2022 tweets",
                                                        html.Span("{0}M".format(str(round(total_tweets, 1))),
                                                                  style={"color": "#36454F", "float": "right"})]),

                            dbc.ListGroupItem(children=["Tweets change", html.Span(children=[
                                html.I(className=tweet_symbol, style=style_arrows), last_tweet_return],
                                style={"color": tweet_color_return,
                                       "marginLeft": "10px", "cursor": "pointer", "float": "right"})]),

                            dbc.ListGroupItem(children=["Price change",
                                                        html.Span(children=[
                                                            html.I(className=price_symbol, style=style_arrows),
                                                            last_price_return],
                                                            style={"color": price_color_return, "marginLeft": "10px",
                                                                   "cursor": "pointer", "float": "right"})]),

                            # FIXME: Change correlation automatically
                            dbc.ListGroupItem(children=["Correlation",
                                                        html.Span(children=[0.75],
                                                                  style={"color": "#36454F", "marginLeft": "10px",
                                                                         "float": "right"})]),
                        ], style={"marginTop": "80px"}
                    )
                ], width=2
            )
        ]
    ),

    dbc.Row(
        dbc.Col(html.Br())
    ),

    dbc.Row(
        [
            dbc.Col(
                [
                    html.H4("Sentiment development", style={"color": moonpass_colors["pink"]}),
                    dcc.Graph(figure=fig_sentiment),
                    # FIXME: Modify slider to buttons similar to CoinmarketCap
                    html.Div([
                        dcc.RangeSlider(min=0, max=20, value=[5, 15], id='sentiment-range-slider'),
                        html.Div(id='sentiment-slider-output-container')
                    ])
                ], width=10
            ),

            dbc.Col(
                [
                    html.H5("Topics being discussed", style={"color": moonpass_colors["pink"]}),
                    dbc.ListGroup(
                        [
                            dbc.ListGroupItem("StepN"),
                            dbc.ListGroupItem("Not Okay Bear"),
                            dbc.ListGroupItem("Solana congested"),
                        ], style={"marginTop": "80px"}
                    )
                ],
                width=2
            )
        ]
    ),

    dbc.Row(
        [
            dbc.Col(
                dbc.CardBody(
                    [
                        html.H4("What the bulls are saying 🐂", className="card-title"),
                        html.H6("Twitter Profile", className="card-subtitle"),
                        html.P(
                            "Solana is a great blockchain because they solve a real issue in the ecosystem, they"
                            "lower the transaction fees",
                            className="card-text",
                        ),
                        dbc.CardLink("Tweet link", href="https://google.com", target="_blank"),
                    ]
                ),
            ),

            dbc.Col(
                dbc.CardBody(
                    [
                        html.H4("What the bears are saying 🐻", className="card-title"),
                        html.H6("Twitter Profile", className="card-subtitle"),
                        html.P(
                            "Tweet content, this project is very bad. Solana is congested the whole time making it not "
                            "decentralized",
                            className="card-text"),
                        dbc.CardLink("Tweet link", href="https://google.com", target="_blank"),
                    ]
                ),
            ),
        ]
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
