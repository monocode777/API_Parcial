from flask import render_template
from flask import Flask, jsonify, request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
from extensions import db, jwt
from datetime import timedelta
import os
from sqlalchemy.exc import OperationalError

# Configuración

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'clave-secreta-codespaces'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///videojuegos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY') or 'jwt-secreto-codespaces'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

# Inicializar extensiones (usar extensiones centralizadas)
db.init_app(app)
jwt.init_app(app)

from models.users_model import User
from models.videojuego import Videojuego

# Registrar rutas usando los controllers
from controllers.users_controller import UsersController
from controllers.videojuegos_controller import VideojuegosController

# Rutas del frontend (render templates)
app.add_url_rule('/login', endpoint='login_page', view_func=lambda: render_template('login.html'), methods=['GET'])
app.add_url_rule('/register', endpoint='register_page', view_func=lambda: render_template('register.html'), methods=['GET'])
app.add_url_rule('/home', endpoint='dashboard_page', view_func=lambda: render_template('home.html'), methods=['GET'])
app.add_url_rule('/videojuegos', endpoint='videojuegos_page', view_func=lambda: render_template('videojuegos.html'), methods=['GET'])

# Rutas de autenticación (UsersController)
app.add_url_rule('/api/auth/register', endpoint='api_register', view_func=UsersController.register, methods=['POST'])
app.add_url_rule('/api/auth/login', endpoint='api_login', view_func=UsersController.login, methods=['POST'])
app.add_url_rule('/api/auth/refresh', endpoint='api_refresh', view_func=UsersController.refresh, methods=['POST'])
app.add_url_rule('/api/auth/logout', endpoint='api_logout', view_func=UsersController.logout, methods=['POST'])
app.add_url_rule('/api/auth/profile', endpoint='api_profile', view_func=UsersController.profile, methods=['GET'])

# Rutas de videojuegos (VideojuegosController)
app.add_url_rule('/api/videojuegos', endpoint='get_videojuegos', view_func=VideojuegosController.get_videojuegos, methods=['GET'])
app.add_url_rule('/api/videojuegos', endpoint='create_videojuego', view_func=VideojuegosController.create_videojuego, methods=['POST'])
app.add_url_rule('/api/videojuegos/<int:videojuego_id>', endpoint='get_videojuego', view_func=VideojuegosController.get_videojuego, methods=['GET'])
app.add_url_rule('/api/videojuegos/<int:videojuego_id>', endpoint='update_videojuego', view_func=VideojuegosController.update_videojuego, methods=['PUT'])
app.add_url_rule('/api/videojuegos/<int:videojuego_id>', endpoint='delete_videojuego', view_func=VideojuegosController.delete_videojuego, methods=['DELETE'])

# Ruta de salud
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy', 
        'message': 'API funcionando correctamente',
        'endpoints': {
            'auth': {
                'POST /api/auth/register': 'Registrar usuario',
                'POST /api/auth/login': 'Iniciar sesión',
                'GET /api/auth/profile': 'Perfil de usuario (requiere token)'
            },
            'videojuegos': {
                'GET /api/videojuegos': 'Listar videojuegos',
                'POST /api/videojuegos': 'Crear videojuego (requiere admin)'
            }
        }
    })

# Ruta de prueba sin API prefix
@app.route('/')
def home():
    return '''
    <html>
        <head>
            <title>API Videojuegos</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                .endpoint { background: #f5f5f5; padding: 10px; margin: 10px 0; }
            </style>
        </head>
        <body>
            <h1>🚀 API de Videojuegos Funcionando</h1>
            <p>La API está corriendo correctamente. Prueba estos endpoints:</p>
            
            <div class="endpoint">
                <strong>GET /api/health</strong> - Estado de la API
            </div>
            
            <div class="endpoint">
                <strong>POST /api/auth/register</strong> - Registrar usuario
            </div>
            
            <div class="endpoint">
                <strong>POST /api/auth/login</strong> - Iniciar sesión
            </div>
            
            <div class="endpoint">
                <strong>GET /api/videojuegos</strong> - Listar videojuegos
            </div>
            
            <p><a href="/api/health">Ver todos los endpoints</a></p>
        </body>
    </html>
    '''

# Manejador de errores
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Endpoint no encontrado',
        'available_endpoints': [
            'GET  /',
            'GET  /api/health',
            'POST /api/auth/register', 
            'POST /api/auth/login',
            'GET  /api/auth/profile',
            'GET  /api/videojuegos',
            'POST /api/videojuegos'
        ]
    }), 404

# Inicializar base de datos
def init_db():
    with app.app_context():
        # Eliminar todas las tablas existentes
        db.drop_all()
        # Crear todas las tablas desde cero
        db.create_all()
        
        # Crear usuario admin por defecto
        admin = User(email='admin@example.com', role='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        
        # Agregar videojuegos de ejemplo
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
                'titulo': 'Red Dead Redemption 2',
                'desarrollador': 'Rockstar Games',
                'año_lanzamiento': 2018,
                'genero': 'Acción-Aventura',
                'plataforma': 'PS4/Xbox One/PC',
                'precio': 49.99,
                'imagen': 'https://upload.wikimedia.org/wikipedia/en/4/44/Red_Dead_Redemption_II.jpg'
            },
            {
                'titulo': 'Cyberpunk 2077',
                'desarrollador': 'CD Projekt Red',
                'año_lanzamiento': 2020,
                'genero': 'RPG',
                'plataforma': 'PS4/Xbox One/PC',
                'precio': 49.99,
                'imagen': 'https://upload.wikimedia.org/wikipedia/en/9/9f/Cyberpunk_2077_box_art.jpg'
            }
        ]
        
        for juego_data in juegos:
            juego = Videojuego(**juego_data)
            db.session.add(juego)
        
        db.session.commit()
        print("✅ Base de datos inicializada con datos de ejemplo")

if __name__ == '__main__':
    init_db()
    
    port = int(os.environ.get('PORT', 5000))
    host = '0.0.0.0'
    
    print(f" Servidor iniciado en http://{host}:{port}")
    print(" Endpoints disponibles:")
    print("   GET  / - Página principal")
    print("   GET  /api/health - Estado de la API")
    print("   POST /api/auth/register - Registrar usuario")
    print("   POST /api/auth/login - Iniciar sesión")
    print("   GET  /api/videojuegos - Listar videojuegos")
    
    app.run(host=host, port=port, debug=True)