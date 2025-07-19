from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, schemas, crud
import uuid, requests, os
from dotenv import load_dotenv

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

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def cliente():
    return FileResponse("static/inventario.html")

@app.get("/admin")
def admin():
    return FileResponse("static/index.html")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/productos/", response_model=schemas.Producto)
def crear_producto(producto: schemas.ProductoCreate, db: Session = Depends(get_db)):
    return crud.crear_producto(db, producto)

@app.get("/productos/", response_model=list[schemas.Producto])
def listar_productos(db: Session = Depends(get_db)):
    return crud.obtener_productos(db)

@app.delete("/productos/{producto_id}")
def eliminar_producto(producto_id: int, db: Session = Depends(get_db)):
    return crud.eliminar_producto(db, producto_id)

@app.put("/productos/{producto_id}", response_model=schemas.Producto)
def actualizar_producto(producto_id: int, producto: schemas.ProductoCreate, db: Session = Depends(get_db)):
    return crud.actualizar_producto(db, producto_id, producto)

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
