import pandas as pd 
import dash 
import plotly.express as px 
import dash_bootstrap_components as dbc 
import plotly.graph_objects as go 
from  dash import dcc,html,dash_table 
from dash.dependencies import Output,Input
from app import app
from df import df
from dash.exceptions import PreventUpdate


config_graph={"displayModeBar": False, "showTips": False}

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

imagenes={
           "Peru":'/assets/Peru.png',
           "Chile": '/assets/Chile.png',
           "Ecuador": '/assets/Ecuador.png',
           "Colombia": '/assets/Colombia.png', 
           "Paraguay": '/assets/Paraguay.png',
           "Argentina": '/assets/Argentina.png',
           "Bolivia":'/assets/Bolivia.png'                          
}


meses_espanol = {
    1: 'Ene',
    2: 'Feb',
    3: 'Mar',
    4: 'Abr',
    5: 'May',
    6: 'Jun',
    7: 'Jul',
    8: 'Ago',
    9: 'Sep',
    10: 'Oct',
    11: 'Nov',
    12: 'Dic'
}


df_temp=df.copy()
grupo5=df_temp.groupby(["Año","Mes"])[["Ventas","Utilidad"]].sum().reset_index()


grupo3=df_temp.groupby(["Año","Region"])["Ventas"].sum().reset_index()




años=[{"label":x,"value":x}for x in sorted(grupo5["Año"].unique())]

list_year=[{"label":x,"value":x}for x in sorted(grupo3["Año"].unique())]

