import pandas as pd
import dash
from dash import html, dcc, Input, Output
from utils.charts import get_pie_chart, get_summary_table

dash.register_page(__name__, path="/", name="Home")

env_files = {
    "Dev": [
        ("Tenant 1", "data/dev_results/tr_results_tenant_1_dev.csv"),
        ("Tenant 2", "data/dev_results/tr_results_tenant_2_dev.csv"),
        ("Tenant 3", "data/dev_results/tr_results_tenant_3_dev.csv"),
    ],
    "QA": [
        ("Tenant 1", "data/qa_results/tr_results_tenant_1_qa.csv"),
        ("Tenant 2", "data/qa_results/tr_results_tenant_2_qa.csv"),
        ("Tenant 3", "data/qa_results/tr_results_tenant_3_qa.csv"),
    ],
    "Preprod": [
        ("Tenant 1", "data/preprod_results/tr_results_tenant_1_preprod.csv"),
        ("Tenant 2", "data/preprod_results/tr_results_tenant_2_preprod.csv"),
        ("Tenant 3", "data/preprod_results/tr_results_tenant_3_preprod.csv"),
    ],
    "Prod": [
        ("Tenant 1", "data/prod_results/tr_results_tenant_1_prod.csv"),
        ("Tenant 2", "data/prod_results/tr_results_tenant_2_prod.csv"),
        ("Tenant 3", "data/prod_results/tr_results_tenant_3_prod.csv"),
    ],
}

layout = html.Div(className="page-container", children=[
    html.Div(className="dashboard-header", children=[
        dcc.Dropdown(
            id="env-dropdown",
            options=[{"label": env, "value": env} for env in env_files.keys()],
            value="Dev",
            clearable=False
        ),
    ]),
    html.Div(id="env-results-container")
])


@dash.callback(
    Output("env-results-container", "children"),
    Input("env-dropdown", "value")
)
def update_dashboard(env):
    tenant_data = env_files[env]
    components = []

    for tenant_name, file_path in tenant_data:
        try:
            df = pd.read_csv(file_path)
        except FileNotFoundError:
            continue

        section = html.Div(className="tenant-section", children=[
            html.H4(className="tenant-name", children=tenant_name),
            html.Div(className="responsive-row", children=[
                html.Div(className="chart-box", children=get_pie_chart(df)),
                html.Div(className="table-box", children=get_summary_table(df))
            ])
        ])
        components.append(section)

    return components
