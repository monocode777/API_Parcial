from app import app, db, Videojuego

GAMES = [
    {
        'titulo': 'Hollow Knight',
        'desarrollador': 'Team Cherry',
        'año_lanzamiento': 2017,
        'genero': 'Metroidvania',
        'precio': 14.99,
        'imagen': 'https://images.unsplash.com/photo-1616401781964-5c3f1d6f0a9a?auto=format&fit=crop&w=800&q=60'
    },
    {
        'titulo': 'Stardew Valley',
        'desarrollador': 'ConcernedApe',
        'año_lanzamiento': 2016,
        'genero': 'Simulación',
        'precio': 14.99,
        'imagen': 'https://images.unsplash.com/photo-1526318472351-c75fcf070dd6?auto=format&fit=crop&w=800&q=60'
    },
    {
        'titulo': 'Celeste',
        'desarrollador': 'Matt Makes Games',
        'año_lanzamiento': 2018,
        'genero': 'Plataformas',
        'precio': 19.99,
        'imagen': 'https://images.unsplash.com/photo-1511512578047-dfb367046420?auto=format&fit=crop&w=800&q=60'
    },
    {
        'titulo': 'Hades',
        'desarrollador': 'Supergiant Games',
        'año_lanzamiento': 2020,
        'genero': 'Roguelike',
        'precio': 24.99,
        'imagen': 'https://images.unsplash.com/photo-1539533981657-4b1f3c6f6c2a?auto=format&fit=crop&w=800&q=60'
    },
    {
        'titulo': 'Disco Elysium',
        'desarrollador': 'ZA/UM',
        'año_lanzamiento': 2019,
        'genero': 'RPG',
        'precio': 39.99,
        'imagen': 'https://images.unsplash.com/photo-1508898578281-774ac4893a12?auto=format&fit=crop&w=800&q=60'
    }
]

with app.app_context():
    for g in GAMES:
        # Evitar duplicados por título
        existing = Videojuego.query.filter_by(titulo=g['titulo']).first()
        if existing:
            print(f"Existe: {g['titulo']}")
            # actualizar imagen si falta
            if not existing.imagen and g.get('imagen'):
                existing.imagen = g['imagen']
                db.session.commit()
                print(f"Imagen añadida a: {g['titulo']}")
            continue
        v = Videojuego(
            titulo=g['titulo'],
            desarrollador=g['desarrollador'],
            año_lanzamiento=g['año_lanzamiento'],
            genero=g['genero'],
            precio=g['precio'],
            imagen=g['imagen']
        )
        db.session.add(v)
    db.session.commit()
    print('Seed completo')
