from flask import Flask
from config.config import Config
from extensions import db  # Importamos db desde extensions
from controllers.videojuegos_controller import videojuegos_bp

app = Flask(__name__)
app.config.from_object(Config)

# Inicializar db con la app
db.init_app(app)

# Crear tablas
with app.app_context():
    db.create_all()

# Registrar blueprint
app.register_blueprint(videojuegos_bp, url_prefix="/videojuegos")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
