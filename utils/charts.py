from dash import dcc
import plotly.graph_objects as go
from dash import dash_table
import pandas as pd


def get_pie_chart(df):
    total_passed = df["Passed"].sum()
    total_failed = df["Failed"].sum()
    total_untested = df["Untested"].sum()
    total_blocked = df["Blocked"].sum()

    fig = go.Figure(data=[go.Pie(
        labels=["Passed", "Failed", "Untested", "Blocked"],
        values=[total_passed, total_failed, total_untested, total_blocked],
        marker_colors=["#3CB850", "#E40046", "#FFC300", "#C0C0C0"]
    )])

    fig.update_layout(
        title=dict(
            text="Test Case Results",
            y=0.02,
            x=0.5,
            xanchor='center',
            yanchor='bottom'
        ),
        margin=dict(t=0, b=60)
    )

    return dcc.Graph(figure=fig)


def get_summary_table(df):
    df = df.copy()

    total_row = pd.DataFrame({
        "Test Suite": ["Total"],
        "Total": [df["Total"].sum()],
        "Passed": [df["Passed"].sum()],
        "Failed": [df["Failed"].sum()],
        "Untested": [df["Untested"].sum()],
        "Blocked": [df["Blocked"].sum()],
        "Pass %": [round((df["Passed"].sum() / df["Total"].sum()) * 100, 2) if df["Total"].sum() else 0.0]
    })

    df_with_total = pd.concat([df, total_row], ignore_index=True)

    return dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in df_with_total.columns],
        data=df_with_total.to_dict("records"),
        style_table={"overflowX": "auto"},
        style_cell={
            "textAlign": "center",
            "padding": "8px",
            "fontFamily": "Arial",
        },
        style_header={
            "backgroundColor": "#f1f1f1",
            "fontWeight": "bold"
        },
        style_data_conditional=[
            {
                "if": {"filter_query": '{Test Suite} = "Total"'},
                "backgroundColor": "#A9A9A9",
                "fontWeight": "bold"
            }
        ]
    )
