from repositories.users_repository import UserRepository
from flask import current_app

class UserService:
    
    @staticmethod
    def register_user(email, password, role='user'):
        return UserRepository.create_user(email, password, role)
    
    @staticmethod
    def authenticate_user(email, password):
        user = UserRepository.find_by_email(email)
        if not user or not user.check_password(password):
            return None, "Credenciales inválidas"
        
        if not user.is_active:
            return None, "Cuenta desactivada"
        
        return user, "Autenticación exitosa"
    
    @staticmethod
    def get_user_profile(user_id):
        user = UserRepository.find_by_id(user_id)
        if not user:
            return None, "Usuario no encontrado"
        return user, "Perfil obtenido"