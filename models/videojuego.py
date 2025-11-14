from extensions import db

class Videojuego(db.Model):
    __tablename__ = 'videojuegos'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    desarrollador = db.Column(db.String(100), nullable=False)
    año_lanzamiento = db.Column(db.Integer, nullable=False)
    genero = db.Column(db.String(50), nullable=False)
    plataforma = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    imagen = db.Column(db.String(500))
    
    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'desarrollador': self.desarrollador,
            'año_lanzamiento': self.año_lanzamiento,
            'genero': self.genero,
            'plataforma': self.plataforma,
            'precio': self.precio,
            'imagen': self.imagen
        }