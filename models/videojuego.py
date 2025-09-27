from sqlalchemy import Column, Integer, String, Float
from models.db import Base

# Definimos el modelo "Videojuego" que se guardará en la base de datos
class Videojuego(Base):
    # ID único de cada videojuego
    __tablename__ = "video_juegos"
    id = Column(Integer, primary_key=True)

    # Título del videojuego (obligatorio)
    titulo = Column(String(100), nullable=False)

    # Género del videojuego (ej: Aventura, Acción, RPG...)
    genero = Column(String(50), nullable=False)

    # Plataforma donde se juega (ej: PC, PlayStation, Xbox...)
    plataforma = Column(String(50), nullable=False)

    # Calificación del videojuego (ej: 4.5 sobre 5)
    rating = Column(Float, nullable=False)

    # Método para convertir un objeto en un diccionario (para enviarlo en JSON)
    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "genero": self.genero,
            "plataforma": self.plataforma,
            "rating": self.rating
        }