layout=dbc.Container([
                dbc.Row([
                      dbc.Col([
                            dcc.Markdown("""
                                             **Paginas / Graficos de Ventas**  
                                               Graficos Paises
                                          """,style={"margin-left":"48px"})
                      ], xs=12, sm=12, md=9),
                      dbc.Col([
                           dbc.Row([
                                dbc.Col([
                                     dbc.Button(
                                          html.I(className="fas fa-user-alt", style={"color": "black","margin-left":"-8px"}),
                                          id="prof", style={"background-color": "transparent","width":"25px"}
                                     ),
                                     dbc.Popover([
                                           dbc.PopoverHeader("Perfil Usuario"),
                                           dbc.PopoverBody([
                                           html.Label("Datos"),
                                           dbc.Row([
                                                 dbc.Col(html.H6("Usuario", style={"font-size": "13px"}), md=4),
                                                 dbc.Col(html.H6("Luis Lopez CHavez", style={"font-size": "13px"}))
                                            ]),
                                           dbc.Row([
                                                dbc.Col(html.H6("Area", style={"font-size": "13px"}), md=4),
                                                dbc.Col(html.H6("Tesoreria", style={"font-size": "13px"}))
                                            ]),
                                            dbc.Row([
                                                 dbc.Col(html.H6("Email", style={"font-size": "13px"}), md=4),
                                                 dbc.Col(html.H6("luisalbertt22@gmail.com", style={"font-size": "13px"}))
                                            ]),
                                            dbc.Row([
                                                dbc.Col(html.H6("Celular", style={"font-size": "13px"}), md=4),
                                                dbc.Col(html.H6("993705286", style={"font-size": "13px"}))
                                            ]),
                                            dbc.Button("cerrar", id="borrar", color="danger", className="mt-2", size="sm")
                                             ])
                                     ], id="popover1", target="prof", is_open=False, placement='bottom', trigger="focus", style={"width": "320px"})
                                 ], xs=2, sm=2, md=1),
                                 dbc.Col([
                                       html.Label("    Sign Out", style={'font-weight': 'bold', "font-size": "13px", "margin-top": "13px"})
                                 ], xs=4, sm=4, md=3),
                                 dbc.Col([
                                      dbc.Button(
                                             html.I(className="fas fa-cog", style={"color": "black","margin-left":"-8px"}),
                                             id="icono", style={"background-color": "transparent","width":"25px"}
                                       ),
                                      dbc.Popover([
                                           dbc.PopoverHeader("Tema"),
                                           dbc.PopoverBody([
                                           dbc.Label("Selecciona un Tema"),
                                           dcc.RadioItems(
                                                    id="seleccion",
                                                    options=[{"label": "Claro", "value": "Claro"}, {"label": "Oscuro", "value": "Oscuro"}],
                                                    value="Claro",
                                                    labelStyle={"display": "block"}
                                           ),
                                           dbc.Button("cerrar", id="borrar", color="danger", className="mt-2", size="sm")
                                          ])
                                      ], id="popover2", target="icono", is_open=False, placement='bottom')
                                 ], xs=3, sm=3, md=2),
                                 dbc.Col([
                                      dbc.Button(
                                            html.I(className="fas fa-bell", style={"color": "black","margin-left":"-8px"}), id="historial",
                                            style={"background-color": "transparent","width":"25px"}
                                      ),
                                      dbc.Popover([
                                             dbc.PopoverHeader("Historial"),
                                             dbc.PopoverBody(
                                                           "Ultimas Actualizacion"
                                             )
                                     ], id="popover4", target="historial", trigger="focus", placement="bottom", is_open=False)
                                 ], xs=3, sm=3, md=3)
                           ])
                      ])         
                ], style={"margin-top": "10px"}),
           
           #----------------------------------graficos lines-NAV-DROP
           
                dbc.Row([
                     dbc.Col([
                         dcc.Graph(
                                id="lineas",
                                style={"width": "100%","height":"420px",'borderRadius': '18px', 'overflow': 'hidden','border': '1px solid #D6D4D3',"margin-left":"10px"}
                          ),
                   
            
                         dbc.Row([
                             dbc.Col([
                         
                                 dcc.Graph(
                                      id="variacion",
                                      style={"height":"20px","widt":"100%"},
                                      config=config_graph                                                    
                                  ),
                           ],sm=12,xs=12,md=4) ,
                          dbc.Col([
                                html.P("")
                          ],sm=12,xs=12,md=3),

                           dbc.Col([
                                dbc.Card([
                                     dbc.Nav([
                                        dbc.NavLink("venta",id="vtas",n_clicks=0,href="#",style={"width":"48%","font-size":"14px"}),
                                         dbc.NavLink("Utilidad",id="util",n_clicks=0,href="#",style={"width":"52%","font-size":"14px"})
                                     ],pills=True)
                                 ],style={"margin-top":"-6px","width":"95%","margin-left":"30px"}),
             
                           ],md=2,sm=7,xs=7) ,
                    
                           dbc.Col([
            
                              dcc.Dropdown(
                                  id="lista_años",
                                  multi=False,
                                  clearable=False,
                                  options=años,
                                  value="2009",
                                  style={"margin-top":"-6px","width":"100%","height":"40px","font-size":"17px",'borderRadius': '15px'}
                    
                            ),
                           
                            ],md=1,sm=4,xs=4,align="center")    
                         ],style={"margin-top":"-357px"})
                   
                    ],sm=12,xs=12,md=12),
               
               
                ],style={"margin-top":"25px"}),
                 
          
           
           
           #--------------------------------------
           
                dbc.Row([
                    dbc.Col([
                       dcc.Graph(
                             id="envios",style={"height":"435px","margin-top":"-20px"}
                       )
                     ],md=5), 
               
         #-----------------------  
               
               dbc.Col([
                  dbc.Card([
                      dbc.Row([
                          dbc.Col([
                              html.Legend("Ventas Globales por Ubicaciones Principales",
                                         style={"margin-top":"20px","margin-left":"45px","font-size":"21px","color":"#504E4E","font-family":"Courier New, Courier, monospace"})
                              
                          ],md=7,sm=7,xs=8),
                          
                          dbc.Col([
                                dcc.Dropdown(
                                 id="years",
                                 multi=False,
                                 options= list_year,
                                 persistence=True,
                                 clearable=False,
                                 value="2009",
                                 style={"width":"85px","margin-top":"20px",'borderRadius': '15px'}
                                 
                                 )  
                          ],md=4,sm=4,xs=4),
                       ]),
                      html.Hr(),   
                      
                      dbc.Row([
                          dbc.Col([
                                  html.Div(
                                           id="imagenes",style={'display': 'flex', 'flex-direction': 'column',"height":"100%",'width': '100%'}
                                  )
                          ],md=3,sm=4,xs=4),
                          dbc.Col([
                                    dash_table.DataTable(
                                         id="tabla_paises",
                                         columns=[{"name":col,"id":col}for col in ["Region","Ventas","porcentaje"]],
                                         data=grupo3.to_dict("records"),
                                         style_table={  
                                                       'overflowX': 'auto',  
                                                       'width': '100%',  
                                                       'height': '420px',
                                                       "margin-left":"-40px",
                                                       "margin-top":"-40px"
                                                       
                                           },  
                                           style_cell={
                                            'padding': '15px', 
                                            'borderRight': '0px',  # Esto elimina específicamente las líneas verticales
                                            'textAlign': 'center',
                                            'border': 'none' , # Elimina todas las líneas alrededor de las celdas
                                             
                                          
                                           },
                                            style_header={
                                              'display': 'none'  # Oculta el encabezado
                                            }
                                    
                                     )
                          ],md=9,sm=7,xs=7)        
                      ])
                   ],style={"width":"100%","height":"100%"}) 
               ],md=6)
            
           ],style={"margin-top":"350px"}) ,
           
           
            #----------------------------------------------------
                               
           dbc.Row([
              dbc.Col([
                  dcc.Markdown(  
                               '''                                  
                                   _© 2024, hecho con **Dash-Plotly** para una mejor web. _
                               ''',style={"margin-top":"60px"}
                               )
              ],md=10),
              dbc.Col([
                  
                   html.A(
                       html.Img(src="/assets/wasa.png", alt="WhatsApp", id="whatsapp-img", style={"height": "115px"}),
                        href="javascript:void(0);",  # Enlace vacío inicialmente
                        id="whatsapp-button",
                        style={
                           "position": "fixed",
                           "bottom": "10px",
                          "right": "20px",
                         "z-index": 999,
                          },
                    ),

    # Ventana emergente (inicialmente oculta)
                    html.Div(
                        id="whatsapp-button-display",
                        style={
                         "display": "none",  # Inicialmente oculta
                         "position": "fixed",
                         "bottom": "20px",
                         "right": "40px",
                         "width": "340px",
                        "background-color": "white",
                        "border": "1px solid #ccc",
                        "box-shadow": "0 2px 10px rgba(0,0,0,0.1)",
                       "z-index": 1000,
                       "padding": "10px",
                       "border-radius": "20px",
                       "height":"250px"
                     },
                     children=[
                         dbc.Card(
                         html.H1("¡Bienvenido!", style={"font-size": "20px","textAlign": "center","margin-top":"20px"}),
                         style={"height":"70px","margin-top":"-20px","width":"335px","margin-left":"-10px",'background-color': '#35CC13',"color":"white"}
                          ),
          
                
                          html.P("¡Hola!, Mi Nombres es Luis",style={"font-size": "18px","margin-top":"20px",'font-weight':'bold'}),
                          html.P("• ¿En qué puedo ayudarte?",style={"font-size": "18px","margin-top":"40px","margin-top":"-20px"}),
                          html.A(
                            html.Button("Abrir Chat", style={"background-color": "#35CC13", "color": "white",'font-weight':'bold',"padding": "6px 22px","border-radius": "20px","margin-top":"40px","margin-left":"80px"}),
                            href="https://wa.me/993705286",  # Reemplaza con tu número de WhatsApp
                            target="_blank",
                          ),
                          html.Button("Cerrar", id="close-chat", style={"margin-top": "10px","padding": "6px 22px","border-radius": "20px"})
                         ]
                     ),
                  
                  
              ],md=2)
          ])                               
                                       
                 
],fluid=True,style={"margin-top":"-50px"})
@app.callback(
    [Output("lineas", "figure"),
     Output("variacion","figure"),
     Output("vtas", "active"),
     Output("util", "active")],
    [Input("lista1","value"),
     Input("lista2","value"),
     Input("lista3","value"),
     Input("lista_años", "value"),
     Input("vtas", "n_clicks"),
     Input("util", "n_clicks")]
)
def actualizar_grafico(value1,value2,value3,año, clicks_ventas, clicks_utilidad):
    df_temp=df.copy()

    
    if value1:
        df_temp=df_temp[df_temp["Subcategoria"].isin(value1)]
    
    if value2:
        df_temp=df_temp[df_temp["Empaque"].isin(value2)]
    
    if value3:
        df_temp=df_temp[df_temp["Region"].isin(value3)]
        
        
    grupo1=df_temp.groupby(["Año","Mes"])[["Ventas","Utilidad"]].sum().reset_index()
    grupo1["Meses"]=grupo1["Mes"].map(meses_espanol)
    grupo1["Año"] = grupo1["Año"].astype(int)  # Aseguramos que la columna "Año" es de tipo entero
        
    
    año = int(año)
    filtrado_años = grupo1[grupo1["Año"] == año]
    filtrado_años2 = grupo1[grupo1["Año"] == (año - 1)]
    
    venta_total= filtrado_años["Ventas"].sum()
    venta_total2=filtrado_años2["Ventas"].sum()
   
    utilidad_total=filtrado_años["Utilidad"].sum()
    utilidad_total2=filtrado_años2["Utilidad"].sum()
    
    
    # Inicializar la figura
    figura = go.Figure()
    fig=go.Figure()
    # Determinar qué gráfico mostrar y cuál NavLink está activo
    if int(clicks_ventas) > int(clicks_utilidad):
        figura.add_trace(go.Scatter(x=filtrado_años["Meses"], y=filtrado_años["Ventas"], mode="lines+markers",name=f"{año}",line_shape="spline",line=dict(width=3,color="#AF3FEB"), marker=dict(size=9),hovertemplate= "%{y:,.2f}"))
        figura.add_trace(go.Scatter(x=filtrado_años2["Meses"], y=filtrado_años2["Ventas"], mode="lines+markers",name=f"{año-1}",line_shape="spline",line=dict(width=3,dash='dot'), marker=dict(size=9),hovertemplate= "%{y:,.2f}"))
        figura.update_layout(main_config,plot_bgcolor="white",showlegend=False,title={'text': f'<b style="color: #888787;font-size: 16px;">Informacion de Venta<br>{año}</b>','y':0.92})
        figura.update_yaxes(domain=[0, 0.70])# espacio titulo y grafico barra
        fig.add_trace(go.Indicator(
                           mode="number+delta",
                           value=venta_total,
                           delta={
                               "reference":venta_total2,
                                "relative":True,
                                "valueformat":".2%",
                                "position":"right",
                                "increasing":{"color":"green"},
                                "decreasing":{"color":"red"},
                                 "font": {"size": 14}
                           },
                           
                           number={"valueformat":",.0f","prefix":"S/","font": {"size": 23}},
                         
        ))
        
        active_vtas = True
        active_util = False
    else:
        figura.add_trace(go.Scatter(x=filtrado_años["Meses"], y=filtrado_años["Utilidad"], mode="lines+markers",name=f"{año}",line_shape="spline",line=dict(width=3), marker=dict(size=9),hovertemplate= "%{y:,.2f}"))
        figura.add_trace(go.Scatter(x=filtrado_años2["Meses"], y=filtrado_años2["Utilidad"], mode="lines+markers",name=f"{año-1}",line_shape="spline",line=dict(width=3,dash='dot'), marker=dict(size=9),hovertemplate= "%{y:,.2f}"))
        figura.update_layout(main_config,plot_bgcolor="white",showlegend=False,title={'text': f'<b style="color: #888787;font-size: 16px;">Informacion de Utilidad<br>{año}</b>','y':0.92})
        figura.update_yaxes(domain=[0, 0.70])# espacio titulo y grafico barra
        fig.add_trace(go.Indicator(
                           mode="number+delta",
                           value=utilidad_total,
                           delta={
                               "reference":utilidad_total2,
                                "relative":True,
                                "valueformat":".2%",
                                "position":"right",
                                "increasing":{"color":"green"},
                                "decreasing":{"color":"red"},
                                 "font": {"size": 14}
                           },
                        
                           number={"valueformat":",.0f","prefix":"S/","font": {"size": 23}},
                          
        ))
        
        
        active_vtas = False
        active_util = True
    
    # Devolver la figura y el estado activo de los NavLink
    return figura,fig, active_vtas, active_util
    
