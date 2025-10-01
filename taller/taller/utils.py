from datetime import timedelta, date

def calcular_proximo_servicio(fecha_servicio, tipo_aceite):
    if tipo_aceite.lower() == "sintético":
        return fecha_servicio + timedelta(days=180)
    else:
        return fecha_servicio + timedelta(days=90)

def necesita_servicio(proximo_servicio):
    return date.today() >= proximo_servicio
