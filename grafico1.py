import pandas as pd 
import dash 
import plotly.express as px 
import dash_bootstrap_components as dbc 
import plotly.graph_objects as go 
from  dash import dcc,html,dash_table,callback_context
from dash.dependencies import Output,Input
from app import app
from dash.exceptions import PreventUpdate
from githubupdate import filter_commits, get_commit_history
from df import df
import pagina1,pagina2,pagina3


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


card_style = {
    'borderBottom': '4px solid #9D9391',  # Cambia el color a un tono más oscuro aquí
    'borderRadius': '15px',  # Opcional: ajusta la curvatura del borde
}

layout=dbc.Container([
            dbc.Row([
                dbc.Col([
                     dcc.Markdown("""
                                    **Paginas / Graficos de Ventas**  
                                      Graficos
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
            ],style={"margin-top": "10px"}),
           
           
           
            dbc.Row([
                dbc.Col([
                    dbc.Card(
                        dbc.CardBody([                      
                            html.Label("Total Ventas", style={"margin-left": "110px"}),
                            html.Legend("Total Ventas", id="total_ventas", style={"margin-left": "70px", 'font-weight': 'bold'})                        
                        ]), style={"border-radius": "13px", "width": "238px", "margin-top": "35px"}
                     ),
                    dbc.Card(
                        dbc.CardBody(
                              html.I(className="fas fa-dollar-sign", style={"font-size": "40px", "margin-top": "-7px"})
                        ), style={"width": "60px", "margin-left": "10px", "border-radius": "13px", "height": "60px", "margin-top": "-115px"}
                     )
                ], xs=12, sm=12, md=6, lg=3, className="mb-4"),
        
                 dbc.Col([
                     dbc.Card(
                         dbc.CardBody([                      
                             html.Label("Total Utilidad", style={"margin-left": "110px"}),
                             html.Legend("Total Ventas", id="total_utilidad", style={"margin-left": "70px", 'font-weight': 'bold'})                        
                        ]), style={"border-radius": "13px", "width": "238px", "margin-top": "35px"}
                     ),
                     dbc.Card(
                          dbc.CardBody(
                          html.I(className="fas fa-university", style={"font-size": "40px", "margin-top": "-7px", "margin-left": "-5px"})
                          ), style={"width": "60px", "margin-left": "10px", "border-radius": "13px", "height": "60px", "margin-top": "-115px"}
                      )
                 ], xs=12, sm=12, md=6, lg=3, className="mb-4"),
        
                dbc.Col([
                   dbc.Card(
                       dbc.CardBody([                      
                            html.Label("Total Costo Envio", style={"margin-left": "76px"}),
                           html.Legend("Total Ventas", id="total_envio", style={"padding-left": "53px", 'font-weight': 'bold'})                        
                      ]), style={"border-radius": "13px", "width": "238px", "margin-top": "35px"}
                   ),
                   dbc.Card(
                        dbc.CardBody(
                            html.I(className="fas fa-truck", style={"font-size": "40px", "margin-top": "-7px", "margin-left": "-9px"})
                            ), style={"width": "60px", "margin-left": "10px", "border-radius": "13px", "height": "60px", "margin-top": "-115px"}
                   )
                ], xs=12, sm=12, md=6, lg=3, className="mb-4"),
        
                dbc.Col([
                     dbc.Card(
                         dbc.CardBody([                      
                              html.Label("Total Descuento", style={"margin-left": "75px"}),
                              html.Legend("123", id="total_descuento", style={"text-align": "left", "padding-left": "90px", 'font-weight': 'bold'})                        
                        ]), style={"border-radius": "13px", "width": "238px", "margin-top": "35px"}
                    ),
                    dbc.Card(
                          dbc.CardBody(
                               html.I(className="fas fa-money-check-alt", style={"font-size": "40px", "margin-top": "-7px", "margin-left": "-10px"})
                          ), style={"width": "60px", "margin-left": "10px", "border-radius": "13px", "height": "60px", "margin-top": "-115px"}
                     )
                 ], xs=12, sm=12, md=6, lg=3, className="mb-4")
           ], className="gx-4 gy-4"),
           
           
           
         
           
           dbc.Row([
               dbc.Col([
                   dbc.Card(
                      dbc.CardBody([
                           html.H5("Total Ventas")
                       ]), style={"height": "380px", "padding-top": "240px", "padding-left": "30px","margin-top":"60px", **card_style}
                   ),
                   dcc.Graph(id="barra1", style={"height": "250px", 'borderRadius': '15px', 'overflow': 'hidden', "width": "90%", "margin-left": "20px","margin-top":"-400px"})
               ], xs=12, sm=12, md=6, lg=4, className="mb-4"),

                dbc.Col([
                    dbc.Card(
                        dbc.CardBody([
                            html.H5("Total Utilidad")
                        ]), style={"height": "380px", "margin-top":"60px",**card_style}
                     ),
                     dcc.Graph(id="barra2", style={"height": "250px", 'borderRadius': '15px', 'overflow': 'hidden',"width": "90%", "margin-left": "20px","margin-top":"-400px"})
                ], xs=12, sm=12, md=6, lg=4, className="mb-4"),

               dbc.Col([
                     dbc.Card(
                          dbc.CardBody([
                          html.H5("Total Envio")
                          ]), style={"height": "380px","margin-top":"60px", **card_style}
                     ),
                     dcc.Graph(id="circulo", style={"height": "250px", 'borderRadius': '15px', 'overflow': 'hidden', "width": "90%", "margin-left": "20px","margin-top":"-400px"})
              ], xs=12, sm=12, md=6, lg=4, className="mb-4")
          ], style={"margin-top": "50px"}),
          
           
          dbc.Row([
               dbc.Col([
           
                dash_table.DataTable(
                    id="datatable-agrupada",
                    columns=[{"name": columna, "id": columna} for columna in ["Categoria", "Subcategoria", "Cantidad", "Ventas", "Utilidad"]],
                    data=df.to_dict("records"),
                    sort_action="native",
                    filter_action="native",
                    page_action="native",
                    page_current=0,
                    page_size=10,
                    style_header={  
                        'font-size': '16px',         
                        'fontWeight': 'bold',
                        'backgroundColor': 'black',
                        'color': 'white',
                        'minWidth': '20px',
                        'maxWidth': '100px',
                        'textAlign': 'center',
                        'maxheight': '27px',
                        'height': '48px'
                    },
                    style_cell={  
                        'padding': '5px',  
                        'text-align': 'center',  
                        'minWidth': '50px',  
                        'maxWidth': '100px',  
                        'overflow': 'hidden',  
                        'textOverflow': 'ellipsis'
                    },
                    style_table={  
                        'overflowX': 'auto',  
                        'width': '100%',  
                        'height': '410px'
                    },                      
                    
                )
           
             ], md=7),
             
             
             #seleccionador de paginas----------
             
             dbc.Col([           
              
                         dbc.Card(
                               dbc.CardBody([
                                      dbc.Row([
                                             dbc.Col(html.H4("",style={"font-size":"13px","margin-top":"-20px"}
                                                             ),md=1,sm=2,xs=2),  # Texto "Páginas"
                                                   
                                             dbc.Col([
                                                   dbc.Button("Pág-1", id="btn-1", color="primary", className="mr-1",style={"margin-top": "-27px","height": "27px","margin-left": "2px", "font-size": "65%","padding": "6px 22px","width":"30%"}),
                                                   dbc.Button("Pág-2", id="btn-2", color="primary", className="mr-1",style={"margin-top": "-27px","height": "27px","margin-left": "2px", "font-size": "65%","padding": "6px 22px","width":"30%"}),
                                                   dbc.Button("Pág-3", id="btn-3", color="primary", className="mr-1",style={"margin-top": "-27px","height": "27px","margin-left": "2px", "font-size": "65%","padding": "6px 22px","width":"30%"}),
                                              ],md=11,sm=11,xs=11)
                                       ], align="center"),
                                ]),
                                style={"background-color": "black", "color": "white", "padding": "10px","height":"50px"}
                          ),
                          html.Div(id="contenido-pagina")                  
                 
             ],md=5)
        
        
              
            
           
          ],style={"margin-top":"220px"}),
          
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
                         # Enlace vacío inicialmente
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
                        id="floating-chat",
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

@app.callback( Output("popover2","is_open"),
               [Input("icono","n_clicks"),
                Input("borrar","n_clicks")]
              )
def actualizar_popover(icono_clicks,borrar_clicks):
    ctx=dash.callback_context
    if not ctx.triggered_id:
     raise PreventUpdate
    
    is_open= True if ctx.triggered_id =="icono" else False
    
    return is_open

def formato_numero(num):
    
    if num >= 1000000000:
       return "S/"+"{:,.0f}".format(num/1000000000)+" B"
    
    elif num >= 1000000:
       return "S/"+"{:,.0f}".format(num/1000)+" M"
   
    else:
        return "S/"+"{:,.2f}".format(num)   
    


    
@app.callback([Output("total_ventas","children"),
               Output("total_utilidad","children"),
               Output("total_envio","children"),
               Output("total_descuento","children"),
               Output("barra1","figure"),
               Output("barra2","figure"),
               Output("circulo","figure"),
               Output("datatable-agrupada","data")],
              [Input("lista1","value"),
               Input("lista2","value"),
               Input("lista3","value")]              
              )
def actualizar_datos(value_a,value_b,value_c):
    
    df_tempo=df.copy()
    
    if value_a :
       df_tempo=df_tempo[df_tempo["Subcategoria"].isin(value_a)]
    
    if value_b :
       df_tempo=df_tempo[df_tempo["Empaque"].isin(value_b)]
    
    if value_c :
       df_tempo= df_tempo[df_tempo["Region"].isin(value_c)]
    
   
    
    
    total_ventas=formato_numero(df_tempo["Ventas"].sum())
    total_utilidad=formato_numero(df_tempo["Utilidad"].sum())
    total_envio=formato_numero(df_tempo["Costo_envio"].sum())
    total_descuento=formato_numero(df_tempo["Descuento"].sum())
    
    #------ FIGURA DE BARRAS (---total ventas---)
    #--a)hacemos una nueva tabla que se mostrara en la figura barras
    ventas_año=df_tempo.groupby("Año")["Ventas"].sum().reset_index()
    #-------CREAR UNA COLUMNA DE VARIACION PORCENTUAL POR AÑO:
    ventas_año["Variacion"]=(ventas_año["Ventas"].pct_change()*100).round(2)
    
    #---------hovertemplate ventanas emeregentes
    dropdown_lista={"Producto":value_a,"Empaque":value_b,"Pais":value_c}
    hovertemplate="%{y:,.2f}<br>"+"".join([f'<b style="color:lime;">{key}:</b><br>{"-".join(map(str,val))}<br>'for key ,val in dropdown_lista.items()if val])
    hovertemplate1="Año: %{label}<br>Cantidad de Envios : %{value}<br>"+"".join([f'<b style="color:lime;">{key}:</b><br>{"-".join(map(str,val))}<br>'for key ,val in dropdown_lista.items()if val])
    
    
    
    
    
    fig_vtas_año=go.Figure()
    fig_vtas_año.add_trace(go.Bar(x=ventas_año["Año"],y=ventas_año["Ventas"],name="ventas",hovertemplate=hovertemplate,marker=dict(color='rgb(255,255,255)')))
    fig_vtas_año.add_trace(go.Scatter(x=ventas_año["Año"],y=ventas_año["Variacion"], mode='lines+markers', yaxis='y2',name='Variación %'))
    fig_vtas_año.update_layout(yaxis2=dict(overlaying="y",side="right"))
    fig_vtas_año.update_layout(plot_bgcolor="#62A26E",paper_bgcolor='#62A26E')
    fig_vtas_año.update_yaxes(showgrid=False) 
    fig_vtas_año.update_layout(main_config,showlegend=False)
    
    # Cambiar el color de los valores de los ejes x e y a blanco
    fig_vtas_año.update_xaxes(tickfont=dict(color='rgb(255,255,255)'))  # Color blanco para los valores del eje x
    fig_vtas_año.update_yaxes(tickfont=dict(color='rgb(255,255,255)'))  # Color blanco para los valores del eje y

    
    
     #------ FIGURA DE BARRAS (---total utilidad---)
    utilidad_año=df_tempo.groupby("Año")["Utilidad"].sum().reset_index()
   
    utilidad_año["var%"]=(utilidad_año["Utilidad"].pct_change()*100).round(2)
    
    fig_utilidad_año=go.Figure()
    fig_utilidad_año.add_trace(go.Bar(x=utilidad_año["Año"],y=utilidad_año["Utilidad"],name="Utilidad de Ventas",hovertemplate=hovertemplate,marker=dict(color='rgb(255,255,255)')))
    fig_utilidad_año.add_trace(go.Scatter(x=utilidad_año["Año"],y=utilidad_año["var%"],mode="lines+markers",yaxis="y2"))
    fig_utilidad_año.update_layout(yaxis2=dict(overlaying="y",side="right"))
    fig_utilidad_año.update_layout(plot_bgcolor="#E7106F",paper_bgcolor="#E7106F")
    fig_utilidad_año.update_yaxes(showgrid=False) 
    fig_utilidad_año.update_layout(main_config,showlegend=False)
   
    # Cambiar el color de los valores de los ejes x e y a blanco
    fig_utilidad_año.update_xaxes(tickfont=dict(color='rgb(255,255,255)'))  # Color blanco para los valores del eje x
    fig_utilidad_año.update_yaxes(tickfont=dict(color='rgb(255,255,255)'))  # Color blanco para los valores del eje y

   
    #------ FIGURA DE CIRCULO (---total envio---)
    
    envio_año=df_tempo.groupby("Año")["Id"].count().reset_index()
    envio_total=envio_año["Id"].sum()
    
    fig_envios=go.Figure()
    fig_envios.add_trace(go.Pie(labels=envio_año["Año"],name="",values=envio_año["Id"],hovertemplate=hovertemplate1,hole=0.9,textfont=dict(color='white')))
    fig_envios.update_layout(main_config,showlegend=False)
    
    fig_envios.update_layout(paper_bgcolor="black")
    fig_envios.update_layout(
                              annotations=[
                                  dict(
                                      text=str(envio_total),
                                      x=0.5,
                                      y=0.55,
                                      font=dict(color="white"),
                                      showarrow=False,
                                      font_size=25
                                     
                                  ),
                                  dict(
                                      text="Cantidad total",
                                      x=0.5,
                                      y=0.45,
                                      font=dict(color="red"),
                                      showarrow=False,
                                      font_size=15
                                  )
                               ]                    
    )
    
    #------ FIGURA DE TABLA(------)
    
    tabla_agrupada=df_tempo.groupby(["Categoria","Subcategoria"])[["Cantidad","Ventas","Utilidad"]].sum().reset_index()
    
   
                                           
    
    return total_ventas,total_utilidad,total_envio,total_descuento,fig_vtas_año,fig_utilidad_año,fig_envios,tabla_agrupada.to_dict("records")
   
   # Callback para actualizar el estilo de las filas seleccionadas
@app.callback(
    Output('datatable-agrupada', 'style_data_conditional'),
    [Input('datatable-agrupada', 'active_cell')]
)
def update_styles(active_cell):
    if active_cell is None:
        return []
    styles = [{
        'if': {'row_index': active_cell['row']},
        'backgroundColor': 'rgba(249, 214, 207)'  # Cambia el color de fondo de la fila seleccionada
    }]
    return styles


# Callback para actualizar el contenido de la página y resaltar el botón seleccionado
@app.callback(
    [Output("contenido-pagina", "children"),
     Output("btn-1", "color"),
     Output("btn-2", "color"),
     Output("btn-3", "color")],
    [Input("btn-1", "n_clicks"),
     Input("btn-2", "n_clicks"),
     Input("btn-3", "n_clicks")]
)
def actualizar_contenido(btn1, btn2, btn3):
    ctx = callback_context
    if not ctx.triggered:
        return pagina1.layout, "success", "primary", "primary"
    else:
        boton_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if boton_id == "btn-1":
            return pagina1.layout, "success", "primary", "primary"
        elif boton_id == "btn-2":
            return pagina2.layout, "primary", "success", "primary"
        elif boton_id == "btn-3":
            return pagina3.layout, "primary", "primary", "success"
        else:
            return pagina1.layout, "success", "primary", "primary"

@app.callback(
    Output("floating-chat", "style"),
    [Input("whatsapp-button", "n_clicks"), Input("close-chat", "n_clicks")],
    [dash.dependencies.State("floating-chat", "style")]
)
def toggle_chat(n1, n2, style):
    if n1 or n2:
        if style["display"] == "none":
            style["display"] = "block"
        else:
            style["display"] = "none"
    return style