@app.callback([Output("tabla_paises","data"),
               Output("envios","figure"),
               Output("imagenes","children")],
              [Input("lista1","value"),
               Input("lista2","value"),
               Input("lista3","value"),
               Input("years","value")]
            
              ) 

def upadte_graph(value1,value2,value3,añitos):
    
    df_temp=df.copy()
    
    if value1:
        df_temp=df_temp[df_temp["Subcategoria"].isin(value1)]
    
    if value2:
        df_temp=df_temp[df_temp["Empaque"].isin(value2)]
    
    if value3:
        df_temp=df_temp[df_temp["Region"].isin(value3)]
    
    
    grupo2=df_temp.groupby(["Año","Region"])["Ventas"].sum().reset_index()
    ventas_año=grupo2.groupby("Año")["Ventas"].sum()

    grupo2["porcentaje"]=((grupo2["Ventas"]/ventas_año[grupo2["Año"]].values)*100).round(2)

    grupo2["imagen"]=grupo2["Region"].map(imagenes)
    
    #--tabla------
    tabla=grupo2[grupo2["Año"]==añitos].copy()
    tabla["Ventas"]=tabla["Ventas"].apply(lambda x: f"{x:,.2f}")
    tabla["porcentaje"]=tabla["porcentaje"].apply(lambda x : str(x)+ "%")
    
    ##----circulo----
    envio_pais=df_temp.groupby(["Año","Region"])["Id"].count().reset_index()
    envio_total=envio_pais[envio_pais["Año"]==añitos]
    total_año=envio_total["Id"].sum()
    total_año_formateado = "{:,}".format(total_año)
    
    pais_envio=go.Figure()
    pais_envio.add_trace(go.Pie(labels=envio_pais[envio_pais["Año"]==añitos]["Region"],values=envio_pais[envio_pais["Año"]==añitos]["Id"],hole=0.96,textfont=dict(color="black")))
    pais_envio.update_layout(main_config,showlegend=False)
    pais_envio.update_layout(title={"text":f"<b> Envios Totales por Pais <br> {añitos}</b>"})
    pais_envio.update_layout(margin={"t": 170, "b": 0, "l": 0, "r": 0})  # Ajusta los valores según lo que desees en grafico pastel
    pais_envio.update_layout(
                              annotations=[
                                    dict(
                                         text=str(total_año_formateado),
                                         x=0.5,
                                         y=0.55,
                                         font=dict(color="black"),
                                         showarrow=False,
                                         font_size=25
                                    ),
                                    dict(
                                        text= "Envios Total",
                                        x=0.5,
                                        y=0.45,
                                        font=dict(color="green"),
                                        showarrow=False,
                                        font_size=16
                                    )  
                                      
                                    
                              ]
                              
    )
    
    #......imagenss
    banderas=tabla["imagen"].apply(lambda x: html.Img(src= x ,style={"width":"30%","margin-bottom":"15px","margin-top":"0px","margin-left":"50px","height":"9%"})).copy()
    
    
    return tabla.to_dict("records"),pais_envio,banderas

@app.callback(
    Output("whatsapp-button-display", "style"),  # Cambiar el identificador de salida
    [Input("whatsapp-button", "n_clicks"), Input("close-chat", "n_clicks")],
    [dash.dependencies.State("whatsapp-button-display", "style")]  # Asegurarse de utilizar el mismo identificador aquí
)
def toggle_chat(n1, n2, style):
    if n1 or n2:
        if style["display"] == "none":
            style["display"] = "block"
        else:
            style["display"] = "none"
    return style

 
    
