import dash_bootstrap_components as dbc
from dash.dependencies import Output,Input
from dash import dcc,html,dash_table
from app import app
from df import df
import dash_ag_grid as dag
import pandas as pd



posicione=[
         "10 Primeros",
          "10 ultimos"
]
seleccion=[{"label":x,"value":x}for x in posicione]

dfx=df.copy()

layout=dbc.Container([
            dbc.Card([
                dbc.Row([
                    dbc.Col([
                      dash_table.DataTable(
                                  id="tabla-grid",
                                  columns=[{"name":columna,"id":columna}for columna in ["Nombre_cliente","Ventas"]],
                                  data=dfx.to_dict("records"),
                                  filter_action="native",
                              
                                  page_action="native",
                                  page_current=0,
                                  page_size=5,
                                  style_table={  
                                         'overflowX': 'auto',  
                                         'width': '100%',  
                                         'height': '300px',
                                         "margin-left":"10px",
                                         'border-radius': '20px',  # Establece el radio de los bordes
                                         
                                 }, 
                                  style_header={
                                         "height":"50px",
                                         "backgroundColor": "#46C22B",
                                         "color":"white",
                                         "font-size":"17px",
                                         'fontWeight': 'bold',
                                         'textAlign': 'center',
                                          'minWidth': '20px',
                                          
                                         
                                  },
                                  style_cell={
                                            'padding': '10px', 
                                            'borderRight': '0px',  # Esto elimina específicamente las líneas verticales
                                            'textAlign': 'center',
                                  }
                                  
                                  
                      )
                    ],md=8,sm=8,xs=8),
                    dbc.Col([
                        dcc.Dropdown(
                                      id="listas",
                                      multi=False,
                                      clearable=False,
                                      options=seleccion,
                                      style={"width":"85%","font-size":"12px","margin-top":"80px"},
                                     
                                     
                        )
                    ],md=4,xs=4,sm=4)   
                ],style={"margin-top":"30px"})
            ],style={"height":"395px","margin-left":"-10px","width":"105%"})
],fluid=True)

@app.callback(Output("tabla-grid","data"),
              Input("listas","value")
             )
def actulizar_grid(valor):
    
    
    agrupado=dfx.groupby(["Año","Mes","Nombre_cliente"])["Ventas"].sum().reset_index().copy()
    añomesmax=agrupado[(agrupado["Año"]==agrupado["Año"].max())&(agrupado["Mes"]==agrupado["Mes"].max())].copy()
   
    
    
    if valor=="10 Primeros":
          z=añomesmax.nlargest(10,"Ventas")[["Nombre_cliente", "Ventas"]]
          z["Ventas"]=z["Ventas"].apply(lambda x :f"{x:,.2f}")
          return z.to_dict('records')
    
    elif valor == "10 ultimos":
          x = añomesmax.nsmallest(10, "Ventas")[["Nombre_cliente", "Ventas"]]
          x["Ventas"]=x["Ventas"].apply(lambda x :f"{x:,.2f}")
          return x.to_dict('records')
    
      # Si no se selecciona ninguna opción, mostramos toda la tabla sin filtrar
    else:
          añomesmax["Ventas"] = añomesmax["Ventas"].apply(lambda x: f"{x:,.2f}")
          return añomesmax[["Nombre_cliente", "Ventas"]].to_dict('records')
    
    
  
  
   