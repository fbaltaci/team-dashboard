import pandas as pd
import plotly.express as px

ENVIRONMENTS = ["dev", "qa", "preprod", "prod"]
DATA_DIR = "data/historical_results"
COLOR_MAP = {"Passed": "#3CB850", "Failed": "#E40046"}


def load_historical_data():
    frames = []
    for env in ENVIRONMENTS:
        df_env = pd.read_csv(f"{DATA_DIR}/historical_results_{env}.csv")
        df_env["Environment"] = env.upper()
        frames.append(df_env)
    return pd.concat(frames, ignore_index=True)


def get_environment_tabs():
    from dash import dcc
    return [dcc.Tab(label=env.upper(), value=env.upper()) for env in ENVIRONMENTS]


def get_tenant_options(df, environment):
    tenants = sorted(df[df["Environment"] == environment]["Tenant"].unique())
    return [{"label": "All", "value": "All"}] + [{"label": t, "value": t} for t in tenants]


def build_historical_chart(df, selected_env, selected_tenant):
    filtered = df[df["Environment"] == selected_env]
    if selected_tenant != "All":
        filtered = filtered[filtered["Tenant"] == selected_tenant]

    chart_title = f"Daily Test Results - {selected_env} - {selected_tenant if selected_tenant != 'All' else 'All Tenants'}"

    fig = px.bar(
        filtered,
        x="Date",
        y=["Passed", "Failed"],
        color_discrete_map=COLOR_MAP,
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
