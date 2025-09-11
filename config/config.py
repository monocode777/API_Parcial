import os

class Config:
    # Clave secreta usada por Flask (sesiones, seguridad)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'clave_secreta_default'

    # Ruta de la base de datos SQLite
    SQLALCHEMY_DATABASE_URI = 'sqlite:///videojuegos.db'

    # Desactiva advertencias innecesarias de SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
