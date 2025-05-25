import dash
from dash import html, dcc, Input, Output
import os

dash.register_page(__name__, path="/logs", name="Logs")

LOG_DIR = "logs"
log_files = sorted([f for f in os.listdir(LOG_DIR) if f.endswith(".log")])
default_log = log_files[0] if log_files else None

layout = html.Div(className="page-container", children=[
    html.H3(id="logs-page-header", children="Execution Logs"),

    dcc.Dropdown(
        id="log-selector",
        options=[{"label": f, "value": f} for f in log_files],
        value=default_log,
        placeholder="Select a log file",
        style={"width": "300px", "marginBottom": "1rem"}
    ),

    html.Div(id="log-file-name", style={"marginBottom": "1rem", "fontWeight": "bold"}),

    html.Pre(id="log-content", style={
        "whiteSpace": "pre-wrap",
        "backgroundColor": "#f8f9fa",
        "padding": "1rem",
        "borderRadius": "8px",
        "maxHeight": "500px",
        "overflowY": "scroll",
        "fontSize": "0.9rem",
        "border": "1px solid #ddd"
    })
])


@dash.callback(
    Output("log-content", "children"),
    Output("log-file-name", "children"),
    Input("log-selector", "value")
)
def display_log(filename):
    if not filename:
        return "", ""

    path = os.path.join(LOG_DIR, filename)
    if not os.path.exists(path):
        return "Log file not found.", filename

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    return content, f"Showing: {filename}"
