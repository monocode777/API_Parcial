from models.users_model import User
from extensions import db

class UsersService:
    @staticmethod
    def create_user(email, password, role='user'):
        if User.query.filter_by(email=email).first():
            return None, 'El usuario ya existe'
        
        user = User(email=email, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user, None
    
    @staticmethod
    def authenticate_user(email, password):
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            return user, None
        return None, 'Credenciales inválidas'
    
    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(user_id)