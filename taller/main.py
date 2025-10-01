from fastapi import FastAPI, UploadFile, File
import pandas as pd
import io
import math

app = FastAPI()

# ===== SUBIR Y PROCESAR EXCEL =====
@app.post("/upload-excel/")
async def upload_excel(file: UploadFile = File(...)):
    try:
        contents = await file.read()

        # Cargar Excel desde fila 11 como acordamos
        df = pd.read_excel(io.BytesIO(contents), header=None, skiprows=11)

        # Renombrar columnas
        df.columns = [
            "ID", "Razón Social", "Última Orden de Servicio", 
            "Recorrido Promedio Mensual", "Celular", "Extra1", "Vehículo",
            "Nivel", "Días Restantes", "Días Último Servicio", "Fecha Servicio/Revisión"
        ]

        # Eliminar columnas innecesarias
        df = df[[
            "ID", "Razón Social", "Última Orden de Servicio", 
            "Recorrido Promedio Mensual", "Celular", "Vehículo",
            "Nivel", "Días Restantes", "Días Último Servicio", "Fecha Servicio/Revisión"
        ]]

        # Limpiar filas sin celular
        df = df.dropna(subset=["Celular"])

        # Convertir a lista de números
        numbers = df["Celular"].astype(str).tolist()

        # Vista previa
        preview = df.head(5).to_dict(orient="records")

        return {
            "filename": file.filename,
            "rows": len(df),
            "preview": preview,
            "numbers": numbers
        }

    except Exception as e:
        return {"error": str(e)}


# ===== ENVIAR MENSAJES EN CHUNKS =====
@app.post("/send-messages/")
async def send_messages(data: dict):
    numbers = data.get("numbers", [])
    chunk_size = data.get("chunk_size", 100)  # Default 100 por lote

    total = len(numbers)
    total_chunks = math.ceil(total / chunk_size)

    sent_batches = []
    for i in range(0, total, chunk_size):
        chunk = numbers[i:i+chunk_size]
        # Aquí va la integración real con Twilio/WhatsApp
        sent_batches.append({"batch": i//chunk_size + 1, "count": len(chunk)})

    return {
        "total_numbers": total,
        "chunk_size": chunk_size,
        "total_batches": total_chunks,
        "batches": sent_batches
    }
