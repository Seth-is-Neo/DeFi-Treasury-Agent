# dashboard/dashboard.py
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

def get_df():
    try:
        df = pd.read_json("pool_data.json")
        df['roi'] = df['realized_profit'] / df['lp_allocation']
        return df
    except Exception as e:
        print("Error reading pool_data.json:", e)
        return pd.DataFrame()

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "AI Treasury Dashboard"

app.layout = dbc.Container([
    html.H1("AI Treasury Dashboard (Shadow Mode)"),
    dbc.Row([
        dbc.Col(dcc.Dropdown(
            id="chain-dropdown",
            options=[{"label": c, "value": c} for c in ["All", "Ethereum", "Polygon", "Hedera"]],
            value="All"
        ), width=3),
        dbc.Col(dcc.Dropdown(
            id="dex-dropdown",
            options=[{"label": d, "value": d} for d in ["All", "Uniswap", "SushiSwap", "HederaDEX"]],
            value="All"
        ), width=3)
    ]),
    dcc.Interval(id="interval-update", interval=5000, n_intervals=0),
    dcc.Graph(id="score-graph"),
    dcc.Graph(id="lp-graph"),
    dcc.Graph(id="vol-tvl-graph"),
    dcc.Graph(id="fees-graph"),
    dcc.Graph(id="il-profit-graph"),
    dcc.Graph(id="price-twap-graph"),
    dcc.Graph(id="roi-heatmap")
], fluid=True)

@app.callback(
    Output("score-graph","figure"),
    Output("lp-graph","figure"),
    Output("vol-tvl-graph","figure"),
    Output("fees-graph","figure"),
    Output("il-profit-graph","figure"),
    Output("price-twap-graph","figure"),
    Output("roi-heatmap","figure"),
    Input("interval-update","n_intervals"),
    Input("chain-dropdown","value"),
    Input("dex-dropdown","value")
)
def update_dashboard(n, chain_filter, dex_filter):
    df = get_df()
    if df.empty:
        return [{}]*7
    if chain_filter != "All": df = df[df.chain==chain_filter]
    if dex_filter != "All": df = df[df.dex==dex_filter]

    fig1 = px.bar(df, x="pair", y="bayesian_score", color="alert_flag", title="Pool Scores & Alerts")
    fig2 = px.bar(df, x="pair", y="lp_allocation", color="dex", title="LP Allocations per DEX")
    fig3 = px.line(df, x="pair", y=["volatility","tvl"], title="Volatility & TVL")
    fig4 = px.line(df, x="pair", y=["expected_fee","actual_fee"], title="Expected vs Actual Fees")
    fig5 = px.line(df, x="pair", y=["impermanent_loss","realized_profit"], title="Impermanent Loss vs Realized Profit")
    fig6 = px.line(df, x="pair", y="price_vs_twap", title="Price vs DEX TWAP")
    fig7 = px.imshow(df.pivot_table(index="chain", columns="pair", values="roi"), color_continuous_scale="Viridis", title="ROI Heatmap")
    
    return fig1, fig2, fig3, fig4, fig5, fig6, fig7

if __name__=="__main__":
    app.run(debug=True, port=8050)
