import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
from dash import dcc
from dash import html
from plotly.subplots import make_subplots

from layout import moonpass_colors, font_family, CONTENT_STYLE
from price_data import get_current_price_from_coingecko, get_historical_price_from_coingecko
from utils import get_color_and_symbol

token = "solana"

custom_div = html.Div(id="custom_div_id", **{'data-url': "https://www.moonpass.ai/"})

date = "29_06"

# Community data
df_community = pd.read_csv("data/counts_{0}_{1}.csv".format(token, date), sep=';', decimal=',',
                           index_col="dates", parse_dates=True)
total_tweets = sum(df_community.tweet_count)
total_tweets /= 1000000
last_tweet_change = (df_community.tweet_count.iloc[-1] - df_community.tweet_count.iloc[-2]) / \
                    df_community.tweet_count.iloc[-2]
last_tweet_return = '{:.1%}'.format(last_tweet_change)

# Sentiment data
df_sentiment = pd.read_csv("data/timeseries_{0}_sentiment_{1}.csv".format(token, date), sep=";", decimal=',')

last_week_sentiment = df_sentiment.iloc[-7:]
last_week_sentiment = last_week_sentiment.sum()
last_neutral = last_week_sentiment["Neutral"]
last_negative = last_week_sentiment["Negative"]
last_positive = last_week_sentiment["Positive"]
neutral_percentage = round(last_neutral/(last_neutral + last_positive + last_negative), 2)
positive_percentage = round(last_positive/(last_neutral + last_positive + last_negative), 2)
negative_percentage = round(last_negative/(last_neutral + last_positive + last_negative), 2)

fig_sentiment = make_subplots(specs=[[{"secondary_y": True}]])
fig_sentiment.add_trace(go.Scatter(
    x=df_sentiment.date, y=df_sentiment.Negative,
    mode='lines',
    line=dict(width=0.5, color='rgb(169, 92, 104)'),  # Puce
    stackgroup='one',
    groupnorm='percent',
    name='negative'
))

fig_sentiment.add_trace(go.Scatter(
    x=df_sentiment.date, y=df_sentiment.Neutral,
    mode='lines',
    line=dict(width=0.5, color='rgb(255, 250, 160)'),  # Pastel Yellow
    stackgroup='one',
    groupnorm='percent',
    name='neutral'
))

fig_sentiment.add_trace(go.Scatter(
    x=df_sentiment.date, y=df_sentiment.Positive,
    mode='lines',
    line=dict(width=0.5, color='rgb(175, 225, 175)'),  # Pistachio
    stackgroup='one',
    groupnorm='percent',
    name='positive'
))

fig_sentiment.update_layout(
    showlegend=True,
    yaxis=dict(
        type='linear',
        range=[1, 100],
        ticksuffix='%')
)

# Price data
current_price_data = get_current_price_from_coingecko(token=token)
last_price = current_price_data["usd"]
last_price_return = '{:.1%}'.format(current_price_data["daily_return"])
last_price_update = current_price_data["last_updated_at"]
price_color_return, price_symbol = get_color_and_symbol(number=current_price_data["daily_return"])
tweet_color_return, tweet_arrow = get_color_and_symbol(number=last_tweet_change)
df_price = get_historical_price_from_coingecko(token=token)

# Topics data
df_topics = pd.read_csv("data/entity_tweets_{0}_{1}.csv".format(token, date), sep=";", decimal=',')

df_price_community = df_price.join(df_community, how="left").dropna()

fig_price_community = make_subplots(specs=[[{"secondary_y": True}]])
fig_price_community.add_bar(x=df_price_community.index,
                            y=df_price_community["tweet_count"],
                            name="tweet count")
fig_price_community.add_trace(
    go.Scatter(
        x=df_price_community.index, y=df_price_community.price, mode='lines',
        name="{0} price".format(token), visible='legendonly'
    ),
    secondary_y=True
)


fig_price_community.update_yaxes(title_text="tweets", secondary_y=False)
fig_price_community.update_yaxes(title_text="price", secondary_y=True)
# Add ranges with sliders https://plotly.com/python/range-slider/
fig_price_community.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label="1m",
                     step="month",
                     stepmode="backward"),
                dict(count=6,
                     label="6m",
                     step="month",
                     stepmode="backward"),
                dict(count=1,
                     label="YTD",
                     step="year",
                     stepmode="todate"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
    )
)

