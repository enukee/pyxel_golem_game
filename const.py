# размер тайла (TILE_SIZE x TILE_SIZE)
TILE_SIZE = 256
TILE_SECTOR_SIZE = TILE_SIZE // 2

# Размер окна
WINDOW_WIDTH = 320
WINDOW_HEIGHT = 240


def getWidthSprite(sprite: str):
    if sprite in SPRITE_POS:
        return SPRITE_POS[sprite][2]

    return None


def getHeightSprite(sprite: str):
    if sprite in SPRITE_POS:
        return SPRITE_POS[sprite][3]

    return None


# Параметры спрайта: положение по x, положение по y, ширина, высота, поворот
SPRITE_POS = {"stub_sprite": [85, 2, 6, 6, 0],
              "player_down": [15, 1, 13, 21, 0],
              "wall": [0, 240, 16, 16, 0]
              }

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
