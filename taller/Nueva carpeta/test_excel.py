import pandas as pd

file_path = "afinaciones.xlsx"   # pon aquí la ruta de tu archivo

# Leer el archivo a partir de la fila 11 (row 10 en base 0)
df = pd.read_excel(file_path, header=None, skiprows=11)

# Asignar nombres de columnas manualmente
df.columns = [
    "ID", "Razón Social", "Última Orden de Servicio", 
    "Recorrido Promedio Mensual", "Celular", "Extra1", "Vehículo",
    "Nivel", "Días Restantes", "Días Último Servicio", "Fecha Servicio/Revisión"
]

# Quitar columnas extrañas
df = df[["ID", "Razón Social", "Última Orden de Servicio", 
         "Recorrido Promedio Mensual", "Celular", "Vehículo",
         "Nivel", "Días Restantes", "Días Último Servicio", "Fecha Servicio/Revisión"]]

# Limpiar filas vacías (cuando no hay número de celular, por ejemplo)
df = df.dropna(subset=["Celular"])

print(df.head(10))   # Ver los primeros 10 registros
