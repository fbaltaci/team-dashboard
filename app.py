import dash
import dash_bootstrap_components as dbc
from dash import html

app = dash.Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)
server = app.server

app.layout = html.Div([
    dbc.Navbar(
        color="dark",
        dark=True,
        className="navbar",
        children=[
            dbc.Container(fluid=True, children=[
                dbc.NavbarBrand("Team's Dashboard", href="/"),
                dbc.Nav([
                    dbc.NavItem(dbc.NavLink("Home", href="/", active="exact")),
                    dbc.NavItem(dbc.NavLink("Historical", href="/historical", active="exact")),
                    dbc.NavItem(dbc.NavLink("Logs", href="/logs", active="exact")),
                ], className="ms-auto", navbar=True)
            ])
        ]
    ),
    html.Div(className="p-4", children=[
        dash.page_container
    ])
])

if __name__ == "__main__":
    app.run(debug=True)
