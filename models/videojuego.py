from sqlalchemy import Column, Integer, String, Float
from models.db import Base

class Videojuego(Base):
    __tablename__ = 'video_juegos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(100), nullable=False)
    genero = Column(String(50), nullable=False)
    plataforma = Column(String(50), nullable=False)
    rating = Column(Float)
