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

class UsuarioBase(BaseModel):
    username: str
    email: str
    is_admin: bool = False

class UsuarioCreate(UsuarioBase):
    password: str

class UsuarioLogin(BaseModel):
    username: str
    password: str

class Usuario(UsuarioBase):
    id: int

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class LoginResponse(BaseModel):
    token: str
    user: Usuario