fig_sentiment.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label="1m",
                     step="month",
                     stepmode="backward"),
                dict(count=6,
                     label="6m",
                     step="month",
                     stepmode="backward"),
                dict(count=1,
                     label="YTD",
                     step="year",
                     stepmode="todate"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
    )
)

# Add price for sentiment graph
fig_sentiment.add_trace(
    go.Scatter(
        x=df_price_community.index, y=df_price_community.price, mode='lines',
        name="{0} price".format(token), visible='legendonly'
    ),
    secondary_y=True
)

fig_sentiment.update_yaxes(title_text="sentiment %", secondary_y=False)
fig_sentiment.update_yaxes(title_text="price", secondary_y=True)

# Style
style_arrows = {"marginRight": "5px"}
twitter_symbol = html.I(className="fab fa-twitter", style=style_arrows)

# FIXME: Add return button
sidebar_header = dbc.Row(
    [
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
# TODO: Add hovering for project selection
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
                                href="/", active="exact",
                                style={'paddingTop': "0px", "color": "white"}
                                ),

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

# FIXME: Add functionality to "Top web3 projects" button
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

vertical_space = dbc.Row(
    dbc.Col(html.Br())
)

title_row = dbc.Row(
    dbc.Col(
        html.H2(children='{0}'.format(token),
                style={
                    'textAlign': 'left',
                    'color': moonpass_colors["purple"]
                }
                ), width="auto"
    )
)

price_row = dbc.Row(
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
                        "24h price change",
                        placement="bottom",
                        target="return_id",
                    ),
                ]
            ), width=4
        ),

        dbc.Col(
            [
                html.Div(
                    [
                        twitter_symbol,
                        html.A(html.H5("Followers: 1.9M"), href="https://twitter.com/solana", target="_blank",
                               style={"color": moonpass_colors["purple"]}),
                    ],
                    style={"display": "flex"}
                )
            ], width=4
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
            ], style={"display": "inline-block"}, width=4
        ),
    ]
)

# https://plotly.com/python/indicator/
# FIXME: Change dynamically numerical value of community growth
# FIXME: Update colors automatically
indicators_section = dbc.Row(
    [
        dbc.Col(
            [
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Community growth", className="card-title"),
                        html.H3(
                            "27 😔", className="card-subtitle"
                        ),
                        html.Span(
                            [
                                html.I(className="fas fa-arrow-circle-down down", style=style_arrows),
                                html.Span("2.3% vs last week", className="down")
                            ], style={"color": tweet_color_return}
                        )
                    ], style={"text-align": "center"})
                ], id="card_growth_id"),

                dbc.Tooltip(
                    "A value of 100 represents steady growth and engagement",
                    target="card_growth_id",
                    placement="bottom"
                )
            ]
        ),

        dbc.Col(
            [
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Community sentiment", className="card-title"),
                        html.H3(
                            "43 🤷", className="card-subtitle"
                        ),
                        html.Span(
                            [
                                html.Span("{:.1%} of tweets neutral or negative".format(
                                    neutral_percentage+negative_percentage
                                ))
                            ], style={"color": "orange"}
                        )
                    ], style={"text-align": "center"}
                    )
                ], id="card_sentiment_id"),

                dbc.Tooltip(
                    "A value of 100 represents overwhelming amount of positive tweets",
                    target="card_sentiment_id",
                    placement="bottom"
                )
            ]
        ),

        dbc.Col(
            [
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Expert voices", className="card-title"),
                        html.H3(
                            "36 😕", className="card-subtitle"
                        ),
                        html.Span(
                            [
                                html.I(className="fas fa-arrow-circle-down down", style=style_arrows),
                                html.Span("70% of experts expressed concerns")
                            ], style={"color": "orange"}
                        )
                    ], style={"text-align": "center"})
                ], id="card_voices_id"),

                dbc.Tooltip(
                    "A value of 100 represents outstanding support of crypto experts",
                    target="card_voices_id",
                    placement="bottom"
                )
            ]
        )
    ], style={"marginTop": "20px"}
)

