from django.shortcuts import render

import plotly.graph_objects as go
from plotly.subplots import make_subplots


import pandas as pd


# Create your views here.


def index(request):
    df = pd.read_csv(
        'https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')

    close = df['AAPL.Close']

    fig = make_subplots(rows=2, shared_xaxes=True, row_heights=[0.6, 0.4],
                        specs=[[{"secondary_y": True}],
                               [{}]
                               ]
                        )

    fig.add_trace(go.Scatter(x=df['Date'], y=df["AAPL.Adjusted"], name="Adjusted"),
                  row=2, col=1,
                  )

    fig.add_trace(go.Bar(x=df['Date'],
                         y=df['AAPL.Volume'],
                         name="Volume"), row=1, col=1, secondary_y=False)

    fig.add_trace(go.Candlestick(x=df['Date'],
                                 open=df['AAPL.Open'],
                                 high=df['AAPL.High'],
                                 low=df['AAPL.Low'],
                                 close=df['AAPL.Close']
                                 ),
                  row=1, col=1,
                  secondary_y=True)
    df["sma1"] = close.rolling(window=7).mean()
    df["sma2"] = close.rolling(window=14).mean()
    fig.add_trace(
        go.Scatter(
            x=df['Date'],
            y=df["sma1"],
            name="sma(7)",
            line=dict(
                color='darkorange',
                width=1)
        ),
        row=1, col=1, secondary_y=True)
    fig.add_trace(
        go.Scatter(
            x=df['Date'],
            y=df["sma2"],
            name="sma(14)",
            line=dict(
                color='tomato',
                width=1)
        ),
        row=1, col=1, secondary_y=True)

    event = [{"side": "BUY",
              "price": df['AAPL.Close'][0],
              "size":1000},
             {"side": "SELL",
              "price": df['AAPL.Close'][100],
              "size":1000},
             {"side": "BUY",
              "price": df['AAPL.Close'][300],
              "size":1000}]
    fig.add_trace(
        go.Scatter(x=df["Date"][[0, 100, 300]], y=df["AAPL.Close"][[0, 100, 300]],
                   name="orders", mode="markers",
                   text=event, textposition="bottom left", textfont=dict(
            family="sans serif",
            size=20,
            color="black"),
            marker=dict(
            color='maroon',
            size=6,)
        ),
        row=1, col=1, secondary_y=True)
    plot_fig = fig.to_html(include_plotlyjs=False)

    return render(request, "graphs/index.html", {
        "graph": plot_fig
    })
