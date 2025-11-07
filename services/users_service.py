from models.users_model import User
from extensions import db

class UsersService:
    @staticmethod
    def create_user(email, password, role='user'):
        """Crear nuevo usuario"""
        if User.query.filter_by(email=email).first():
            return None, 'El usuario ya existe'
        
        user = User(email=email, role=role)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        return user, None
    
    @staticmethod
    def authenticate_user(email, password):
        """Autenticar usuario"""
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            return user, None
        return None, 'Credenciales inválidas'
    
    @staticmethod
    def get_user_by_id(user_id):
        """Obtener usuario por ID"""
        return User.query.get(user_id)
    
    @staticmethod
    def get_user_by_email(email):
        """Obtener usuario por email"""
        return User.query.filter_by(email=email).first()