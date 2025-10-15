from config.database import get_db_session
from models.videojuego import Videojuego

# Obtener todos los videojuegos
def obtener_todos():
    session = get_db_session()
    videojuegos = session.query(Videojuego).all()
    data = [v.to_dict() for v in videojuegos]
    session.close()
    return data

# Obtener un videojuego por ID
def obtener_por_id(id):
    session = get_db_session()
    v = session.query(Videojuego).get(id)
    data = v.to_dict() if v else None
    session.close()
    return data

# Agregar un nuevo videojuego a la base de datos
def agregar(data):
    session = get_db_session()
    nuevo = Videojuego(
        titulo=data["titulo"],
        genero=data["genero"],
        plataforma=data["plataforma"],
        rating=data["rating"],
    )
    session.add(nuevo)
    session.commit()
    data = nuevo.to_dict()
    session.close()
    return data

# Actualizar un videojuego existente
def actualizar(id, data):
    session = get_db_session()
    v = session.query(Videojuego).get(id)
    if v:
        v.titulo = data.get("titulo", v.titulo)
        v.genero = data.get("genero", v.genero)
        v.plataforma = data.get("plataforma", v.plataforma)
        v.rating = data.get("rating", v.rating)
        session.commit()
        result = v.to_dict()
    else:
        result = None
    session.close()
    return result

# Eliminar un videojuego
def eliminar(id):
    session = get_db_session()
    v = session.query(Videojuego).get(id)
    if v:
        session.delete(v)
        session.commit()
        session.close()
        return True
    session.close()
    return False
