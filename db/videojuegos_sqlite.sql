CREATE TABLE IF NOT EXISTS videojuegos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    genero TEXT NOT NULL,
    plataforma TEXT NOT NULL,
    rating REAL NOT NULL
);

INSERT INTO videojuegos (titulo, genero, plataforma, rating) VALUES
('The Legend of Zelda: Breath of the Wild', 'Aventura', 'Nintendo Switch', 9.8),
('God of War Ragnarok', 'Acción', 'PlayStation 5', 9.7),
('Minecraft', 'Sandbox', 'Multiplataforma', 9.0),
('Elden Ring', 'RPG', 'PC', 9.6),
('Halo Infinite', 'Shooter', 'Xbox Series X', 8.5),
('Super Mario Odyssey', 'Plataformas', 'Nintendo Switch', 9.2),
('Cyberpunk 2077', 'RPG', 'PC', 7.5),
('FIFA 23', 'Deportes', 'Multiplataforma', 8.0),
('Call of Duty: Modern Warfare II', 'Shooter', 'Multiplataforma', 8.7),
('Animal Crossing: New Horizons', 'Simulación', 'Nintendo Switch', 9.1);
