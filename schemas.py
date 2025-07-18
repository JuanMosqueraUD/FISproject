from pydantic import BaseModel

class ProductoBase(BaseModel):
    nombre: str
    cantidad: int
    descripcion: str

class ProductoCreate(ProductoBase):
    pass

class Producto(ProductoBase):
    id: int

    class Config:
        from_attributes = True
