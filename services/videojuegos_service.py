from models.videojuego import db, Videojuego

def obtener_todos():
    videojuegos = Videojuego.query.all()
    return [v.to_dict() for v in videojuegos]

def obtener_por_id(id):
    videojuego = Videojuego.query.get(id)
    return videojuego.to_dict() if videojuego else None

def agregar(videojuego_data):
    nuevo = Videojuego(
        titulo=videojuego_data["titulo"],
        genero=videojuego_data["genero"],
        plataforma=videojuego_data["plataforma"],
        rating=videojuego_data["rating"],
    )
    db.session.add(nuevo)
    db.session.commit()
    return nuevo.to_dict()

def actualizar(id, datos):
    videojuego = Videojuego.query.get(id)
    if not videojuego:
        return None
    videojuego.titulo = datos.get("titulo", videojuego.titulo)
    videojuego.genero = datos.get("genero", videojuego.genero)
    videojuego.plataforma = datos.get("plataforma", videojuego.plataforma)
    videojuego.rating = datos.get("rating", videojuego.rating)
    db.session.commit()
    return videojuego.to_dict()

def eliminar(id):
    videojuego = Videojuego.query.get(id)
    if not videojuego:
        return False
    db.session.delete(videojuego)
    db.session.commit()
    return True
