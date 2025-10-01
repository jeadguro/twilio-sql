from sqlalchemy.orm import Session
from models import Cliente, Carro, Servicio
from utils import calcular_proximo_servicio

def get_or_create_cliente(db: Session, nombre, telefono, email=None):
    cliente = db.query(Cliente).filter_by(telefono=telefono).first()
    if not cliente:
        cliente = Cliente(nombre=nombre, telefono=telefono, email=email)
        db.add(cliente)
        db.commit()
        db.refresh(cliente)
    return cliente

def get_or_create_carro(db: Session, cliente_id, marca, modelo, anio, placa):
    carro = db.query(Carro).filter_by(placa=placa).first()
    if not carro:
        carro = Carro(cliente_id=cliente_id, marca=marca, modelo=modelo, anio=anio, placa=placa)
        db.add(carro)
        db.commit()
        db.refresh(carro)
    return carro

def crear_servicio(db: Session, carro_id, tipo_servicio, tipo_aceite, fecha_servicio):
    proximo = calcular_proximo_servicio(fecha_servicio, tipo_aceite)
    servicio = Servicio(
        carro_id=carro_id,
        tipo_servicio=tipo_servicio,
        tipo_aceite=tipo_aceite,
        fecha_servicio=fecha_servicio,
        proximo_servicio=proximo
    )
    db.add(servicio)
    db.commit()
    db.refresh(servicio)
    return servicio
