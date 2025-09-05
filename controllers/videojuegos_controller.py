from flask import Blueprint, jsonify, request
import services.videojuegos_service as service

videojuegos_bp = Blueprint("videojuegos", __name__)

@videojuegos_bp.route("/", methods=["GET"])
def obtener_videojuegos():
    return jsonify(service.obtener_todos())

@videojuegos_bp.route("/<int:id>", methods=["GET"])
def obtener_videojuego(id):
    videojuego = service.obtener_por_id(id)
    if videojuego:
        return jsonify(videojuego)
    return jsonify({"error": "No encontrado"}), 404

@videojuegos_bp.route("/", methods=["POST"])
def agregar_videojuego():
    data = request.get_json()
    nuevo = service.agregar(data)
    return jsonify(nuevo), 201

@videojuegos_bp.route("/<int:id>", methods=["PUT"])
def actualizar_videojuego(id):
    data = request.get_json()
    actualizado = service.actualizar(id, data)
    if actualizado:
        return jsonify(actualizado)
    return jsonify({"error": "No encontrado"}), 404

@videojuegos_bp.route("/<int:id>", methods=["DELETE"])
def eliminar_videojuego(id):
    eliminado = service.eliminar(id)
    if eliminado:
        return jsonify({"mensaje": "Videojuego eliminado"})
    return jsonify({"error": "No encontrado"}), 404
