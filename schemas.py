from pydantic import BaseModel

class ProductoBase(BaseModel):
    nombre: str
    cantidad: int
    descripcion: str
    marca: str
    categoria: str
    imagen_url: str | None = None

class ProductoCreate(ProductoBase):
    pass

class Producto(ProductoBase):
    id: int

    class Config:
        from_attributes = True
