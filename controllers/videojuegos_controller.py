from flask import Blueprint, request, jsonify
from services.videojuegos_service import obtener_todos, obtener_por_id, agregar, actualizar, eliminar

videojuegos_bp = Blueprint('videojuegos', __name__)

# ✅ Validación básica de datos
def validar_datos(data, actualizar=False):
    errores = []

    # En POST todos los campos son obligatorios
    if not actualizar:
        if "titulo" not in data or not data["titulo"]:
            errores.append("El campo 'titulo' es obligatorio")
        if "genero" not in data or not data["genero"]:
            errores.append("El campo 'genero' es obligatorio")
        if "plataforma" not in data or not data["plataforma"]:
            errores.append("El campo 'plataforma' es obligatorio")
        if "rating" not in data:
            errores.append("El campo 'rating' es obligatorio")
    else:
        # En PUT, solo valida los campos que llegan
        if "rating" in data and not isinstance(data["rating"], (int, float)):
            errores.append("El campo 'rating' debe ser numérico")

    # Validación de rating
    if "rating" in data:
        try:
            rating = float(data["rating"])
            if rating < 0 or rating > 10:
                errores.append("El campo 'rating' debe estar entre 0 y 10")
        except (ValueError, TypeError):
            errores.append("El campo 'rating' debe ser un número")

    return errores


# 📌 GET todos
@videojuegos_bp.route('/', methods=['GET'])
def get_videojuegos():
    videojuegos = obtener_todos()
    return jsonify(videojuegos), 200


# 📌 GET por ID
@videojuegos_bp.route('/<int:id>', methods=['GET'])
def get_videojuego(id):
    videojuego = obtener_por_id(id)
    if videojuego:
        return jsonify(videojuego), 200
    return jsonify({'error': 'Videojuego no encontrado'}), 404


# 📌 POST (crear)
@videojuegos_bp.route('/', methods=['POST'])
def create_videojuego():
    data = request.get_json()

    if not data:
        return jsonify({"error": "El cuerpo de la petición no puede estar vacío"}), 400

    errores = validar_datos(data, actualizar=False)
    if errores:
        return jsonify({"errores": errores}), 400

    nuevo = agregar(data)
    return jsonify(nuevo), 201


# 📌 PUT (actualizar)
@videojuegos_bp.route('/<int:id>', methods=['PUT'])
def update_videojuego(id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "El cuerpo de la petición no puede estar vacío"}), 400

    errores = validar_datos(data, actualizar=True)
    if errores:
        return jsonify({"errores": errores}), 400

    actualizado = actualizar(id, data)
    if actualizado:
        return jsonify(actualizado), 200
    return jsonify({'error': 'Videojuego no encontrado'}), 404


# 📌 DELETE
@videojuegos_bp.route('/<int:id>', methods=['DELETE'])
def delete_videojuego(id):
    eliminado = eliminar(id)
    if eliminado:
        return jsonify({'message': 'Videojuego eliminado'}), 200
    return jsonify({'error': 'Videojuego no encontrado'}), 404
