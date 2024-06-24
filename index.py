import dash
from dash import dcc, html
from dash.dependencies import Output,Input,State
import dash_bootstrap_components as dbc
from app import app
import lateral, grafico1, grafico2

server=app.server

# Estilos para la barra lateral oculta
SIDEBAR_STYLE_HIDDEN = {
    "position": "fixed",
    "top": 0,
    "left": "-16rem",
    "width": "16rem",
    "height": "100%",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
    "transition": "all 0.5s",
    "z-index": "2"
}

# Estilos para la barra lateral visible
SIDEBAR_STYLE_VISIBLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "width": "16rem",
    "height": "100%",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
    "transition": "all 0.5s",
    "z-index": "2"
}

# Estilos para el contenido principal
CONTENT_STYLE = {
    "transition": "margin-left .5s",
    "padding": "2rem 1rem",
     "margin-top": "-25px"
}

CONTENT_STYLE_WITH_SIDEBAR = {
    "transition": "margin-left .5s",
    "padding": "1rem 1rem",
    "margin-left": "15rem",
    
}

app.layout = html.Div([
    dcc.Location(id="url", pathname="/grafico1"),
    html.Div(
        lateral.layout,  # Aquí se incluye el layout de la barra lateral definido en el módulo lateral
        id='sidebar',
        style=SIDEBAR_STYLE_HIDDEN
    ),
    html.Div(id="graficos", style=CONTENT_STYLE, children=[
        dbc.Button(html.I(className="fas fa-sliders-h",style={"color":"black"}), id='sidebar-toggle', n_clicks=0,style={"font-size":"19px","width":"205x", "height": "46px","background-color": "transparent"}),
        html.Div(id="content")
    ])
])

@app.callback(
    [Output('sidebar', 'style'), Output('graficos', 'style')],
    [Input('sidebar-toggle', 'n_clicks')],
    [State('sidebar', 'style')]
)
def toggle_sidebar(n, sidebar_style):
    if n % 2 == 0:
        # Barra lateral oculta
        sidebar_style = SIDEBAR_STYLE_HIDDEN
        content_style = CONTENT_STYLE
    else:
        # Barra lateral visible
        sidebar_style = SIDEBAR_STYLE_VISIBLE
        content_style = CONTENT_STYLE_WITH_SIDEBAR
    return sidebar_style, content_style

@app.callback(Output("content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/grafico1":
        return grafico1.layout
    elif pathname == "/grafico2":
        return grafico2.layout
    # Puedes continuar agregando más páginas aquí

if __name__== '__main__':
   app.run_server(port=8052,debug=True)