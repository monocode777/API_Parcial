from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Videojuego(db.Model):
    __tablename__ = "videojuegos"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo = db.Column(db.String(100), nullable=False)
    genero = db.Column(db.String(50), nullable=False)
    plataforma = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "genero": self.genero,
            "plataforma": self.plataforma,
            "rating": self.rating,
        }
