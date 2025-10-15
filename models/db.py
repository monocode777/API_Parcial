from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Ruta de la base de datos SQLite (puedes cambiarla si quieres)
DATABASE_URL = "sqlite:///./instance/database.db"

# Crea el motor de conexión
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Crea la clase base de los modelos
Base = declarative_base()

# Crea la sesión (para interactuar con la base)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
