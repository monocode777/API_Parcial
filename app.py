from flask import Flask
from config.config import Config
from config.jwt import *
from flask_jwt_extended import JWTManager
from extensions import db
from flask import Flask
from controllers.videojuegos_controller import videojuegos_bp
from controllers.users_controller import user_bp


app = Flask(__name__)

# Configurar JWT
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
app.config['JWT_TOKEN_LOCATION'] = JWT_TOKEN_LOCATION
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = JWT_ACCESS_TOKEN_EXPIRES
app.config['JWT_HEADER_NAME'] = JWT_HEADER_NAME
app.config['JWT_HEADER_TYPE'] = JWT_HEADER_TYPE

jwt = JWTManager(app)


# Registrar el blueprint de videojuegos
app.register_blueprint(videojuegos_bp)
app.register_blueprint(user_bp)

if __name__ == "__main__":
    app.run(debug=True)

# Creamos la aplicación Flask
app = Flask(__name__)

# Cargamos la configuración desde config.py
app.config.from_object(Config)

# Inicializamos la extensión de base de datos (SQLAlchemy)
db.init_app(app)

# Creamos las tablas si no existen
with app.app_context():
    db.create_all()

# Registramos el "blueprint" de videojuegos en la ruta /videojuegos
app.register_blueprint(videojuegos_bp, url_prefix="/videojuegos")

@app.route('/api/videojuegos', methods=['POST'])
@jwt_required()
def create_videojuego():
    try:
        claims = get_jwt()
        if claims.get('role') != 'admin':
            return jsonify({'error': 'Se requieren permisos de administrador'}), 403
        
        data = request.get_json()
        
        if not data.get('titulo') or not data.get('desarrollador'):
            return jsonify({'error': 'Título y desarrollador son requeridos'}), 400
        
        videojuego = Videojuego(
            titulo=data['titulo'],
            desarrollador=data['desarrollador'],
            año_lanzamiento=data.get('año_lanzamiento'),
            genero=data.get('genero'),
            precio=data.get('precio')
        )
        
        db.session.add(videojuego)
        db.session.commit()
        
        return jsonify({
            'message': 'Videojuego creado exitosamente',
            'videojuego': {
                'id': videojuego.id,
                'titulo': videojuego.titulo,
                'desarrollador': videojuego.desarrollador,
                'año_lanzamiento': videojuego.año_lanzamiento,
                'genero': videojuego.genero,
                'precio': videojuego.precio
            }
        }), 201
        
    except Exception as e:
        return jsonify({'error': 'Error interno del servidor'}), 500

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
        db.create_all()
        
        # Crear usuario admin por defecto si no existe
        admin_user = User.query.filter_by(email='admin@example.com').first()
        if not admin_user:
            admin = User(email='admin@example.com', role='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("✅ Usuario admin creado: admin@example.com / admin123")
        
        # Crear algunos videojuegos de ejemplo si no existen
        if Videojuego.query.count() == 0:
            videojuegos = [
                Videojuego(titulo='The Legend of Zelda', desarrollador='Nintendo', año_lanzamiento=2017, genero='Aventura', precio=59.99),
                Videojuego(titulo='God of War', desarrollador='Santa Monica Studio', año_lanzamiento=2018, genero='Acción', precio=49.99),
                Videojuego(titulo='Minecraft', desarrollador='Mojang', año_lanzamiento=2011, genero='Sandbox', precio=26.95)
            ]
            db.session.add_all(videojuegos)
            db.session.commit()
            print(" Videojuegos de ejemplo creados")

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
