import dash
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.express as px 
from dash.dependencies import Output,Input
from dash import dcc,html,dash_table
import plotly.graph_objects as go
from app import app
from df import df

dfz=df.copy()

card_style = {
    'borderBottom': '4px solid #9D9391',  # Cambia el color a un tono más oscuro aquí
    'borderRadius': '15px',  # Opcional: ajusta la curvatura del borde
}

meses_espanol = {
    1: 'Enero',
    2: 'Febrero',
    3: 'Marzo',
    4: 'Abril',
    5: 'Mayo',
    6: 'Junio',
    7: 'Julio',
    8: 'Agosto',
    9: 'Septiembre',
    10: 'Octubre',
    11: 'Noviembre',
    12: 'Diciembre'
}

main_config = {
    "hovermode": "x unified",
    "hoverlabel": {
        "bgcolor": "rgba(0,0,0,0.5)",
        "font": {"color": "white"}
    },
    "legend": {
        "yanchor":"top", 
        "y":0.9, 
        "xanchor":"left",
        "x":0.1,
        "title": {"text": None},
        "font" :{"color":"white"},
        "bgcolor": "rgba(0,0,0,0.5)"
    },
    "margin": {"l":30, "r":30, "t":30, "b":30}
}

# Definir un diccionario de colores para cada categoría
colores_categorias = {
    'Tecnologia': 'blue',
    'Muebles': 'green',
    'Elementos de oficina': 'red',
    # Añade más categorías y sus colores correspondientes aquí
}
agrupado=dfz.groupby(["Año","Mes","Segmento","Categoria"])["Ventas"].sum().reset_index()
agrupado["Meses"]=agrupado["Mes"].map(meses_espanol)


month=[{"label":x,"value":x}for x in agrupado["Meses"].unique()]


layout=dbc.Container([
         dbc.Card([
             dbc.CardBody([
                   dbc.Row([
                        dbc.Col([
                              dcc.Graph(
                                    id="barra",
                                     style={"height":"320px",'borderRadius': '15px', 'overflow': 'hidden',"width":"160%"}
                              ),
                         ],md=8,xs=8,sm=8),   
                        dbc.Col([   
                              dcc.Dropdown(
                                  id="lista",
                                  clearable=False,
                                  style={"width":"100px",'borderRadius': '15px',"margin-top":"10px"},
                                  options=month,
                                  persistence=True,
                                  value="Enero"
                                
                              )
                           
                       
                        ],md=4)
                   ])
              ])
          ],style={"height":"390px","width":"100%"})    
              
])

@app.callback(Output("barra","figure"),
              Input("lista","value")
              )

def actualizar_barra(valores):
    
    filter_table=agrupado[(agrupado["Año"]==agrupado["Año"].max())&(agrupado["Meses"]==valores)]
     
     
    figura=go.Figure() 
    for segmento in  filter_table["Segmento"].unique():
        dfsegmento=filter_table[filter_table["Segmento"]==segmento]
        for categoria in dfsegmento["Categoria"].unique():
            dfcategoria=dfsegmento[dfsegmento["Categoria"]==categoria]
            # Usar el diccionario de colores para asignar el color de la categoría
            color = colores_categorias.get(categoria, 'grey')  # 'grey' es el color por defecto si la categoría no está en el diccionario
            
            figura.add_trace(go.Bar(x=[segmento],y=dfcategoria["Ventas"],name=categoria,marker_color=color,hovertemplate= "%{y:,.2f}"))   
            
            figura.update_layout(main_config,barmode="stack",showlegend=False)   
            figura.update_yaxes(showgrid=False) # borra cuadricula del interior del grafico
            figura.update_layout(plot_bgcolor="#F7B329",paper_bgcolor="#F7B329",title={'text': '<b style="color: white;">Segmento<br>2022</b>','y':0.92})
            figura.update_yaxes(domain=[0, 0.85])# espacio titulo y grafico barra
            
            
            
    return figura         