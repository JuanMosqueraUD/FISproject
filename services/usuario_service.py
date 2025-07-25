from sqlalchemy.orm import Session
from fastapi import HTTPException
import models, schemas
from services.auth_service import PasswordManager
from typing import List, Optional

class UsuarioService:
    """
    Servicio para operaciones CRUD de usuarios usando programación orientada a objetos.
    Implementa el patrón Repository con encapsulación de la lógica de negocio.
    """
    
    def __init__(self, db: Session):
        """
        Constructor del servicio de usuarios.
        
        Args:
            db (Session): Sesión de base de datos SQLAlchemy
        """
        self.db = db
        self.password_manager = PasswordManager()

    def crear_usuario(self, data: schemas.UsuarioCreate) -> models.Usuario:
        """
        Crea un nuevo usuario en la base de datos.
        
        Args:
            data (UsuarioCreate): Datos del usuario a crear
            
        Returns:
            Usuario: El usuario creado
            
        Raises:
            HTTPException: Si hay error en la creación o el usuario ya existe
        """
        try:
            # Verificar si el usuario ya existe
            if self.obtener_usuario_por_username(data.username):
                raise HTTPException(status_code=400, detail="El usuario ya existe")
            
            if self.obtener_usuario_por_email(data.email):
                raise HTTPException(status_code=400, detail="El email ya está registrado")
            
            # Hash de la contraseña
            hashed_password = self.password_manager.hash_password(data.password)
            
            # Crear el usuario
            usuario = models.Usuario(
                username=data.username,
                email=data.email,
                password=hashed_password,
                is_admin=data.is_admin
            )
            
            self.db.add(usuario)
            self.db.commit()
            self.db.refresh(usuario)
            print(f"UsuarioService: Usuario {data.username} creado exitosamente")
            return usuario
        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            print(f"UsuarioService: Error al crear usuario: {e}")
            raise HTTPException(status_code=500, detail=f"Error al crear usuario: {str(e)}")

    def obtener_usuarios(self) -> List[models.Usuario]:
        """
        Obtiene todos los usuarios de la base de datos.
        
        Returns:
            List[Usuario]: Lista de todos los usuarios
            
        Raises:
            HTTPException: Si hay error en la consulta
        """
        try:
            usuarios = self.db.query(models.Usuario).all()
            print(f"UsuarioService: Obtenidos {len(usuarios)} usuarios")
            return usuarios
        except Exception as e:
            print(f"UsuarioService: Error al obtener usuarios: {e}")
            raise HTTPException(status_code=500, detail=f"Error al obtener usuarios: {str(e)}")

    def obtener_usuario_por_id(self, usuario_id: int) -> Optional[models.Usuario]:
        """
        Obtiene un usuario específico por su ID.
        
        Args:
            usuario_id (int): ID del usuario a buscar
            
        Returns:
            Usuario | None: El usuario encontrado o None si no existe
        """
        try:
            usuario = self.db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
            if usuario:
                print(f"UsuarioService: Usuario {usuario_id} encontrado")
            else:
                print(f"UsuarioService: Usuario {usuario_id} no encontrado")
            return usuario
        except Exception as e:
            print(f"UsuarioService: Error al buscar usuario por ID: {e}")
            return None

    def obtener_usuario_por_username(self, username: str) -> Optional[models.Usuario]:
        """
        Obtiene un usuario por su nombre de usuario.
        
        Args:
            username (str): Nombre de usuario a buscar
            
        Returns:
            Usuario | None: El usuario encontrado o None si no existe
        """
        try:
            usuario = self.db.query(models.Usuario).filter(models.Usuario.username == username).first()
            if usuario:
                print(f"UsuarioService: Usuario '{username}' encontrado")
            return usuario
        except Exception as e:
            print(f"UsuarioService: Error al buscar usuario por username: {e}")
            return None

    def obtener_usuario_por_email(self, email: str) -> Optional[models.Usuario]:
        """
        Obtiene un usuario por su email.
        
        Args:
            email (str): Email del usuario a buscar
            
        Returns:
            Usuario | None: El usuario encontrado o None si no existe
        """
        try:
            usuario = self.db.query(models.Usuario).filter(models.Usuario.email == email).first()
            if usuario:
                print(f"UsuarioService: Usuario con email '{email}' encontrado")
            return usuario
        except Exception as e:
            print(f"UsuarioService: Error al buscar usuario por email: {e}")
            return None

    def actualizar_usuario(self, usuario_id: int, data: schemas.UsuarioBase) -> models.Usuario:
        """
        Actualiza un usuario existente.
        
        Args:
            usuario_id (int): ID del usuario a actualizar
            data (UsuarioBase): Nuevos datos del usuario
            
        Returns:
            Usuario: El usuario actualizado
            
        Raises:
            HTTPException: Si el usuario no existe o hay error en la actualización
        """
        try:
            usuario = self.obtener_usuario_por_id(usuario_id)
            if not usuario:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")
            
            print(f"UsuarioService: Actualizando usuario {usuario_id}")
            
            # Verificar si el nuevo username ya existe (si se está cambiando)
            if data.username != usuario.username and self.obtener_usuario_por_username(data.username):
                raise HTTPException(status_code=400, detail="El nuevo nombre de usuario ya existe")
            
            # Verificar si el nuevo email ya existe (si se está cambiando)
            if data.email != usuario.email and self.obtener_usuario_por_email(data.email):
                raise HTTPException(status_code=400, detail="El nuevo email ya está registrado")
            
            # Actualizar campos
            usuario.username = data.username
            usuario.email = data.email
            usuario.is_admin = data.is_admin
            
            self.db.commit()
            self.db.refresh(usuario)
            print(f"UsuarioService: Usuario {usuario_id} actualizado exitosamente")
            return usuario
        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            print(f"UsuarioService: Error al actualizar usuario: {e}")
            raise HTTPException(status_code=500, detail=f"Error al actualizar usuario: {str(e)}")

    def cambiar_password(self, usuario_id: int, nueva_password: str) -> models.Usuario:
        """
        Cambia la contraseña de un usuario.
        
        Args:
            usuario_id (int): ID del usuario
            nueva_password (str): Nueva contraseña en texto plano
            
        Returns:
            Usuario: El usuario actualizado
            
        Raises:
            HTTPException: Si el usuario no existe o hay error
        """
        try:
            usuario = self.obtener_usuario_por_id(usuario_id)
            if not usuario:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")
            
            # Hash de la nueva contraseña
            hashed_password = self.password_manager.hash_password(nueva_password)
            usuario.password = hashed_password
            
            self.db.commit()
            self.db.refresh(usuario)
            print(f"UsuarioService: Contraseña actualizada para usuario {usuario_id}")
            return usuario
        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            print(f"UsuarioService: Error al cambiar contraseña: {e}")
            raise HTTPException(status_code=500, detail=f"Error al cambiar contraseña: {str(e)}")

    def eliminar_usuario(self, usuario_id: int) -> dict:
        """
        Elimina un usuario de la base de datos.
        
        Args:
            usuario_id (int): ID del usuario a eliminar
            
        Returns:
            dict: Mensaje de confirmación
            
        Raises:
            HTTPException: Si el usuario no existe o hay error en la eliminación
        """
        try:
            usuario = self.obtener_usuario_por_id(usuario_id)
            if not usuario:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")
            
            self.db.delete(usuario)
            self.db.commit()
            print(f"UsuarioService: Usuario {usuario_id} eliminado exitosamente")
            return {"mensaje": "Usuario eliminado exitosamente"}
        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            print(f"UsuarioService: Error al eliminar usuario: {e}")
            raise HTTPException(status_code=500, detail=f"Error al eliminar usuario: {str(e)}")

    def obtener_administradores(self) -> List[models.Usuario]:
        """
        Obtiene todos los usuarios administradores.
        
        Returns:
            List[Usuario]: Lista de usuarios administradores
        """
        try:
            admins = self.db.query(models.Usuario).filter(models.Usuario.is_admin == True).all()
            print(f"UsuarioService: Encontrados {len(admins)} administradores")
            return admins
        except Exception as e:
            print(f"UsuarioService: Error al obtener administradores: {e}")
            return []

    def obtener_usuarios_regulares(self) -> List[models.Usuario]:
        """
        Obtiene todos los usuarios regulares (no administradores).
        
        Returns:
            List[Usuario]: Lista de usuarios regulares
        """
        try:
            usuarios = self.db.query(models.Usuario).filter(models.Usuario.is_admin == False).all()
            print(f"UsuarioService: Encontrados {len(usuarios)} usuarios regulares")
            return usuarios
        except Exception as e:
            print(f"UsuarioService: Error al obtener usuarios regulares: {e}")
            return []

    def validar_credenciales(self, username: str, password: str) -> Optional[models.Usuario]:
        """
        Valida las credenciales de un usuario.
        
        Args:
            username (str): Nombre de usuario
            password (str): Contraseña en texto plano
            
        Returns:
            Usuario | None: El usuario si las credenciales son válidas, None en caso contrario
        """
        try:
            usuario = self.obtener_usuario_por_username(username)
            if usuario and self.password_manager.verify_password(password, usuario.password):
                print(f"UsuarioService: Credenciales válidas para usuario '{username}'")
                return usuario
            else:
                print(f"UsuarioService: Credenciales inválidas para usuario '{username}'")
                return None
        except Exception as e:
            print(f"UsuarioService: Error al validar credenciales: {e}")
            return None
