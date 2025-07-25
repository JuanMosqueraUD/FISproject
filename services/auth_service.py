from datetime import datetime, timedelta
from typing import Optional
import hashlib
import secrets

class PasswordManager:
    """Clase para gestionar el hash y verificación de contraseñas"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Genera un hash de la contraseña"""
        # Para simplicidad usamos MD5, en producción usaría bcrypt
        return hashlib.md5(password.encode()).hexdigest()
    
    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """Verifica si la contraseña coincide con el hash"""
        return hashlib.md5(password.encode()).hexdigest() == hashed_password

class TokenManager:
    """Clase para gestionar tokens de sesión"""
    
    def __init__(self):
        self.active_tokens = {}  # token -> user_data
    
    def create_token(self, user_id: int, username: str, is_admin: bool) -> str:
        """Crea un token de sesión para el usuario"""
        token = secrets.token_urlsafe(32)
        self.active_tokens[token] = {
            "user_id": user_id,
            "username": username,
            "is_admin": is_admin,
            "created_at": datetime.now()
        }
        return token
    
    def validate_token(self, token: str) -> Optional[dict]:
        """Valida un token y retorna los datos del usuario"""
        if token in self.active_tokens:
            token_data = self.active_tokens[token]
            # Token válido por 24 horas
            if datetime.now() - token_data["created_at"] < timedelta(hours=24):
                return token_data
            else:
                # Token expirado
                del self.active_tokens[token]
        return None
    
    def invalidate_token(self, token: str):
        """Invalida un token (logout)"""
        if token in self.active_tokens:
            del self.active_tokens[token]

class AuthService:
    """Servicio principal de autenticación"""
    
    def __init__(self):
        self.password_manager = PasswordManager()
        self.token_manager = TokenManager()
    
    def authenticate_user(self, db, username: str, password: str) -> Optional[dict]:
        """Autentica un usuario y retorna datos si es válido"""
        # Usar UsuarioService en lugar de crud
        from services.usuario_service import UsuarioService
        
        usuario_service = UsuarioService(db)
        user = usuario_service.validar_credenciales(username, password)
        
        if user:
            return {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "is_admin": user.is_admin
            }
        return None
    
    def create_session(self, user_data: dict) -> str:
        """Crea una sesión para el usuario autenticado"""
        return self.token_manager.create_token(
            user_data["id"],
            user_data["username"],
            user_data["is_admin"]
        )
    
    def verify_admin_access(self, token: str) -> bool:
        """Verifica si el token corresponde a un usuario admin"""
        token_data = self.token_manager.validate_token(token)
        return token_data is not None and token_data.get("is_admin", False)
    
    def verify_user_access(self, token: str) -> Optional[dict]:
        """Verifica si el token es válido para cualquier usuario"""
        return self.token_manager.validate_token(token)
    
    def logout(self, token: str):
        """Cierra la sesión del usuario"""
        self.token_manager.invalidate_token(token)

# Instancia global del servicio de autenticación
auth_service = AuthService()
