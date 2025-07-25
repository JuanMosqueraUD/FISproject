import uvicorn
import os
from dotenv import load_dotenv

if __name__ == "__main__":
    # Cargar variables de entorno desde .env
    load_dotenv()
    
    # Verificar que las variables de entorno estén configuradas
    if not os.getenv("DATABASE_URL"):
        print("ERROR: DATABASE_URL no está configurada en las variables de entorno")
        print("Asegúrate de tener un archivo .env con la configuración de la base de datos")
        exit(1)
    
    print("Iniciando servidor FastAPI...")
    print(f"Base de datos: {os.getenv('DATABASE_URL', 'No configurada')}")
    
    try:
        uvicorn.run(
            "main:app",
            host="127.0.0.1",
            port=8000,
            reload=True,
            log_level="info"
        )
    except Exception as e:
        print(f"Error al iniciar el servidor: {e}")