# FIXME: Change order of Twitter button in dashboard layout
twitter_share_button = dbc.Row(
    # Source: https://publish.twitter.com/?buttonType=TweetButton&widget=Button &
    # https://github.com/plotly/dash/pull/237
    dbc.Col(html.A("Tweet", **{'data-url': "www.moonpass.ai", "data-via": "moonpass_ai",
                               "data-related": "moonpass_ai", "data-show-count": "false"},
                   href="https://twitter.com/share?ref_src=twsrc%5Etfw", target="_blank", style={"float": "right"},
                   className="twitter-share-button")
            )
)

community_section = dbc.Row(
    [
        dbc.Col(
            [
                html.H4("Community growth", style={"color": moonpass_colors["pink"]}),
                dcc.Graph(figure=fig_price_community),
            ], width=10
        ),

        dbc.Col(
            [
                html.H5("Key metrics", style={"color": moonpass_colors["pink"]}),
                dbc.ListGroup(
                    [
                        dbc.ListGroupItem(children=[
                            html.Div([
                                twitter_symbol, "2022", html.Span("{0}M".format(str(round(total_tweets, 1))),
                                                                  style={"color": "#36454F", "float": "right"})
                            ], id="tweets_2022_id"),

                            dbc.Tooltip("Total amount of tweets retrieved in 2022",
                                        target="tweets_2022_id", placement="left")
                        ]),

                        dbc.ListGroupItem(children=[
                            html.Div(
                                [
                                    twitter_symbol, html.Span(children=[
                                    html.I(className=tweet_arrow, style=style_arrows), last_tweet_return],
                                    style={"color": tweet_color_return,
                                           "marginLeft": "10px", "float": "right"})
                                ], id="tweet_change_id"
                            ),
                            dbc.Tooltip("24h daily tweets change", target="tweet_change_id", placement="left")
                        ]),

                        dbc.ListGroupItem(children=[
                            html.Div(
                                [
                                    html.I(className="fas fa-dollar-sign", style=style_arrows), html.Span(children=[
                                    html.I(className=price_symbol, style=style_arrows), last_price_return],
                                    style={"color": price_color_return, "marginLeft": "10px", "float": "right"})
                                ], id="price_change_id"
                            ),
                            dbc.Tooltip("24h price change", target="price_change_id", placement="left")
                        ]),

                    ], style={"marginTop": "80px"}
                )
            ], width=2
        )
    ]
)

# TODO: Add tooltip with number of tweets for topics being discussed
sentiment_section = dbc.Row(
    [
        dbc.Col(
            [
                html.H4("Sentiment development", style={"color": moonpass_colors["pink"]}),
                dcc.Graph(figure=fig_sentiment),
            ], width=10
        ),

        dbc.Col(
            [
                html.H5("Topics discussed", style={"color": moonpass_colors["pink"]}),
                dbc.ListGroup(
                    [
                        dbc.ListGroupItem(html.Small("1. {0}".format(df_topics.iloc[0].entity_name))),
                        dbc.ListGroupItem(html.Small("2. {0}".format(df_topics.iloc[2].entity_name))),
                        dbc.ListGroupItem(html.Small("3. {0}".format(df_topics.iloc[3].entity_name))),
                        dbc.ListGroupItem(html.Small("4. {0}".format(df_topics.iloc[4].entity_name))),
                        dbc.ListGroupItem(html.Small("5. {0}".format(df_topics.iloc[5].entity_name))),
                    ], style={"marginTop": "80px"}
                )
            ],
            width=2
        )
    ]
)

voices_section = dbc.Row(
    dbc.Col(
        [
            html.H4("Most engaged tweets last week", style={"color": moonpass_colors["pink"]}),
        ], width=10
    ),
)

