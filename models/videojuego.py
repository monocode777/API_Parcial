from extensions import db

<<<<<<< HEAD
# Definimos el modelo "Videojuego" que se guardará en la base de datos
class Videojuego(Base):
    __tablename__ = 'videojuegos'  # ← Esta línea es necesaria

    # ID único de cada videojuego
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
=======
class Videojuego(db.Model):
    __tablename__ = 'videojuegos'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    desarrollador = db.Column(db.String(100), nullable=False)
    año_lanzamiento = db.Column(db.Integer)
    genero = db.Column(db.String(50))
    plataforma = db.Column(db.String(50))
    precio = db.Column(db.Float)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    
>>>>>>> development
    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'desarrollador': self.desarrollador,
            'año_lanzamiento': self.año_lanzamiento,
            'genero': self.genero,
            'plataforma': self.plataforma,
            'precio': self.precio,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }