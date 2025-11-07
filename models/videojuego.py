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
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    
    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'desarrollador': self.desarrollador,
            'año_lanzamiento': self.año_lanzamiento,
            'genero': self.genero,
            'plataforma': self.plataforma,
            'precio': self.precio,
            'imagen': self.imagen,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Videojuego {self.titulo}>'