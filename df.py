import pandas as pd


url = 'https://github.com/kont123456/envios_global/raw/main/Plantilla.xlsx'
df = pd.read_excel(url)
df["Año"]=df["Fecha_envio"].dt.year.astype(str)
df["Mes"]=df["Fecha_envio"].dt.month




