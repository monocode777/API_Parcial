from flask import Flask, jsonify
from config import config
from extensions import db, jwt
from controllers.users_controller import UsersController
from controllers.videojuegos_controller import VideojuegosController
import jwt as pyjwt

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Inicializar extensiones
    db.init_app(app)
    jwt.init_app(app)
    
    # Importar y registrar callbacks JWT
    from jwt import check_if_token_revoked, user_lookup_callback
    
    # Rutas de autenticación
    app.add_url_rule('/api/auth/register', view_func=UsersController.register, methods=['POST'])
    app.add_url_rule('/api/auth/login', view_func=UsersController.login, methods=['POST'])
    app.add_url_rule('/api/auth/refresh', view_func=UsersController.refresh, methods=['POST'])
    app.add_url_rule('/api/auth/logout', view_func=UsersController.logout, methods=['POST'])
    app.add_url_rule('/api/auth/profile', view_func=UsersController.profile, methods=['GET'])
    
    # Rutas de videojuegos
    app.add_url_rule('/api/videojuegos', view_func=VideojuegosController.get_videojuegos, methods=['GET'])
    app.add_url_rule('/api/videojuegos/<int:videojuego_id>', view_func=VideojuegosController.get_videojuego, methods=['GET'])
    app.add_url_rule('/api/videojuegos', view_func=VideojuegosController.create_videojuego, methods=['POST'])
    app.add_url_rule('/api/videojuegos/<int:videojuego_id>', view_func=VideojuegosController.update_videojuego, methods=['PUT'])
    app.add_url_rule('/api/videojuegos/<int:videojuego_id>', view_func=VideojuegosController.delete_videojuego, methods=['DELETE'])
    
    # Ruta de verificación de salud
    @app.route('/api/health')
    def health_check():
        return jsonify({'status': 'healthy', 'message': 'API funcionando correctamente'})
    
    # Manejador de errores global
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Endpoint no encontrado'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Error interno del servidor'}), 500
    
    # Crear tablas en la base de datos
    with app.app_context():
        db.create_all()
        from database import init_db
        init_db()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)