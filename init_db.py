from app import app, db, User, Videojuego

def init_db():
    with app.app_context():
        # Eliminar todas las tablas existentes
        db.drop_all()
        # Crear todas las tablas desde cero
        db.create_all()

        # Crear usuario admin por defecto
        admin = User(email='admin@example.com', role='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        
        # Agregar videojuegos de ejemplo
        juegos = [
            {
                'titulo': 'The Legend of Zelda: Tears of the Kingdom',
                'desarrollador': 'Nintendo',
                'año_lanzamiento': 2023,
                'genero': 'Acción-Aventura',
                'plataforma': 'Nintendo Switch',
                'precio': 59.99,
                'imagen': 'https://assets.nintendo.com/image/upload/ar_16:9,c_lpad,w_656/b_white/f_auto/q_auto/ncom/software/switch/70010000063714/276a412988e07c4d55a2996c6d38abb408b464413b2dfeb44d2aa460b9f622e1'
            },
            {
                'titulo': 'Red Dead Redemption 2',
                'desarrollador': 'Rockstar Games',
                'año_lanzamiento': 2018,
                'genero': 'Acción-Aventura',
                'plataforma': 'PS4/Xbox One/PC',
                'precio': 49.99,
                'imagen': 'https://upload.wikimedia.org/wikipedia/en/4/44/Red_Dead_Redemption_II.jpg'
            },
            {
                'titulo': 'Cyberpunk 2077',
                'desarrollador': 'CD Projekt Red',
                'año_lanzamiento': 2020,
                'genero': 'RPG',
                'plataforma': 'PS4/Xbox One/PC',
                'precio': 49.99,
                'imagen': 'https://upload.wikimedia.org/wikipedia/en/9/9f/Cyberpunk_2077_box_art.jpg'
            }
        ]
        
        for juego_data in juegos:
            juego = Videojuego(**juego_data)
            db.session.add(juego)
        
        db.session.commit()
        print("✅ Base de datos inicializada con datos de ejemplo")

if __name__ == '__main__':
    init_db()