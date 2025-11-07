from flask import Flask, jsonify
from flask_cors import CORS
from extensions import db, jwt
from datetime import timedelta
import os

# Configuración
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'clave-secreta-codespaces'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///videojuegos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY') or 'jwt-secreto-codespaces'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

# Habilitar CORS
CORS(app)

# Inicializar extensiones
db.init_app(app)
jwt.init_app(app)

# Importar modelos y controladores - CORREGIDO
from models.users_model import User
from models.videojuego import Videojuego
from controllers.users_controller import UsersController
from controllers.videojuegos_controller import VideojuegosController
# ================= RUTAS API =================

# Autenticación
app.add_url_rule('/api/auth/register', view_func=UsersController.register, methods=['POST'])
app.add_url_rule('/api/auth/login', view_func=UsersController.login, methods=['POST'])
app.add_url_rule('/api/auth/refresh', view_func=UsersController.refresh, methods=['POST'])
app.add_url_rule('/api/auth/profile', view_func=UsersController.profile, methods=['GET'])

# Videojuegos
app.add_url_rule('/api/videojuegos', view_func=VideojuegosController.get_videojuegos, methods=['GET'])
app.add_url_rule('/api/videojuegos', view_func=VideojuegosController.create_videojuego, methods=['POST'])
app.add_url_rule('/api/videojuegos/<int:videojuego_id>', view_func=VideojuegosController.get_videojuego, methods=['GET'])
app.add_url_rule('/api/videojuegos/<int:videojuego_id>', view_func=VideojuegosController.update_videojuego, methods=['PUT'])
app.add_url_rule('/api/videojuegos/<int:videojuego_id>', view_func=VideojuegosController.delete_videojuego, methods=['DELETE'])
app.add_url_rule('/api/videojuegos/search', view_func=VideojuegosController.search_videojuegos, methods=['GET'])

# Rutas básicas
@app.route('/')
def home():
    return jsonify({'message': '🚀 API Videojuegos - Usa /api/health para documentación'})

@app.route('/api/health')
def health_check():
    return jsonify({
        'status': 'healthy', 
        'message': 'API funcionando',
        'endpoints': ['/api/auth/*', '/api/videojuegos/*']
    })

# Inicializar BD
def init_db():
    with app.app_context():
        db.drop_all()
        db.create_all()
        
        # Admin por defecto
        from services.users_service import UsersService
        UsersService.create_user('admin@example.com', 'admin123', 'admin')
        
        # Videojuegos de ejemplo
        from services.videojuegos_service import VideojuegosService
        juegos = [
            {
                'titulo': 'The Legend of Zelda: Tears of the Kingdom',
                'desarrollador': 'Nintendo', 'año_lanzamiento': 2023,
                'genero': 'Acción-Aventura', 'plataforma': 'Nintendo Switch',
                'precio': 59.99,
                'imagen': 'https://assets.nintendo.com/image/upload/ar_16:9,c_lpad,w_656/b_white/f_auto/q_auto/ncom/software/switch/70010000063714/276a412988e07c4d55a2996c6d38abb408b464413b2dfeb44d2aa460b9f622e1'
            },
            {
                'titulo': 'Elden Ring', 'desarrollador': 'FromSoftware', 'año_lanzamiento': 2022,
                'genero': 'RPG de Acción', 'plataforma': 'PS5/Xbox Series X/PC', 'precio': 59.99,
                'imagen': 'https://upload.wikimedia.org/wikipedia/en/b/b9/Elden_Ring_Box_art.jpg'
            }
        ]
        
        for juego in juegos:
            VideojuegosService.create_videojuego(juego)
        
        print("✅ BD inicializada")

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 API en http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=True)