# TODO: Create dynamically this section
# TODO: Change size of tweets
# https://developer.twitter.com/en/docs/twitter-for-websites/embedded-tweets/overview
bulls_section = dbc.Row(
    dbc.Col(
        [
            html.H4("What the bulls are saying 🐂", className="card-title"),
            dbc.ListGroup(
                [
                    dbc.ListGroupItem(
                        html.Iframe(
                            srcDoc='''
                                    <blockquote class="twitter-tweet" data-lang="en" data-theme="light"><p lang="en" dir="ltr">It feels to me like <a href="https://twitter.com/search?q=%24SOL&amp;src=ctag&amp;ref_src=twsrc%5Etfw">$SOL</a> is going thru a similar trough of disillusionment as <a href="https://twitter.com/search?q=%24ETH&amp;src=ctag&amp;ref_src=twsrc%5Etfw">$ETH</a> did back in 2018. In bear markets prices aren&#39;t just reflexive—sentiment is too. <a href="https://twitter.com/solana?ref_src=twsrc%5Etfw">@solana</a> has a vibrant developer ecosystem and its downtime issues are solvable. This will be obvious in retrospect.</p>&mdash; spencernoon.eth (@spencernoon) <a href="https://twitter.com/spencernoon/status/1541497867373772802?ref_src=twsrc%5Etfw">June 27, 2022</a></blockquote> 
                                    <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
                                    ''',
                        )
                    ),
                    dbc.ListGroupItem(
                        html.Iframe(
                            srcDoc='''
                                    <blockquote class="twitter-tweet"><p lang="en" dir="ltr">1/<br><br>solana poses a large and growing threat to ethereum.<br><br>you’re wrong if you believe otherwise bc “haha VC chain offline”.<br><br>i can explain why - after following both ecosystems closely for years and talking to 100s of devs &amp; users.<br><br>i want the EVM to win. but i’m also not blind.</p>&mdash; nathan.eth (@nathanweb3) <a href="https://twitter.com/nathanweb3/status/1540122390079934464?ref_src=twsrc%5Etfw">June 23, 2022</a></blockquote> 
                                    <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
                                    ''',
                        )
                    ),
                    dbc.ListGroupItem(
                        html.Iframe(
                            srcDoc='''
                                    <blockquote class="twitter-tweet"><p lang="en" dir="ltr">Solana is doing 5,200 TPS with $.00002 fees and you are still on 30 TPS anon? 🥹 Feel bad for you son <a href="https://t.co/JbmbaWwlum">https://t.co/JbmbaWwlum</a></p>&mdash; S◎L Legend {6666} (@SolanaLegend) <a href="https://twitter.com/SolanaLegend/status/1538839311973552133?ref_src=twsrc%5Etfw">June 20, 2022</a></blockquote> 
                                    <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
                                    ''',
                        )
                    )
                ],
                horizontal="lg",
            ),
        ]
    )
)

bears_section_1 = dbc.Row(
    dbc.Col(
        [
            html.H4("What the bears are saying 🐻", className="card-title"),
            dbc.ListGroup(
                [

                    dbc.ListGroupItem(
                        html.Iframe(
                            srcDoc='''
                        <blockquote class="twitter-tweet"><p lang="en" dir="ltr">/1 <br><br>The latest Solana update has in-fact made the network too fast and caused MAJOR problems.<br><br>I&#39;ll explain why in this🧵thread...</p>&mdash; Cel◎n 🚧 (@0xCelon) <a href="https://twitter.com/0xCelon/status/1538921568893542401?ref_src=twsrc%5Etfw">June 20, 2022</a></blockquote> 
                        <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
                        ''',
                        )
                    ),

                    dbc.ListGroupItem(
                        html.Iframe(
                            srcDoc='''
                        <blockquote class="twitter-tweet"><p lang="en" dir="ltr">A “decentralized” protocol built on Solana votes to take over someone’s funds<br><br>Celsius “designed to help you reach your financial goals” denies users access to their funds<br><br>UST algorithmic “stablecoin” failing, destroying lives<br><br>The current state of crypto. We gotta do better.</p>&mdash; Aleksandra Huk (@HukAleksandra) <a href="https://twitter.com/HukAleksandra/status/1538856271100641280?ref_src=twsrc%5Etfw">June 20, 2022</a></blockquote> 
                        <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
                        ''',
                        )
                    ),

                    dbc.ListGroupItem(
                        html.Iframe(
                            srcDoc='''
                        <blockquote class="twitter-tweet"><p lang="en" dir="ltr">Of all the things That happened this cycle, Solana’s vote to confiscate a users funds is BY FAR the most egregious.<br><br>It’s worse even then the ETH DAO confiscation.<br><br>It’s the clearest demonstration yet that PoS is not a consensus mechanism.</p>&mdash; Yago (@EdanYago) <a href="https://twitter.com/EdanYago/status/1538725149838647297?ref_src=twsrc%5Etfw">June 20, 2022</a></blockquote>
                         <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
                        ''',
                        )
                    ),
                ], horizontal="md",
            ),
        ]
    )
)

