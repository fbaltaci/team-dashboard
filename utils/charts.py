from dash import dcc, html
import plotly.graph_objects as go
from dash import dash_table


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
    fig.update_layout(title="Test Case Results")

    return dcc.Graph(figure=fig)


def get_summary_table(df):
    return dash_table.DataTable(
        data=df.to_dict("records"),
        columns=[{"name": i, "id": i} for i in df.columns],
        style_table={"overflowX": "auto"},
        style_cell={"textAlign": "center"},
        page_size=50
    )
