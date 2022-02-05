from itertools import count
from turtle import color
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from data import (
    countries_df,
    totals_df,
    dropdown_options,
    make_global_df,
    make_country_df,
)
from builders import make_table

stylesheets = [
    "https://cdn.jsdelivr.net/npm/reset-css@5.0.1/reset.min.css",
    "https://fonts.googleapis.com/css2?family=Open+Sans&display=swap",
]

app = dash.Dash(__name__, external_stylesheets=stylesheets)

bubble_map = px.scatter_geo(
    countries_df,
    size="확진",
    size_max=40,
    title="나라별 확진자",
    template="plotly_dark",
    hover_name="국가별",
    color="확진",
    color_continuous_scale=px.colors.sequential.Oryel,
    locations="국가별",
    locationmode="country names",
    hover_data={
        "확진": ":,2f",
        "완치": ":,2f",
        "사망": ":,2f",
        "국가별": False,
    },
)
bubble_map.update_layout(margin=dict(l=0, r=0, t=50, b=0))

bars_graph = px.bar(
    totals_df,
    x="condition",
    y="count",
    hover_data={"count": ":,"},
    template="plotly_dark",
    title="전체 유형별 통계",
    labels={"condition": "유형", "count": "인원(명)", "color": "유형"},
)
bars_graph.update_traces(marker_color=["#e74c3c", "#8e44ad", "#27ae60"])

app.layout = html.Div(
    style={
        "minHeight": "100vh",
        "backgroundColor": "#111111",
        "color": "white",
        "fontFamily": "Open Sans, sans-serif",
    },
    children=[
        html.Header(
            style={"textAlign": "center", "paddingTop": "50px", "marginBottom": 100},
            children=[html.H1("Covid-19 Dashboard", style={"fontSize": 40})],
        ),
        html.Div(
            style={
                "display": "grid",
                "gap": 50,
                "gridTemplateColumns": "repeat(4, 1fr)",
            },
            children=[
                html.Div(
                    style={"grid-column": "span 3"},
                    children=[dcc.Graph(figure=bubble_map)],
                ),
                html.Div(children=[make_table(countries_df)]),
            ],
        ),
        html.Div(
            style={
                "display": "grid",
                "gap": 50,
                "gridTemplateColumns": "repeat(4, 1fr)",
            },
            children=[
                html.Div(children=[dcc.Graph(figure=bars_graph)]),
                html.Div(
                    style={"grid-column": "span 3"},
                    children=[
                        dcc.Dropdown(
                            style={
                                "width": 320,
                                "margin": "0 auto",
                                "color": "#111111",
                            },
                            id="country",
                            options=[
                                {"label": country, "value": country}
                                for country in dropdown_options
                            ],
                        ),
                        dcc.Graph(id="country_graph"),
                    ],
                ),
            ],
        ),
    ],
)


@app.callback(Output("country_graph", "figure"), [Input("country", "value")])
def update_hello(value):
    if value:
        df = make_country_df(value)
    else:
        df = make_global_df()
    df.columns = ["날짜", "확진", "사망", "완치"]
    fig = px.line(
        df,
        x="날짜",
        y=["확진", "사망", "완치"],
        template="plotly_dark",
        labels={
            "value": "인원(명)",
            "variable": "유형",
        },
        hover_data={"value": ":,", "variable": False, "날짜": False},
    )
    fig.update_xaxes(rangeslider_visible=True)
    fig["data"][0]["line"]["color"] = "#e74c3c"
    fig["data"][1]["line"]["color"] = "#8e44ad"
    fig["data"][2]["line"]["color"] = "#27ae60"
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
