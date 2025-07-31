from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Cookie
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, schemas
import uuid, requests, os
from dotenv import load_dotenv
from services.auth_service import auth_service
from services.producto_service import ProductoService
from services.usuario_service import UsuarioService
from typing import Optional

load_dotenv()
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurar archivos estáticos sin caché para desarrollo
class NoCacheStaticFiles(StaticFiles):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def file_response(self, full_path, stat_result, scope, status_code=200):
        response = super().file_response(full_path, stat_result, scope, status_code)
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response

app.mount("/static", NoCacheStaticFiles(directory="static"), name="static")

@app.get("/")
def cliente():
    return FileResponse("static/inventario.html")

@app.get("/admin")
def admin(token: Optional[str] = Cookie(None)):
    # Verificar si el usuario está autenticado y es admin
    if not token or not auth_service.verify_admin_access(token):
        return FileResponse("static/login.html")
    return FileResponse("static/index.html")

@app.get("/login")
def login_page():
    return FileResponse("static/login.html")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/productos/", response_model=schemas.Producto)
def crear_producto(producto: schemas.ProductoCreate, token: Optional[str] = Cookie(None), db: Session = Depends(get_db)):
    # Verificar que el usuario sea admin
    if not token or not auth_service.verify_admin_access(token):
        raise HTTPException(status_code=403, detail="Acceso denegado - Solo administradores")
    
    # Usar el servicio de productos
    producto_service = ProductoService(db)
    return producto_service.crear_producto(producto)

@app.get("/productos/", response_model=list[schemas.Producto])
def listar_productos(db: Session = Depends(get_db)):
    # Usar el servicio de productos
    producto_service = ProductoService(db)
    return producto_service.obtener_productos()

@app.delete("/productos/{producto_id}")
def eliminar_producto(producto_id: int, token: Optional[str] = Cookie(None), db: Session = Depends(get_db)):
    # Verificar que el usuario sea admin
    if not token or not auth_service.verify_admin_access(token):
        raise HTTPException(status_code=403, detail="Acceso denegado - Solo administradores")
    
    # Usar el servicio de productos
    producto_service = ProductoService(db)
    return producto_service.eliminar_producto(producto_id)

@app.put("/productos/{producto_id}", response_model=schemas.Producto)
def actualizar_producto(producto_id: int, producto: schemas.ProductoCreate, token: Optional[str] = Cookie(None), db: Session = Depends(get_db)):
    # Verificar que el usuario sea admin
    if not token or not auth_service.verify_admin_access(token):
        raise HTTPException(status_code=403, detail="Acceso denegado - Solo administradores")
    
    # Usar el servicio de productos
    producto_service = ProductoService(db)
    return producto_service.actualizar_producto(producto_id, producto)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

@app.post("/upload-imagen/")
async def upload_imagen(file: UploadFile = File(...)):
    nombre_archivo = f"{uuid.uuid4()}_{file.filename}"
    contenido = await file.read()

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/octet-stream"
    }

    url = f"{SUPABASE_URL}/storage/v1/object/imagenes/{nombre_archivo}"

    resp = requests.post(url, headers=headers, data=contenido)
    if resp.status_code in [200, 201]:
        imagen_url = f"{SUPABASE_URL}/storage/v1/object/public/imagenes/{nombre_archivo}"
        return {"url": imagen_url}
    else:
        raise HTTPException(status_code=500, detail="Error al subir la imagen")

# ============ RUTAS DE AUTENTICACIÓN ============

@app.post("/auth/register", response_model=schemas.Usuario)
def registrar_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    """Registrar un nuevo usuario"""
    usuario_service = UsuarioService(db)
    return usuario_service.crear_usuario(usuario)

@app.post("/auth/login")
def login(credentials: schemas.UsuarioLogin, db: Session = Depends(get_db)):
    """Autenticar usuario y crear sesión"""
    usuario_service = UsuarioService(db)
    user = usuario_service.validar_credenciales(credentials.username, credentials.password)
    
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    
    # Convertir a dict para el servicio de auth
    user_data = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "is_admin": user.is_admin
    }
    
    token = auth_service.create_session(user_data)
    
    # Crear respuesta con cookie
    response = RedirectResponse(url="/admin" if user_data["is_admin"] else "/", status_code=302)
    response.set_cookie(key="token", value=token, httponly=True, max_age=86400)  # 24 horas
    
    return response

@app.post("/auth/logout")
def logout(token: Optional[str] = Cookie(None)):
    """Cerrar sesión del usuario"""
    if token:
        auth_service.logout(token)
    
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie(key="token")
    return response

@app.get("/auth/me")
def get_current_user(token: Optional[str] = Cookie(None)):
    """Obtener información del usuario actual"""
    if not token:
        raise HTTPException(status_code=401, detail="No autenticado")
    
    user_data = auth_service.verify_user_access(token)
    if not user_data:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    return user_data

@app.get("/usuarios/", response_model=list[schemas.Usuario])
def listar_usuarios(token: Optional[str] = Cookie(None), db: Session = Depends(get_db)):
    """Listar todos los usuarios (solo para admins)"""
    if not token or not auth_service.verify_admin_access(token):
        raise HTTPException(status_code=403, detail="Acceso denegado - Solo administradores")
    
    usuario_service = UsuarioService(db)
    return usuario_service.obtener_usuarios()

# ============ RUTAS ADICIONALES PARA APROVECHAR LOS SERVICIOS ============

@app.get("/productos/categoria/{categoria}", response_model=list[schemas.Producto])
def buscar_productos_por_categoria(categoria: str, db: Session = Depends(get_db)):
    """Buscar productos por categoría"""
    producto_service = ProductoService(db)
    return producto_service.buscar_productos_por_categoria(categoria)

@app.get("/productos/marca/{marca}", response_model=list[schemas.Producto])
def buscar_productos_por_marca(marca: str, db: Session = Depends(get_db)):
    """Buscar productos por marca"""
    producto_service = ProductoService(db)
    return producto_service.buscar_productos_por_marca(marca)

@app.get("/productos/stock-bajo", response_model=list[schemas.Producto])
def productos_stock_bajo(limite: int = 5, token: Optional[str] = Cookie(None), db: Session = Depends(get_db)):
    """Obtener productos con stock bajo (solo para admins)"""
    if not token or not auth_service.verify_admin_access(token):
        raise HTTPException(status_code=403, detail="Acceso denegado - Solo administradores")
    
    producto_service = ProductoService(db)
    return producto_service.verificar_stock_bajo(limite)

@app.get("/usuarios/administradores", response_model=list[schemas.Usuario])
def listar_administradores(token: Optional[str] = Cookie(None), db: Session = Depends(get_db)):
    """Listar usuarios administradores (solo para admins)"""
    if not token or not auth_service.verify_admin_access(token):
        raise HTTPException(status_code=403, detail="Acceso denegado - Solo administradores")
    
    usuario_service = UsuarioService(db)
    return usuario_service.obtener_administradores()


