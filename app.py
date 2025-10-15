from flask import Flask
from flask_jwt_extended import JWTManager
from extensions import db
from controllers.videojuegos_controller import videojuegos_bp
from controllers.users_controller import user_bp
from config.jwt import (
    JWT_SECRET_KEY,
    JWT_TOKEN_LOCATION,
    JWT_ACCESS_TOKEN_EXPIRES,
    JWT_HEADER_NAME,
    JWT_HEADER_TYPE
)

app = Flask(__name__)

# 🔧 Configuración base de datos
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# 🔐 Configuración JWT
app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
app.config["JWT_TOKEN_LOCATION"] = JWT_TOKEN_LOCATION
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = JWT_ACCESS_TOKEN_EXPIRES
app.config["JWT_HEADER_NAME"] = JWT_HEADER_NAME
app.config["JWT_HEADER_TYPE"] = JWT_HEADER_TYPE

jwt_manager = JWTManager(app)

# Inicialización de base de datos
db.init_app(app)

# Registro de Blueprints
app.register_blueprint(user_bp, url_prefix="/users")
app.register_blueprint(videojuegos_bp, url_prefix="/videojuegos")

# Creación de tablas
with app.app_context():
    db.create_all()

# Ejecución del servidor
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
