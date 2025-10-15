from flask import Blueprint, request, jsonify
from services.videojuegos_service import obtener_todos, obtener_por_id, agregar, actualizar, eliminar

# Creamos un Blueprint para separar las rutas relacionadas con videojuegos
videojuegos_bp = Blueprint("videojuegos", __name__, url_prefix="/videojuegos")


# Ruta para listar todos los videojuegos
@videojuegos_bp.route("/", methods=["GET"])
def listar():
    return jsonify(obtener_todos())

# Ruta para obtener un videojuego específico por su ID
@videojuegos_bp.route("/<int:id>", methods=["GET"])
def obtener(id):
    v = obtener_por_id(id)
    if v:
        return jsonify(v)
    return jsonify({"error": "Videojuego no encontrado"}), 404

# Ruta para crear un nuevo videojuego
@videojuegos_bp.route("/", methods=["POST"])
def crear():
    data = request.get_json()
    # Validamos que vengan todos los campos necesarios
    if not all(k in data for k in ("titulo", "genero", "plataforma", "rating")):
        return jsonify({"error": "Faltan campos obligatorios"}), 400
    return jsonify(agregar(data)), 201

# Ruta para actualizar un videojuego existente
@videojuegos_bp.route("/<int:id>", methods=["PUT"])
def editar(id):
    data = request.get_json()
    v = actualizar(id, data)
    if v:
        return jsonify(v)
    return jsonify({"error": "Videojuego no encontrado"}), 404

# Ruta para eliminar un videojuego
@videojuegos_bp.route("/<int:id>", methods=["DELETE"])
def borrar(id):
    if eliminar(id):
        return jsonify({"mensaje": "Videojuego eliminado"}), 200
    return jsonify({"error": "Videojuego no encontrado"}), 404
