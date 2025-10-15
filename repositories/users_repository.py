from models.users_model import User
from extensions import db

class UserRepository:
    
    @staticmethod
    def find_by_email(email):
        return User.query.filter_by(email=email).first()
    
    @staticmethod
    def find_by_id(user_id):
        return User.query.get(user_id)
    
    @staticmethod
    def create_user(email, password, role='user'):
        if UserRepository.find_by_email(email):
            return None, "El email ya está registrado"
        
        user = User(email=email, role=role)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        return user, "Usuario creado exitosamente"
    
    @staticmethod
    def get_all_users():
        return User.query.all()