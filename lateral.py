import pandas as pd
import dash 
import plotly.express as px 
import dash_bootstrap_components as dbc 
import plotly.graph_objects as go
from dash import dcc,html,dash_table 
from dash.dependencies import Output,Input 
from app import app 
from df import df

layout= dbc.Container([
             dbc.Row([
                 dbc.Col([
                      dbc.Card([
                          dbc.Row([
                              dbc.Col([
                                   html.I(className="fas fa-th",style={"margin-left":"18px","font-size":"30px","color":"white","width":"100%"})
                              ],md=2,xs=2,sm=2),
                              dbc.Col([
                                  html.Label("Ventas Totales",style={"margin-left":"20px","font-size":"18px","color":"white","width":"100%"})
                              ],sm=8,xs=8)
                          ],style={"margin-top":"30px"}),
                          dbc.Row(
                              html.Legend("Filtros",style={"margin-left":"20px","font-size":"15px","color":"white"}),
                          style={"margin-top":"30px"}),
                          dbc.Row([
                              dbc.Col([
                                  html.I(className="far fa-dot-circle",style={"margin-left":"18px","font-size":"20px","color":"white","margin-top":"30px"})
                              ],md=3,xs=3,sm=3),
                              dbc.Col([
                                  html.Label("Productos",style={"margin-left":"20px","font-size":"15px","color":"white"}),
                                  dcc.Dropdown(
                                                id="lista1",
                                                multi=True,
                                                persistence=True,
                                                persistence_type="session",
                                                clearable=False,
                                                style={"width":"150px","font-size":"14px","height":"110px"}
                                  )
                              ])
                          ]),
                          dbc.Row([
                              dbc.Col([
                                  html.I(className="far fa-dot-circle",style={"margin-left":"18px","font-size":"20px","color":"white","margin-top":"30px"})
                              ],md=3,xs=3,sm=3),
                              dbc.Col([
                                  html.Label("Empaque",style={"margin-left":"20px","font-size":"15px","color":"white"}),
                                  dcc.Dropdown(
                                                id="lista2",
                                                multi=True,
                                                persistence=True,
                                                persistence_type="session",
                                                clearable=False,
                                                style={"width":"150px","font-size":"14px","height":"110px"}
                                  )
                              ])
                          ],style={"margin-top":"30px"}),
                          dbc.Row([
                              dbc.Col([
                                  html.I(className="far fa-dot-circle",style={"margin-left":"18px","font-size":"20px","color":"white","margin-top":"30px"})
                              ],md=3,xs=3,sm=3),
                              dbc.Col([
                                  html.Label("Pais",style={"margin-left":"20px","font-size":"15px","color":"white"}),
                                  dcc.Dropdown(
                                                id="lista3",
                                                multi=True,
                                                persistence=True,
                                                persistence_type="session",
                                                clearable=False,
                                                style={"width":"150px","font-size":"14px","height":"110px"}
                                  )
                              ])
                          ],style={"margin-top":"30px"}),
                          
                          dbc.Row([
                              dbc.Col([
                                  dbc.Nav([
                                      dbc.NavLink([html.I(className="fas fa-chart-bar"),"   Ventas Totales"],href="/grafico1",active="exact",style={"borderRadius": "15px"}),
                                      dbc.NavLink([html.I(className="fa fa-globe"),"   Ventas Paises"],href="/grafico2",active="exact",style={"borderRadius": "15px"})
                                  ],vertical=True,pills=True,id="nav-link",style={"width": "210px","margin-left":"10px","textAlign": "center"})
                              ])
                          ],style={"margin-top":"40px","width":"100%"})
                          
                          
                      ],style={"height":"780px","margin-left":"-20px","margin-top":"-20px","border-radius":"20px","width":"230px","background-color":"black"}),   
                 ])
               
                 
             ])
])
@app.callback(  Output("lista1","options"),
               [Input("lista2","value"),
                Input("lista3","value")]
             )
def actualizar_lsiat1(value_2,value_3):
    df_temp=df
    
    if value_2:
        df_temp=df_temp[df_temp["Empaque"].isin(value_2)]
    
    if value_3:
        df_temp=df_temp[df_temp["Region"].isin(value_3)]
    
    return [{"label":x,"value":x} for x in sorted(df_temp["Subcategoria"].unique())]

@app.callback(  Output("lista2","options"),
               [Input("lista1","value"),
                Input("lista3","value")]
             )
def actualizar_lsiat1(value_1,value_3):
    df_temp=df
    
    if value_1:
        df_temp=df_temp[df_temp["Subcategoria"].isin(value_1)]
    
    if value_3:
        df_temp=df_temp[df_temp["Region"].isin(value_3)]
    
    return [{"label":x,"value":x} for x in sorted(df_temp["Empaque"].unique())]

@app.callback(  Output("lista3","options"),
               [Input("lista1","value"),
                Input("lista2","value")]
             )
def actualizar_lsiat1(value_1,value_2):
    df_temp=df
    
    if value_1:
        df_temp=df_temp[df_temp["Subcategoria"].isin(value_1)]
    
    if value_2:
        df_temp=df_temp[df_temp["Empaque"].isin(value_2)]
    
    return [{"label":x,"value":x} for x in sorted(df_temp["Region"].unique())]

