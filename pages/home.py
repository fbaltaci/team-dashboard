import pandas as pd
import dash
from dash import html, dcc, Input, Output
from utils.charts import get_pie_chart, get_summary_table

dash.register_page(__name__, path="/", name="Home")

# Load and combine all test result CSVs
df_tenant_1 = pd.read_csv("data/tr_results_tenant_1.csv")
df_tenant_2 = pd.read_csv("data/tr_results_tenant_2.csv")
df_tenant_3 = pd.read_csv("data/tr_results_tenant_3.csv")

# Add 'Environment' column to each
df_tenant_1["Environment"] = "Tenant 1"
df_tenant_2["Environment"] = "Tenant 2"
df_tenant_3["Environment"] = "Tenant 3"

# Combine them
df = pd.concat([df_tenant_1, df_tenant_2, df_tenant_3], ignore_index=True)

layout = html.Div(className="page-container", children=[
    html.H2("Test Results Dashboard"),

    dcc.Tabs(
        id="suite-tabs",
        value="All",
        children=[
            dcc.Tab(label="All Results", value="All"),
            dcc.Tab(label="Tenant 1", value="Tenant 1"),
            dcc.Tab(label="Tenant 2", value="Tenant 2"),
            dcc.Tab(label="Tenant 3", value="Tenant 3"),
        ]
    ),

    html.Div(id="tab-content", style={"marginTop": "2rem"})
])


@dash.callback(
    Output("tab-content", "children"),
    Input("suite-tabs", "value")
)
def render_tab_content(selected):
    if selected == "All":
        filtered = df.copy()
    else:
        filtered = df[df["Environment"] == selected]

    return html.Div(className="pie-chart-row", children=[
        html.Div(get_pie_chart(filtered)),
        html.Div(get_summary_table(filtered))
    ])
