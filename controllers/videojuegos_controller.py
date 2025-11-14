from flask import jsonify
from services.videojuegos_service import VideojuegosService

class VideojuegosController:
    @staticmethod
    def get_videojuegos():
        try:
            videojuegos = VideojuegosService.get_all_videojuegos()
            return jsonify([v.to_dict() for v in videojuegos]), 200
        except Exception as e:
            return jsonify({'msg': f'Error: {str(e)}'}), 500