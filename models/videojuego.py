from extensions import db

# Definimos el modelo "Videojuego" que se guardará en la base de datos
class Videojuego(db.Model):
    # ID único de cada videojuego
    id = db.Column(db.Integer, primary_key=True)

    # Título del videojuego (obligatorio)
    titulo = db.Column(db.String(100), nullable=False)

    # Género del videojuego (ej: Aventura, Acción, RPG...)
    genero = db.Column(db.String(50), nullable=False)

    # Plataforma donde se juega (ej: PC, PlayStation, Xbox...)
    plataforma = db.Column(db.String(50), nullable=False)

    # Calificación del videojuego (ej: 4.5 sobre 5)
    rating = db.Column(db.Float, nullable=False)

    # Método para convertir un objeto en un diccionario (para enviarlo en JSON)
    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "genero": self.genero,
            "plataforma": self.plataforma,
            "rating": self.rating
        }
