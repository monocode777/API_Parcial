from flask import Flask
from config import Config
from extensions import db
from controllers.videojuegos_controller import videojuegos_bp

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

# Ejecutamos la aplicación (disponible en el puerto 5000)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
