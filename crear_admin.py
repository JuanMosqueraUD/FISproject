"""
Script para crear un usuario administrador inicial
Ejecutar este script después de crear la base de datos
"""

from database import SessionLocal, engine
import models, schemas
from services.usuario_service import UsuarioService

def crear_admin_inicial():
    """Crea un usuario administrador inicial si no existe"""
    
    # Crear las tablas si no existen
    models.Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Crear instancia del servicio de usuarios
        usuario_service = UsuarioService(db)
        
        # Verificar si ya existe un admin
        admin_existente = usuario_service.obtener_usuario_por_username("admin")
        
        if admin_existente:
            print("✅ Usuario administrador ya existe")
            print(f"   Username: {admin_existente.username}")
            print(f"   Email: {admin_existente.email}")
            return
        
        # Crear usuario administrador
        admin_data = schemas.UsuarioCreate(
            username="admin",
            email="admin@maquillaje.com",
            password="admin123",
            is_admin=True
        )
        
        admin_usuario = usuario_service.crear_usuario(admin_data)
        
        print("🎉 ¡Usuario administrador creado exitosamente!")
        print(f"   Username: {admin_usuario.username}")
        print(f"   Email: {admin_usuario.email}")
        print(f"   Es admin: {admin_usuario.is_admin}")
        print("\n📝 Credenciales de acceso:")
        print(f"   Usuario: admin")
        print(f"   Contraseña: admin123")
        print("\n🔗 Accede en: http://localhost:8000/login")
        
    except Exception as e:
        print(f"❌ Error al crear usuario administrador: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Creando usuario administrador inicial...")
    crear_admin_inicial()
