import dash
import dash_bootstrap_components as dbc
from dash import html

app = dash.Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

app.title = "Team Dashboard"

app.layout = html.Div([
    dbc.NavbarSimple(
        brand="Team's Dashboard",
        brand_href="/",
        color="dark",
        dark=True,
        children=[
            dbc.NavItem(dbc.NavLink("Home", href="/")),
            dbc.NavItem(dbc.NavLink("Historical", href="/historical")),
            dbc.NavItem(dbc.NavLink("Logs", href="/logs")),
        ]
    ),
    html.Div(className="p-4", children=[
        dash.page_container
    ])
])

if __name__ == "__main__":
    app.run(debug=True)
