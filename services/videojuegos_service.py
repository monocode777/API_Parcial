from models.videojuego import Videojuego
from config.database import get_db_session

def obtener_todos():
    db = get_db_session()
    videojuegos = db.query(Videojuego).all()
    resultado = [
        {
            "id": v.id,
            "titulo": v.titulo,
            "genero": v.genero,
            "plataforma": v.plataforma,
            "rating": v.rating
        }
        for v in videojuegos
    ]
    db.close()
    return resultado

def obtener_por_id(id):
    db = get_db_session()
    v = db.query(Videojuego).filter(Videojuego.id == id).first()
    db.close()
    if v:
        return {
            "id": v.id,
            "titulo": v.titulo,
            "genero": v.genero,
            "plataforma": v.plataforma,
            "rating": v.rating
        }
    return None

def agregar(data):
    db = get_db_session()
    nuevo = Videojuego(**data)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    db.close()
    return {"mensaje": "Videojuego agregado correctamente", "id": nuevo.id}

def actualizar(id, data):
    db = get_db_session()
    v = db.query(Videojuego).filter(Videojuego.id == id).first()
    if not v:
        db.close()
        return None
    for key, value in data.items():
        setattr(v, key, value)
    db.commit()
    db.refresh(v)
    db.close()
    return {"mensaje": "Videojuego actualizado", "id": v.id}

def eliminar(id):
    db = get_db_session()
    v = db.query(Videojuego).filter(Videojuego.id == id).first()
    if not v:
        db.close()
        return False
    db.delete(v)
    db.commit()
    db.close()
    return True
