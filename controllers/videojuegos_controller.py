from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from services.videojuegos_service import VideojuegoService

class VideojuegosController:
    
    @staticmethod
    def get_videojuegos():
        try:
            videojuegos = VideojuegoService.get_all_videojuegos()
            return jsonify({
                'videojuegos': [v.to_dict() for v in videojuegos]
            }), 200
        except Exception as e:
            return jsonify({'error': 'Error interno del servidor'}), 500
    
    @staticmethod
    def get_videojuego(videojuego_id):
        try:
            videojuego = VideojuegoService.get_videojuego_by_id(videojuego_id)
            if not videojuego:
                return jsonify({'error': 'Videojuego no encontrado'}), 404
            
            return jsonify({
                'videojuego': videojuego.to_dict()
            }), 200
        except Exception as e:
            return jsonify({'error': 'Error interno del servidor'}), 500
    
    @staticmethod
    @jwt_required()
    def create_videojuego():
        try:
            claims = get_jwt()
            if claims.get('role') != 'admin':
                return jsonify({'error': 'Se requieren permisos de administrador'}), 403
            
            data = request.get_json()
            required_fields = ['titulo', 'desarrollador']
            
            for field in required_fields:
                if field not in data or not data[field]:
                    return jsonify({'error': f'El campo {field} es requerido'}), 400
            
            videojuego = VideojuegoService.create_videojuego(
                titulo=data['titulo'],
                desarrollador=data['desarrollador'],
                año_lanzamiento=data.get('año_lanzamiento'),
                genero=data.get('genero'),
                plataforma=data.get('plataforma'),
                precio=data.get('precio')
            )
            
            return jsonify({
                'message': 'Videojuego creado exitosamente',
                'videojuego': videojuego.to_dict()
            }), 201
            
        except Exception as e:
            return jsonify({'error': 'Error interno del servidor'}), 500
    
    @staticmethod
    @jwt_required()
    def update_videojuego(videojuego_id):
        try:
            claims = get_jwt()
            if claims.get('role') != 'admin':
                return jsonify({'error': 'Se requieren permisos de administrador'}), 403
            
            data = request.get_json()
            allowed_fields = ['titulo', 'desarrollador', 'año_lanzamiento', 'genero', 'plataforma', 'precio']
            update_data = {}
            
            for field in allowed_fields:
                if field in data:
                    update_data[field] = data[field]
            
            videojuego, message = VideojuegoService.update_videojuego(videojuego_id, **update_data)
            
            if not videojuego:
                return jsonify({'error': message}), 404
            
            return jsonify({
                'message': message,
                'videojuego': videojuego.to_dict()
            }), 200
            
        except Exception as e:
            return jsonify({'error': 'Error interno del servidor'}), 500
    
    @staticmethod
    @jwt_required()
    def delete_videojuego(videojuego_id):
        try:
            claims = get_jwt()
            if claims.get('role') != 'admin':
                return jsonify({'error': 'Se requieren permisos de administrador'}), 403
            
            success, message = VideojuegoService.delete_videojuego(videojuego_id)
            
            if not success:
                return jsonify({'error': message}), 404
            
            return jsonify({
                'message': message
            }), 200
            
        except Exception as e:
            return jsonify({'error': 'Error interno del servidor'}), 500