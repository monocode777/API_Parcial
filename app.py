from flask import Flask
from controllers.videojuegos_controller import videojuegos_bp
from models.videojuego import db
from config.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar base de datos
    db.init_app(app)

    # Crear las tablas si no existen
    with app.app_context():
        db.create_all()

    # Registrar rutas
    app.register_blueprint(videojuegos_bp, url_prefix="/videojuegos")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
