from sqlalchemy.orm import Session
import models, schemas

def crear_producto(db: Session, producto: schemas.ProductoCreate):
    db_producto = models.Producto(**producto.dict())
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto

def obtener_productos(db: Session):
    return db.query(models.Producto).all()

def eliminar_producto(db: Session, producto_id: int):
    producto = db.query(models.Producto).filter(models.Producto.id == producto_id).first()
    if producto:
        db.delete(producto)
        db.commit()
        return {"mensaje": "Producto eliminado"}
    else:
        raise Exception("Producto no encontrado")

def actualizar_producto(db: Session, producto_id: int, datos: schemas.ProductoCreate):
    producto = db.query(models.Producto).filter(models.Producto.id == producto_id).first()
    if not producto:
        raise Exception("Producto no encontrado")
    for campo, valor in datos.dict().items():
        setattr(producto, campo, valor)
    db.commit()
    db.refresh(producto)
    return producto
