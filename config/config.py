import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "secret-key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///videojuegos.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
