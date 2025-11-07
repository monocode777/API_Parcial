from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.videojuegos_service import VideojuegosService
from services.users_service import UsersService

class VideojuegosController:
    @staticmethod
    def get_videojuegos():
        try:
            videojuegos = VideojuegosService.get_all_videojuegos()
            return jsonify([v.to_dict() for v in videojuegos]), 200
        except Exception as e:
            return jsonify({'msg': f'Error obteniendo videojuegos: {str(e)}'}), 500

    @staticmethod
    @jwt_required()
    def create_videojuego():
        try:
            current_user_id = get_jwt_identity()
            user = UsersService.get_user_by_id(current_user_id)
            
            # Verificar si es admin
            if user.role != 'admin':
                return jsonify({'msg': 'Se requieren permisos de administrador'}), 403
            
            data = request.get_json()
            if not data:
                return jsonify({'msg': 'No se proporcionaron datos'}), 400
            
            # Validar campos requeridos
            required_fields = ['titulo', 'desarrollador', 'año_lanzamiento', 'genero', 'plataforma', 'precio']
            for field in required_fields:
                if field not in data:
                    return jsonify({'msg': f'Campo requerido faltante: {field}'}), 400
            
            videojuego = VideojuegosService.create_videojuego(data)
            return jsonify({
                'msg': 'Videojuego creado exitosamente',
                'videojuego': videojuego.to_dict()
            }), 201
            
        except Exception as e:
            return jsonify({'msg': f'Error creando videojuego: {str(e)}'}), 500

    @staticmethod
    def get_videojuego(videojuego_id):
        try:
            videojuego = VideojuegosService.get_videojuego_by_id(videojuego_id)
            if not videojuego:
                return jsonify({'msg': 'Videojuego no encontrado'}), 404
            
            return jsonify({
                'videojuego': videojuego.to_dict()
            }), 200
            
        except Exception as e:
            return jsonify({'msg': f'Error obteniendo videojuego: {str(e)}'}), 500

    @staticmethod
    @jwt_required()
    def update_videojuego(videojuego_id):
        try:
            current_user_id = get_jwt_identity()
            user = UsersService.get_user_by_id(current_user_id)
            
            # Verificar si es admin
            if user.role != 'admin':
                return jsonify({'msg': 'Se requieren permisos de administrador'}), 403
            
            data = request.get_json()
            if not data:
                return jsonify({'msg': 'No se proporcionaron datos'}), 400
            
            videojuego, error = VideojuegosService.update_videojuego(videojuego_id, data)
            if error:
                return jsonify({'msg': error}), 404
            
            return jsonify({
                'msg': 'Videojuego actualizado exitosamente',
                'videojuego': videojuego.to_dict()
            }), 200
            
        except Exception as e:
            return jsonify({'msg': f'Error actualizando videojuego: {str(e)}'}), 500

    @staticmethod
    @jwt_required()
    def delete_videojuego(videojuego_id):
        try:
            current_user_id = get_jwt_identity()
            user = UsersService.get_user_by_id(current_user_id)
            
            # Verificar si es admin
            if user.role != 'admin':
                return jsonify({'msg': 'Se requieren permisos de administrador'}), 403
            
            success, error = VideojuegosService.delete_videojuego(videojuego_id)
            if error:
                return jsonify({'msg': error}), 404
            
            return jsonify({'msg': 'Videojuego eliminado exitosamente'}), 200
            
        except Exception as e:
            return jsonify({'msg': f'Error eliminando videojuego: {str(e)}'}), 500

    @staticmethod
    def search_videojuegos():
        try:
            search_term = request.args.get('q', '')
            if not search_term:
                return jsonify({'msg': 'Término de búsqueda requerido'}), 400
            
            videojuegos = VideojuegosService.search_videojuegos(search_term)
            return jsonify([v.to_dict() for v in videojuegos]), 200
            
        except Exception as e:
            return jsonify({'msg': f'Error buscando videojuegos: {str(e)}'}), 500