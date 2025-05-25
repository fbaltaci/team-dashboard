import dash
from dash import html, dcc, Input, Output
import pandas as pd
import plotly.express as px

dash.register_page(__name__, path="/historical", name="Historical")

environments = ["dev", "qa", "preprod", "prod"]
dfs = []

for env in environments:
    df_env = pd.read_csv(f"data/historical_results/historical_results_{env}.csv")
    df_env["Environment"] = env.upper()
    dfs.append(df_env)

df = pd.concat(dfs, ignore_index=True)

layout = html.Div(className="page-container", children=[
    html.H3(id="historical-page-header", children="Historical Test Execution Results"),
    html.Div([
        dcc.Tabs(
            id="environment-tabs",
            value="DEV",
            children=[
                dcc.Tab(label=env.upper(), value=env.upper()) for env in environments
            ]
        ),
    ], style={"margin-bottom": "20px"}),

    html.Div([
        html.Label(id="tenant-dropdown-label", children="Select Tenant"),
        dcc.Dropdown(
            id="tenant-dropdown",
            options=[{"label": "All", "value": "All"}] +
                    [{"label": tenant, "value": tenant} for tenant in df["Tenant"].unique()],
            value="All",
            style={"width": "300px"}
        ),
    ]),

    dcc.Graph(id="historical-chart")
])


@dash.callback(
    Output("tenant-dropdown", "options"),
    Input("environment-tabs", "value")
)
def update_tenant_dropdown(selected_env):
    filtered_df = df[df["Environment"] == selected_env]
    tenant_options = [{"label": "All", "value": "All"}] + [
        {"label": tenant, "value": tenant} for tenant in sorted(filtered_df["Tenant"].unique())
    ]
    return tenant_options


@dash.callback(
    Output("historical-chart", "figure"),
    Input("environment-tabs", "value"),
    Input("tenant-dropdown", "value")
)
def update_chart(selected_env, selected_tenant):
    filtered = df[df["Environment"] == selected_env]

    if selected_tenant != "All":
        filtered = filtered[filtered["Tenant"] == selected_tenant]

    chart_title = f"Daily Test Results - {selected_env} - {selected_tenant if selected_tenant != 'All' else 'All Tenants'}"

    fig = px.bar(
        filtered,
        x="Date",
        y=["Passed", "Failed"],
        color_discrete_map={"Passed": "#3CB850", "Failed": "#E40046"},
        barmode="group",
        text_auto=True
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Number of Test Cases",
        annotations=[
            dict(
                text=chart_title,
                showarrow=False,
                xref="paper",
                yref="paper",
                x=0.5,
                y=-0.25,
                xanchor="center",
                yanchor="top",
                font=dict(size=16)
            )
        ],
        margin=dict(b=100)
    )

    return fig
