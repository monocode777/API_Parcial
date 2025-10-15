import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv
from models.db import Base
from models.videojuego import Videojuego  # 👈 Importa el modelo antes de create_all

logging.basicConfig(level=logging.INFO)

# Cargar variables de entorno
load_dotenv()

MYSQL_URI = os.getenv('MYSQL_URI')
SQLITE_URI = 'sqlite:///./instance/database.db'  # 👈 Usa SOLO esta ruta

def get_engine():
    """
    Crea la conexión a MySQL si existe, de lo contrario usa SQLite local.
    """
    if MYSQL_URI:
        try:
            engine = create_engine(MYSQL_URI, echo=True)
            conn = engine.connect()
            conn.close()
            logging.info('✅ Conexión a MySQL exitosa.')
            return engine
        except OperationalError:
            logging.warning('⚠️ No se pudo conectar a MySQL. Usando SQLite local.')
    engine = create_engine(SQLITE_URI, echo=True)
    return engine

engine = get_engine()
Session = sessionmaker(bind=engine)

# 👇 Crear las tablas (una sola vez)
Base.metadata.create_all(engine)

def get_db_session():
    """Retorna una sesión nueva de base de datos."""
    return Session()
