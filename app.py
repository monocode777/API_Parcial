from flask import Flask
from config.config import Config
from flask_sqlalchemy import SQLAlchemy
from controllers.videojuegos_controller import videojuegos_bp

# Inicializa la app Flask
app = Flask(__name__)

# Configuración de la app (se carga desde config/config.py)
app.config.from_object(Config)

# Inicializa SQLAlchemy para manejar la base de datos
db = SQLAlchemy(app)

# Crea todas las tablas si no existen (basado en los modelos)
with app.app_context():
    db.create_all()

# Registra el blueprint de videojuegos (rutas de la API)
app.register_blueprint(videojuegos_bp, url_prefix='/videojuegos')

# Punto de entrada principal
if __name__ == '__main__':
    app.run(debug=True)
