from models.videojuego import Videojuego
from extensions import db

class VideojuegosService:
    @staticmethod
    def get_all_videojuegos():
        """Obtener todos los videojuegos"""
        return Videojuego.query.all()
    
    @staticmethod
    def get_videojuego_by_id(videojuego_id):
        """Obtener videojuego por ID"""
        return Videojuego.query.get(videojuego_id)
    
    @staticmethod
    def create_videojuego(videojuego_data):
        """Crear nuevo videojuego"""
        videojuego = Videojuego(**videojuego_data)
        db.session.add(videojuego)
        db.session.commit()
        return videojuego
    
    @staticmethod
    def update_videojuego(videojuego_id, update_data):
        """Actualizar videojuego"""
        videojuego = Videojuego.query.get(videojuego_id)
        if not videojuego:
            return None, 'Videojuego no encontrado'
        
        for key, value in update_data.items():
            if hasattr(videojuego, key):
                setattr(videojuego, key, value)
        
        db.session.commit()
        return videojuego, None
    
    @staticmethod
    def delete_videojuego(videojuego_id):
        """Eliminar videojuego"""
        videojuego = Videojuego.query.get(videojuego_id)
        if not videojuego:
            return False, 'Videojuego no encontrado'
        
        db.session.delete(videojuego)
        db.session.commit()
        return True, None
    
    @staticmethod
    def search_videojuegos(search_term):
        """Buscar videojuegos por título o desarrollador"""
        return Videojuego.query.filter(
            (Videojuego.titulo.ilike(f'%{search_term}%')) |
            (Videojuego.desarrollador.ilike(f'%{search_term}%'))
        ).all()