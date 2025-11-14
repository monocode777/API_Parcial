from flask import Flask, jsonify
from flask_cors import CORS
from extensions import db, jwt
from datetime import timedelta
import os

# Configuración
app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave-secreta-api'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///videojuegos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'jwt-secreto-api'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

# CORS para desarrollo
CORS(app)

# Inicializar extensiones
db.init_app(app)
jwt.init_app(app)

# Importar controladores
from controllers.users_controller import UsersController
from controllers.videojuegos_controller import VideojuegosController

# ================= RUTAS API =================
app.add_url_rule('/api/auth/register', view_func=UsersController.register, methods=['POST'])
app.add_url_rule('/api/auth/login', view_func=UsersController.login, methods=['POST'])
app.add_url_rule('/api/auth/profile', view_func=UsersController.profile, methods=['GET'])
app.add_url_rule('/api/videojuegos', view_func=VideojuegosController.get_videojuegos, methods=['GET'])

@app.route('/')
def home():
    return jsonify({'message': '🚀 API Videojuegos'})

@app.route('/api/health')
def health_check():
    return jsonify({'status': 'healthy', 'message': 'API funcionando'})

# Inicializar BD
def init_db():
    with app.app_context():
        db.drop_all()
        db.create_all()
        
        # Crear admin
        from services.users_service import UsersService
        UsersService.create_user('admin@example.com', 'admin123', 'admin')
        
        # Videojuegos de ejemplo
        from services.videojuegos_service import VideojuegosService
        juegos = [
            {
                'titulo': 'The Legend of Zelda: Tears of the Kingdom',
                'desarrollador': 'Nintendo',
                'año_lanzamiento': 2023,
                'genero': 'Acción-Aventura',
                'plataforma': 'Nintendo Switch',
                'precio': 59.99,
                'imagen': 'https://assets.nintendo.com/image/upload/ar_16:9,c_lpad,w_656/b_white/f_auto/q_auto/ncom/software/switch/70010000063714/276a412988e07c4d55a2996c6d38abb408b464413b2dfeb44d2aa460b9f622e1'
            },
            {
                'titulo': 'Elden Ring',
                'desarrollador': 'FromSoftware',
                'año_lanzamiento': 2022,
                'genero': 'RPG',
                'plataforma': 'Multiplataforma',
                'precio': 59.99,
                'imagen': 'https://upload.wikimedia.org/wikipedia/en/b/b9/Elden_Ring_Box_art.jpg'
            }
        ]
        
        for juego in juegos:
            VideojuegosService.create_videojuego(juego)
        
        print("✅ Base de datos inicializada")

if __name__ == '__main__':
    init_db()
    print("🚀 API Backend iniciada en http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)