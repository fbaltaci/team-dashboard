import dash
from dash import html, dcc, Input, Output

from utils.historical_utils import (
    load_historical_data,
    get_environment_tabs,
    get_tenant_options,
    build_historical_chart
)

dash.register_page(__name__, path="/historical", name="Historical")

df = load_historical_data()

layout = html.Div(className="page-container", children=[
    html.H3(id="historical-page-header", children="Historical Test Execution Results"),

    dcc.Tabs(
        id="environment-tabs",
        value="DEV",
        children=get_environment_tabs(),
        className="env-tabs",
        style={"margin-bottom": "20px"}
    ),

    html.Div([
        html.Label(id="tenant-dropdown-label", children="Select Tenant"),
        dcc.Dropdown(
            id="tenant-dropdown",
            value="All",
            style={"width": "300px"}
        ),
    ], className="tenant-dropdown-wrapper"),

    dcc.Graph(id="historical-chart")
])


@dash.callback(
    Output("tenant-dropdown", "options"),
    Input("environment-tabs", "value")
)
def update_tenant_dropdown(selected_env):
    return get_tenant_options(df, selected_env)


@dash.callback(
    Output("historical-chart", "figure"),
    Input("environment-tabs", "value"),
    Input("tenant-dropdown", "value")
)
def update_chart(selected_env, selected_tenant):
    return build_historical_chart(df, selected_env, selected_tenant)
