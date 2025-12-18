# размер тайла (TILE_SIZE x TILE_SIZE)
TILE_SIZE = 256
TILE_SECTOR_SIZE = TILE_SIZE / 2

# Размер окна
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000

# Параметры спрайта: положение по x, положение по y, ширина, высота, поворот
SPRITE_POS = {}

# Тайл делится на 4 равных сектора
# 0 - сектор пола
# 1 - сектор стены
# None - сектор пустой
TILE_STRUCTURE = {
    "horizontal_road": [1, 1, 0, 0],
    "vertical_road": [0, None, 0, None],
    "lower_left_corner": [0, 1, 0, 0],
    "upper_right_corner": [1, None, 0, None],
}
