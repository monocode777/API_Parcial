from app import app, db
from models.videojuego import Videojuego

def seed_games():
    with app.app_context():
        # Crear algunos videojuegos de ejemplo
        games = [
            {
                'titulo': 'The Legend of Zelda: Breath of the Wild',
                'desarrollador': 'Nintendo',
                'año_lanzamiento': 2017,
                'genero': 'Acción-Aventura',
                'plataforma': 'Nintendo Switch',
                'precio': 59.99,
                'imagen': 'https://assets.nintendo.com/image/upload/ar_16:9,b_auto:border,c_lpad/b_white/f_auto/q_auto/dpr_auto/c_scale,w_300/v1/ncom/en_US/games/switch/t/the-legend-of-zelda-breath-of-the-wild-switch/hero'
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
            },
            {
                'titulo': 'Elden Ring',
                'desarrollador': 'FromSoftware',
                'año_lanzamiento': 2022,
                'genero': 'RPG de Acción',
                'plataforma': 'PS5/Xbox Series X/PC',
                'precio': 59.99,
                'imagen': 'https://upload.wikimedia.org/wikipedia/en/b/b9/Elden_Ring_Box_art.jpg'
            },
            {
                'titulo': 'God of War Ragnarök',
                'desarrollador': 'Santa Monica Studio',
                'año_lanzamiento': 2022,
                'genero': 'Acción-Aventura',
                'plataforma': 'PS4/PS5',
                'precio': 69.99,
                'imagen': 'https://upload.wikimedia.org/wikipedia/en/e/ee/God_of_War_Ragnar%C3%B6k_cover.jpg'
            }
        ]

        for game_data in games:
            game = Videojuego(**game_data)
            db.session.add(game)
        
        db.session.commit()
        print("¡Juegos agregados exitosamente!")

if __name__ == '__main__':
    seed_games()