bears_section_2 = dbc.Row(
    dbc.Col(
        dbc.ListGroup(
            [
                dbc.ListGroupItem(
                    html.Iframe(
                        srcDoc='''
                <blockquote class="twitter-tweet"><p lang="en" dir="ltr">If the Solana devs aren&#39;t afraid to liquidate a whale then they aren&#39;t afraid to do it to you either.</p>&mdash; Lucid (@LucidCiC) <a href="https://twitter.com/LucidCiC/status/1538868905535410176?ref_src=twsrc%5Etfw">June 20, 2022</a></blockquote> 
                <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
                ''',
                    )
                ),

                dbc.ListGroupItem(
                    html.Iframe(
                        srcDoc='''
                    <blockquote class="twitter-tweet"><p lang="en" dir="ltr">How <a href="https://twitter.com/_Urkann?ref_src=twsrc%5Etfw">@_Urkann</a> has prepared to sweep tens of thousands of <a href="https://twitter.com/search?q=%24SOL&amp;src=ctag&amp;ref_src=twsrc%5Etfw">$SOL</a> whilst enslaving the entirety of <a href="https://twitter.com/hashtag/Solana?src=hash&amp;ref_src=twsrc%5Etfw">#Solana</a> with his project, <a href="https://twitter.com/DegenSweepers?ref_src=twsrc%5Etfw">@DegenSweepers</a>:<br><br>🧵 1/20</p>&mdash; Batman (@BatmanOfCT) <a href="https://twitter.com/BatmanOfCT/status/1541851160512024579?ref_src=twsrc%5Etfw">June 28, 2022</a></blockquote>
                    <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
                    ''',
                    )
                ),
                dbc.ListGroupItem(
                    html.Iframe(
                        srcDoc='''
                    <blockquote class="twitter-tweet"><p lang="en" dir="ltr">I will fight the Botted projects, WE will fight them <a href="https://twitter.com/hashtag/UrkannArmy?src=hash&amp;ref_src=twsrc%5Etfw">#UrkannArmy</a> <br>I&#39;m tired of seeing these usurpers taking the solana community for fools. A lot of newbies will be fooled and this will only tarnish the image of NFTs.<br>I won&#39;t allow it. <br>who is with me?</p>&mdash; Urkann 🧹 (33.3%) {C̶U̶L̶T̶} aka The Sweepooor 💀 (@_Urkann) <a href="https://twitter.com/_Urkann/status/1540058572704317442?ref_src=twsrc%5Etfw">June 23, 2022</a></blockquote>
                    <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
                    ''',
                    )
                ),
            ], horizontal="md",
        )
    )
)

project_page_children = html.Div([
    title_row,

    dbc.Row(
        dbc.Col(html.Hr())
    ),

    price_row,

    indicators_section,

    vertical_space,

    twitter_share_button,

    vertical_space,

    community_section,

    vertical_space,

    sentiment_section,

    voices_section,

    vertical_space,

    bulls_section,

    vertical_space,

    bears_section_1,

    bears_section_2

])

# Content Page
content = html.Div(
    id="page-content", style=CONTENT_STYLE, children=[
        # html.Div(id='landing_page_id', children=landing_page_children),
        html.Div(id='project_page_id', children=project_page_children),
        html.Footer([
            html.I(className="far fa-copyright"), "2022 moonpass.ai"],
            style={"position": "absolute", "bottom": "1", "right": "0", "marginRight": "15px", "marginTop": "15px",
                   "fontSize": "80%"})
    ]
)
