from flask import request, jsonify
from flask_jwt_extended import (
    create_access_token, create_refresh_token, 
    jwt_required, get_jwt_identity, get_jwt
)
from services.users_services import UserService
from models.users_model import TokenBlocklist
from extensions import db

class UsersController:
    
    @staticmethod
    def register():
        try:
            data = request.get_json()
            email = data.get('email')
            password = data.get('password')
            role = data.get('role', 'user')
            
            if not email or not password:
                return jsonify({'error': 'Email y contraseña son requeridos'}), 400
            
            user, message = UserService.register_user(email, password, role)
            
            if not user:
                return jsonify({'error': message}), 400
            
            return jsonify({
                'message': message,
                'user': user.to_dict()
            }), 201
            
        except Exception as e:
            return jsonify({'error': 'Error interno del servidor'}), 500
    
    @staticmethod
    def login():
        try:
            data = request.get_json()
            email = data.get('email')
            password = data.get('password')
            
            if not email or not password:
                return jsonify({'error': 'Email y contraseña son requeridos'}), 400
            
            user, message = UserService.authenticate_user(email, password)
            
            if not user:
                return jsonify({'error': message}), 401
            
            access_token = create_access_token(identity=str(user.id), additional_claims={"role": user.role})
            refresh_token = create_refresh_token(identity=user.id)
            
            return jsonify({
                'message': message,
                'access_token': access_token,
                'refresh_token': refresh_token,
                'user': user.to_dict()
            }), 200
            
        except Exception as e:
            return jsonify({'error': 'Error interno del servidor'}), 500
    
    @staticmethod
    @jwt_required(refresh=True)
    def refresh():
        try:
            current_user_id = get_jwt_identity()
            user, message = UserService.get_user_profile(current_user_id)
            
            if not user:
                return jsonify({'error': message}), 404
            
            access_token = create_access_token(identity=user.id, additional_claims={'role': user.role})
            
            return jsonify({
                'access_token': access_token
            }), 200
            
        except Exception as e:
            return jsonify({'error': 'Error interno del servidor'}), 500
    
    @staticmethod
    @jwt_required()
    def logout():
        try:
            jti = get_jwt()['jti']
            token_type = get_jwt()['type']
            user_id = get_jwt_identity()
            
            # Agregar token a la lista negra
            revoked_token = TokenBlocklist(
                jti=jti,
                token_type=token_type,
                user_id=user_id,
                expires=get_jwt()['exp']
            )
            
            db.session.add(revoked_token)
            db.session.commit()
            
            return jsonify({'message': 'Sesión cerrada exitosamente'}), 200
            
        except Exception as e:
            return jsonify({'error': 'Error interno del servidor'}), 500
    
    @staticmethod
    @jwt_required()
    def profile():
        try:
            current_user_id = get_jwt_identity()
            user, message = UserService.get_user_profile(current_user_id)
            
            if not user:
                return jsonify({'error': message}), 404
            
            return jsonify({
                'user': user.to_dict()
            }), 200
            
        except Exception as e:
            return jsonify({'error': 'Error interno del servidor'}), 500