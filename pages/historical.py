import dash
from dash import html, dcc, Input, Output
import pandas as pd
import plotly.express as px

dash.register_page(__name__, path="/historical", name="Historical")

# Load the historical data from CSV
df = pd.read_csv("data/historical_results.csv")

layout = html.Div(className="page-container", children=[
    html.H3("Historical Test Execution Results"),

    dcc.Dropdown(
        id="env-dropdown",
        options=[{"label": "All", "value": "All"}] +
                [{"label": env, "value": env} for env in df["Environment"].unique()],
        value="All",
        style={"width": "300px"}
    ),

    dcc.Graph(id="historical-chart")
])


@dash.callback(
    Output("historical-chart", "figure"),
    Input("env-dropdown", "value")
)
def update_chart(selected_env):
    if selected_env == "All":
        filtered = df.copy()
    else:
        filtered = df[df["Environment"] == selected_env]

    fig = px.bar(
        filtered,
        x="Date",
        y=["Passed", "Failed"],
        color_discrete_map={"Passed": "#3CB850", "Failed": "#E40046"},
        barmode="group",
        text_auto=True,
        title=f"Daily Test Results - {selected_env if selected_env != 'All' else 'All Environments'}"
    )

    fig.update_layout(xaxis_title="Date", yaxis_title="Number of Test Cases")
    return fig
