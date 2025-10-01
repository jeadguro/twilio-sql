from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100))
    telefono = Column(String(20), unique=True)
    email = Column(String(100))

    carros = relationship("Carro", back_populates="cliente")


class Carro(Base):
    __tablename__ = "carros"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    marca = Column(String(50))
    modelo = Column(String(50))
    anio = Column(Integer)
    placa = Column(String(20), unique=True)

    cliente = relationship("Cliente", back_populates="carros")
    servicios = relationship("Servicio", back_populates="carro")


class Servicio(Base):
    __tablename__ = "servicios"

    id = Column(Integer, primary_key=True, index=True)
    carro_id = Column(Integer, ForeignKey("carros.id"))
    tipo_servicio = Column(String(100))
    tipo_aceite = Column(String(50))
    fecha_servicio = Column(Date)
    proximo_servicio = Column(Date)
    mensaje_enviado = Column(Boolean, default=False)

    carro = relationship("Carro", back_populates="servicios")
