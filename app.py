from flask import render_template
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
import os

# Configuración
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'clave-secreta-codespaces'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///videojuegos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY') or 'jwt-secreto-codespaces'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

# Inicializar extensiones
db = SQLAlchemy(app)
jwt = JWTManager(app)

# Modelos
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Videojuego(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    desarrollador = db.Column(db.String(100), nullable=False)
    año_lanzamiento = db.Column(db.Integer)
    genero = db.Column(db.String(50))
    precio = db.Column(db.Float)

# Rutas de Autenticación
@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/home')
def dashboard_page():
    return render_template('home.html')


@app.route('/videojuegos')
def videojuegos_page():
    # Página del frontend para gestionar videojuegos (requiere token en cliente)
    return render_template('videojuegos.html')
@app.route('/api/auth/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Email y contraseña son requeridos'}), 400
        
        # Verificar si el usuario ya existe
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'El email ya está registrado'}), 400
        
        # Crear nuevo usuario
        user = User(email=email)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'message': 'Usuario registrado exitosamente',
            'user': {
                'id': user.id,
                'email': user.email,
                'role': user.role
            }
        }), 201
        
    except Exception as e:
        return jsonify({'error': 'Error interno del servidor'}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Email y contraseña son requeridos'}), 400
        
        user = User.query.filter_by(email=email).first()
        
        if not user or not user.check_password(password):
            return jsonify({'error': 'Credenciales inválidas'}), 401
        
        access_token = create_access_token(identity=str(user.id), additional_claims={'role': user.role})
        
        return jsonify({
            'message': 'Login exitoso',
            'access_token': access_token,
            'user': {
                'id': user.id,
                'email': user.email,
                'role': user.role
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Error interno del servidor'}), 500

@app.route('/api/auth/profile', methods=['GET'])
@jwt_required()
def profile():
    try:
        # get_jwt_identity() puede devolver una cadena si el token guarda el id como str
        current_user_id = get_jwt_identity()
        try:
            current_user_id = int(current_user_id)
        except Exception:
            # si no pudo castear, usar tal cual (SQLAlchemy acepta str para get también en algunos casos)
            pass
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        return jsonify({
            'user': {
                'id': user.id,
                'email': user.email,
                'role': user.role
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Error interno del servidor'}), 500

# Rutas de Videojuegos
@app.route('/api/videojuegos', methods=['GET'])
@jwt_required()
def get_videojuegos():
    try:
        videojuegos = Videojuego.query.all()
        return jsonify({
            'videojuegos': [{
                'id': v.id,
                'titulo': v.titulo,
                'desarrollador': v.desarrollador,
                'año_lanzamiento': v.año_lanzamiento,
                'genero': v.genero,
                'precio': v.precio
            } for v in videojuegos]
        }), 200
    except Exception as e:
        return jsonify({'error': 'Error interno del servidor'}), 500

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


@app.route('/api/videojuegos/<int:videojuego_id>', methods=['DELETE'])
@jwt_required()
def delete_videojuego(videojuego_id):
    try:
        claims = get_jwt()
        if claims.get('role') != 'admin':
            return jsonify({'error': 'Se requieren permisos de administrador'}), 403

        videojuego = Videojuego.query.get(videojuego_id)
        if not videojuego:
            return jsonify({'error': 'Videojuego no encontrado'}), 404

        db.session.delete(videojuego)
        db.session.commit()

        return jsonify({'message': 'Videojuego eliminado exitosamente'}), 200
    except Exception as e:
        return jsonify({'error': 'Error interno del servidor'}), 500


@app.route('/api/videojuegos/<int:videojuego_id>', methods=['PUT'])
@jwt_required()
def update_videojuego(videojuego_id):
    try:
        claims = get_jwt()
        if claims.get('role') != 'admin':
            return jsonify({'error': 'Se requieren permisos de administrador'}), 403

        videojuego = Videojuego.query.get(videojuego_id)
        if not videojuego:
            return jsonify({'error': 'Videojuego no encontrado'}), 404

        data = request.get_json() or {}

        # Actualizar solo campos presentes
        if 'titulo' in data:
            videojuego.titulo = data.get('titulo')
        if 'desarrollador' in data:
            videojuego.desarrollador = data.get('desarrollador')
        if 'año_lanzamiento' in data:
            videojuego.año_lanzamiento = data.get('año_lanzamiento')
        if 'genero' in data:
            videojuego.genero = data.get('genero')
        if 'precio' in data:
            videojuego.precio = data.get('precio')

        db.session.commit()

        return jsonify({
            'message': 'Videojuego actualizado exitosamente',
            'videojuego': {
                'id': videojuego.id,
                'titulo': videojuego.titulo,
                'desarrollador': videojuego.desarrollador,
                'año_lanzamiento': videojuego.año_lanzamiento,
                'genero': videojuego.genero,
                'precio': videojuego.precio
            }
        }), 200
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