from sqlalchemy.orm import Session
from fastapi import HTTPException
import models, schemas
from typing import List, Optional

class ProductoService:
    """
    Servicio para operaciones CRUD de productos usando programación orientada a objetos.
    Implementa el patrón Repository con encapsulación de la lógica de negocio.
    """
    
    def __init__(self, db: Session):
        """
        Constructor del servicio de productos.
        
        Args:
            db (Session): Sesión de base de datos SQLAlchemy
        """
        self.db = db

    def crear_producto(self, data: schemas.ProductoCreate) -> models.Producto:
        """
        Crea un nuevo producto en la base de datos.
        
        Args:
            data (ProductoCreate): Datos del producto a crear
            
        Returns:
            Producto: El producto creado
            
        Raises:
            HTTPException: Si hay error en la creación
        """
        try:
            print(f"ProductoService: Creando producto con datos: {data.dict()}")
            producto = models.Producto(**data.dict())
            self.db.add(producto)
            self.db.commit()
            self.db.refresh(producto)
            print(f"ProductoService: Producto creado exitosamente con ID: {producto.id}")
            return producto
        except Exception as e:
            self.db.rollback()
            print(f"ProductoService: Error al crear producto: {e}")
            raise HTTPException(status_code=500, detail=f"Error al crear producto: {str(e)}")

    def obtener_productos(self) -> List[models.Producto]:
        """
        Obtiene todos los productos de la base de datos.
        
        Returns:
            List[Producto]: Lista de todos los productos
            
        Raises:
            HTTPException: Si hay error en la consulta
        """
        try:
            productos = self.db.query(models.Producto).all()
            print(f"ProductoService: Obtenidos {len(productos)} productos")
            return productos
        except Exception as e:
            print(f"ProductoService: Error al obtener productos: {e}")
            raise HTTPException(status_code=500, detail=f"Error al obtener productos: {str(e)}")

    def obtener_producto_por_id(self, producto_id: int) -> Optional[models.Producto]:
        """
        Obtiene un producto específico por su ID.
        
        Args:
            producto_id (int): ID del producto a buscar
            
        Returns:
            Producto | None: El producto encontrado o None si no existe
        """
        try:
            producto = self.db.query(models.Producto).filter(models.Producto.id == producto_id).first()
            if producto:
                print(f"ProductoService: Producto {producto_id} encontrado")
            else:
                print(f"ProductoService: Producto {producto_id} no encontrado")
            return producto
        except Exception as e:
            print(f"ProductoService: Error al buscar producto: {e}")
            return None

    def eliminar_producto(self, producto_id: int) -> dict:
        """
        Elimina un producto de la base de datos.
        
        Args:
            producto_id (int): ID del producto a eliminar
            
        Returns:
            dict: Mensaje de confirmación
            
        Raises:
            HTTPException: Si el producto no existe o hay error en la eliminación
        """
        try:
            producto = self.obtener_producto_por_id(producto_id)
            if not producto:
                raise HTTPException(status_code=404, detail="Producto no encontrado")
            
            self.db.delete(producto)
            self.db.commit()
            print(f"ProductoService: Producto {producto_id} eliminado exitosamente")
            return {"mensaje": "Producto eliminado exitosamente"}
        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            print(f"ProductoService: Error al eliminar producto: {e}")
            raise HTTPException(status_code=500, detail=f"Error al eliminar producto: {str(e)}")

    def actualizar_producto(self, producto_id: int, data: schemas.ProductoCreate) -> models.Producto:
        """
        Actualiza un producto existente.
        
        Args:
            producto_id (int): ID del producto a actualizar
            data (ProductoCreate): Nuevos datos del producto
            
        Returns:
            Producto: El producto actualizado
            
        Raises:
            HTTPException: Si el producto no existe o hay error en la actualización
        """
        try:
            producto = self.obtener_producto_por_id(producto_id)
            if not producto:
                raise HTTPException(status_code=404, detail="Producto no encontrado")
            
            print(f"ProductoService: Actualizando producto {producto_id} con datos: {data.dict()}")
            for campo, valor in data.dict().items():
                setattr(producto, campo, valor)
            
            self.db.commit()
            self.db.refresh(producto)
            print(f"ProductoService: Producto {producto_id} actualizado exitosamente")
            return producto
        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            print(f"ProductoService: Error al actualizar producto: {e}")
            raise HTTPException(status_code=500, detail=f"Error al actualizar producto: {str(e)}")

    def buscar_productos_por_categoria(self, categoria: str) -> List[models.Producto]:
        """
        Busca productos por categoría.
        
        Args:
            categoria (str): Categoría a buscar
            
        Returns:
            List[Producto]: Lista de productos de la categoría
        """
        try:
            productos = self.db.query(models.Producto).filter(models.Producto.categoria.ilike(f"%{categoria}%")).all()
            print(f"ProductoService: Encontrados {len(productos)} productos en categoría '{categoria}'")
            return productos
        except Exception as e:
            print(f"ProductoService: Error al buscar por categoría: {e}")
            return []

    def buscar_productos_por_marca(self, marca: str) -> List[models.Producto]:
        """
        Busca productos por marca.
        
        Args:
            marca (str): Marca a buscar
            
        Returns:
            List[Producto]: Lista de productos de la marca
        """
        try:
            productos = self.db.query(models.Producto).filter(models.Producto.marca.ilike(f"%{marca}%")).all()
            print(f"ProductoService: Encontrados {len(productos)} productos de marca '{marca}'")
            return productos
        except Exception as e:
            print(f"ProductoService: Error al buscar por marca: {e}")
            return []

    def verificar_stock_bajo(self, limite: int = 5) -> List[models.Producto]:
        """
        Obtiene productos con stock bajo.
        
        Args:
            limite (int): Cantidad límite para considerar stock bajo
            
        Returns:
            List[Producto]: Lista de productos con stock bajo
        """
        try:
            productos = self.db.query(models.Producto).filter(models.Producto.cantidad <= limite).all()
            print(f"ProductoService: Encontrados {len(productos)} productos con stock bajo")
            return productos
        except Exception as e:
            print(f"ProductoService: Error al verificar stock: {e}")
            return []
