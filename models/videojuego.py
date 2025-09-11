from app import db

# Modelo que representa la tabla "videojuegos"
class Videojuego(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Identificador único
    titulo = db.Column(db.String(100), nullable=False)  # Nombre del videojuego
    genero = db.Column(db.String(50), nullable=False)   # Género (acción, RPG, etc.)
    plataforma = db.Column(db.String(50), nullable=False)  # Plataforma (PS5, PC, etc.)
    rating = db.Column(db.Float, nullable=False)  # Calificación

    # Convierte el objeto a un diccionario (útil para JSON en la API)
    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'genero': self.genero,
            'plataforma': self.plataforma,
            'rating': self.rating
        }
