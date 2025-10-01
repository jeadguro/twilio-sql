import pandas as pd
from fastapi import FastAPI, UploadFile, File, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, Servicio
from crud import get_or_create_cliente, get_or_create_carro, crear_servicio
from utils import necesita_servicio
from twilio.rest import Client
from datetime import datetime

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Twilio config
ACCOUNT_SID = "ACxxxxxxxx"
AUTH_TOKEN = "xxxxxxxx"
FROM_NUMBER = "+1XXXXXXXX"
twilio_client = Client(ACCOUNT_SID, AUTH_TOKEN)

# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    df = pd.read_csv(file.file)
    for _, row in df.iterrows():
        cliente = get_or_create_cliente(db, row["cliente_nombre"], row["telefono"])
        carro = get_or_create_carro(db, cliente.id, row["marca"], row["modelo"], row["anio"], row["placa"])
        fecha = datetime.strptime(row["fecha_servicio"], "%Y-%m-%d").date()
        crear_servicio(db, carro.id, row["tipo_servicio"], row["tipo_aceite"], fecha)
    return {"message": "CSV cargado correctamente"}


@app.get("/clientes-pendientes/")
def clientes_pendientes(db: Session = Depends(get_db)):
    servicios = db.query(Servicio).filter(Servicio.mensaje_enviado == False).all()
    pendientes = []
    for s in servicios:
        if necesita_servicio(s.proximo_servicio):
            pendientes.append({
                "cliente": s.carro.cliente.nombre,
                "telefono": s.carro.cliente.telefono,
                "carro": f"{s.carro.marca} {s.carro.modelo} {s.carro.anio}",
                "tipo_servicio": s.tipo_servicio,
                "tipo_aceite": s.tipo_aceite,
                "fecha_servicio": s.fecha_servicio.isoformat(),
                "proximo_servicio": s.proximo_servicio.isoformat()
            })
    return pendientes


@app.post("/enviar-mensajes/")
def enviar_mensajes(db: Session = Depends(get_db)):
    servicios = db.query(Servicio).filter(Servicio.mensaje_enviado == False).all()
    enviados = []
    for s in servicios:
        if necesita_servicio(s.proximo_servicio):
            msg = f"Hola {s.carro.cliente.nombre}, su carro {s.carro.marca} {s.carro.modelo} ({s.carro.placa}) ya requiere {s.tipo_servicio}. Agende su cita."
            twilio_client.messages.create(
                body=msg,
                from_=FROM_NUMBER,
                to=s.carro.cliente.telefono
            )
            s.mensaje_enviado = True
            enviados.append(s.carro.cliente.nombre)
    db.commit()
    return {"mensajes_enviados": enviados}
