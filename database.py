from extensions import db

def init_db():
    # Crear todas las tablas
    db.create_all()
    
    # Crear usuario admin por defecto si no existe
    from models.users_model import User
    from services.users_services import UserService
    
    admin_user = User.query.filter_by(email='admin@example.com').first()
    if not admin_user:
        UserService.register_user('admin@example.com', 'admin123', 'admin')
        print("Usuario admin creado: admin@example.com / admin123")