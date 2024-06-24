import dash
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.express as px 
from dash.dependencies import Output,Input
from dash import dcc,html,dash_table
import plotly.graph_objects as go
from app import app
from df import df
from xlwings import view  # para convertir  tu  arhcivo a excel con wiew

dfz=df.copy()


#----------------- variacion de pedidos
grupo1=dfz.groupby(["Año","Mes"])["Id"].count().reset_index()
grupo1["var"]=(grupo1["Id"].pct_change()*100).round(2)
var_pedidos=grupo1.iloc[len(grupo1)-1,3]

#----------------- venta total del mes actual
grupo2=dfz.groupby(["Año","Mes"])["Ventas"].sum().reset_index()
vtas_mes=grupo2.iloc[len(grupo2)-1,2]

#----------------- cantidad de pedidos este mes
grupo3=dfz.groupby(["Año","Mes"])["Id"].count().reset_index()
cat_pedido_mes=grupo3.iloc[len(grupo3)-1,2]

#----------------- categoria mas vendida

grupo4=dfz.groupby(["Año","Mes","Categoria"])["Ventas"].sum().reset_index()
catg_vendida=grupo4[(grupo4["Año"]==grupo4["Año"].max())&(grupo4["Mes"]==grupo4["Mes"].max())]
catg_vendida2=catg_vendida[catg_vendida["Ventas"]==catg_vendida["Ventas"].max()]["Categoria"].reset_index()
catg_vendida3=catg_vendida2.iloc[0,1]

#----------------- nuevo cliente este mes
orden_fecha=dfz.sort_values("Fecha_envio")
orden_fecha["contar_clientes_nuevos"]=orden_fecha.duplicated(subset=["Nombre_cliente"],keep="first").astype(int)
orden_fecha["contar_clientes_nuevos"]=1-orden_fecha["contar_clientes_nuevos"]
grupo5=orden_fecha.groupby(["Año","Mes"])["contar_clientes_nuevos"].sum().reset_index()
cliente_nuevos=grupo5.iloc[len(grupo5)-1,2]






layout=dbc.Container([     
           dbc.Card([
               dbc.CardBody([
                   dbc.Card([
                       dbc.Row([
                           dbc.Col(
                               html.I(className="fas fa-tags",style={"font-size":"25px","margin-top":"10px","margin-left":"10px","color":"orange"})
                           ,md=2,xs=2,sm=2),
                          dbc.Col([
                               html.H6("Variacion % de pedidos"),
                               html.Label(f"{var_pedidos}% este mes")
                                        
                          ],md=10,xs=10,sm=10)
                                    
                        ],style={"margin-top":"10px"})
                     ]),
                    dbc.Card([
                       dbc.Row([
                           dbc.Col(
                               html.I(className="fas fa-bell",style={"font-size":"25px","margin-top":"10px","margin-left":"10px","color":"blue"})
                           ,md=2,xs=2,sm=2),
                          dbc.Col([
                               html.H6("Venta Total actual"),
                               html.Label(f"{vtas_mes:,.2f} este mes")
                                        
                          ],md=10,xs=10,sm=10)
                                    
                        ],style={"margin-top":"10px"})
                     ],style={"margin-top":"12px"}),
                     dbc.Card([
                       dbc.Row([
                           dbc.Col(
                               html.I(className="fas fa-cart-arrow-down",style={"font-size":"25px","margin-top":"10px","margin-left":"10px","color":"green"})
                           ,md=2,xs=2,sm=2),
                          dbc.Col([
                               html.H6("Cantidad de Pedidos"),
                               html.Label(f"{cat_pedido_mes} este mes")
                                        
                          ],md=10,xs=10,sm=10)
                                    
                        ],style={"margin-top":"10px"})
                     ],style={"margin-top":"12px"}),
                    dbc.Card([
                       dbc.Row([
                           dbc.Col(
                               html.I(className="fas fa-cart-arrow-down",style={"font-size":"25px","margin-top":"10px","margin-left":"10px","color":"red"})
                           ,md=2,xs=2,sm=2),
                          dbc.Col([
                               html.H6("Categoria mas Vendida"),
                               html.Label(f"{catg_vendida3} este mes")
                                        
                          ],md=10,xs=10,sm=10)
                                    
                        ],style={"margin-top":"10px"})
                     ],style={"margin-top":"12px"}),
                     dbc.Card([
                       dbc.Row([
                           dbc.Col(
                               html.I(className="fas fa-credit-card",style={"font-size":"25px","margin-top":"10px","margin-left":"10px","color":"black"})
                           ,md=2,xs=2,sm=2),
                          dbc.Col([
                               html.H6("N° de Clientes nuevos"),
                               html.Label(f"{cliente_nuevos}este mes")
                                        
                          ],md=10,xs=10,sm=10)
                                    
                        ],style={"margin-top":"10px"})
                     ],style={"margin-top":"12px"})    
                   
                ])
            ])         
])

