from flask import jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from services.users_service import UsersService

class UsersController:
    @staticmethod
    def register():
        try:
            data = request.get_json()
            email = data.get('email')
            password = data.get('password')
            
            if not email or not password:
                return jsonify({'msg': 'Email y contraseña son requeridos'}), 400
            
            user, error = UsersService.create_user(email, password)
            if error:
                return jsonify({'msg': error}), 400
            
            return jsonify({
                'msg': 'Usuario registrado exitosamente',
                'user': user.to_dict()
            }), 201
            
        except Exception as e:
            return jsonify({'msg': f'Error en el servidor: {str(e)}'}), 500

    @staticmethod
    def login():
        try:
            data = request.get_json()
            email = data.get('email')
            password = data.get('password')
            
            if not email or not password:
                return jsonify({'msg': 'Email y contraseña son requeridos'}), 400
            
            user, error = UsersService.authenticate_user(email, password)
            if error:
                return jsonify({'msg': error}), 401
            
            access_token = create_access_token(identity=user.id)
            
            return jsonify({
                'access_token': access_token,
                'user': user.to_dict()
            }), 200
            
        except Exception as e:
            return jsonify({'msg': f'Error en el servidor: {str(e)}'}), 500

    @staticmethod
    @jwt_required()
    def profile():
        try:
            user_id = get_jwt_identity()
            user = UsersService.get_user_by_id(user_id)
            return jsonify({'user': user.to_dict()}), 200
        except Exception as e:
            return jsonify({'msg': f'Error: {str(e)}'}), 500