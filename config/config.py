class Config:
    DEBUG = True
    SECRET_KEY = "clave-secreta"
    SQLALCHEMY_DATABASE_URI = "sqlite:///videojuegos.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False