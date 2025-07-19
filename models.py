from sqlalchemy import Column, Integer, String
from database import Base

class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    cantidad = Column(Integer)
    descripcion = Column(String)
    marca = Column(String)
    categoria = Column(String)
    imagen_url = Column(String)
