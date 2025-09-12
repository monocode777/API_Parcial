from extensions import db
from models.videojuego import Videojuego

# Obtener todos los videojuegos
def obtener_todos():
    return [v.to_dict() for v in Videojuego.query.all()]

# Obtener un videojuego por ID
def obtener_por_id(id):
    v = Videojuego.query.get(id)
    return v.to_dict() if v else None

# Agregar un nuevo videojuego a la base de datos
def agregar(data):
    nuevo = Videojuego(
        titulo=data["titulo"],
        genero=data["genero"],
        plataforma=data["plataforma"],
        rating=data["rating"],
    )
    db.session.add(nuevo)   # lo añadimos a la sesión
    db.session.commit()     # guardamos en la base de datos
    return nuevo.to_dict()

# Actualizar un videojuego existente
def actualizar(id, data):
    v = Videojuego.query.get(id)
    if v:
        v.titulo = data.get("titulo", v.titulo)
        v.genero = data.get("genero", v.genero)
        v.plataforma = data.get("plataforma", v.plataforma)
        v.rating = data.get("rating", v.rating)
        db.session.commit()
        return v.to_dict()
    return None

# Eliminar un videojuego
def eliminar(id):
    v = Videojuego.query.get(id)
    if v:
        db.session.delete(v)
        db.session.commit()
        return True
    return False
