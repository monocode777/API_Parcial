from models.videojuego import Videojuego
from extensions import db

class VideojuegoService:
    
    @staticmethod
    def get_all_videojuegos():
        return Videojuego.query.all()
    
    @staticmethod
    def get_videojuego_by_id(videojuego_id):
        return Videojuego.query.get(videojuego_id)
    
    @staticmethod
    def create_videojuego(titulo, desarrollador, año_lanzamiento=None, genero=None, plataforma=None, precio=None):
        videojuego = Videojuego(
            titulo=titulo,
            desarrollador=desarrollador,
            año_lanzamiento=año_lanzamiento,
            genero=genero,
            plataforma=plataforma,
            precio=precio
        )
        
        db.session.add(videojuego)
        db.session.commit()
        
        return videojuego
    
    @staticmethod
    def update_videojuego(videojuego_id, **kwargs):
        videojuego = Videojuego.query.get(videojuego_id)
        if not videojuego:
            return None, "Videojuego no encontrado"
        
        for key, value in kwargs.items():
            if hasattr(videojuego, key):
                setattr(videojuego, key, value)
        
        db.session.commit()
        return videojuego, "Videojuego actualizado"
    
    @staticmethod
    def delete_videojuego(videojuego_id):
        videojuego = Videojuego.query.get(videojuego_id)
        if not videojuego:
            return False, "Videojuego no encontrado"
        
        db.session.delete(videojuego)
        db.session.commit()
        return True, "Videojuego eliminado"