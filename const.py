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
SPRITE_POS = {"stub_sprite":        [85, 2, 6, 6, 0],
              "player":             [15, 1, 13, 21, 0],
              "player_pos0_down":   [15, 1, 13, 21, 0],
              "player_pos0_up":     [1, 1, 13, 21, 0],
              "player_pos0_left":   [29, 1, 13, 21, 0],
              "player_pos0_right":  [29, 1, -13, 21, 0],
              "player_pos1_down":   [15, 23, 13, 21, 0],
              "player_pos1_up":     [1, 23, 13, 21, 0],
              "player_pos1_left":   [29, 23, 13, 21, 0],
              "player_pos1_right":  [29, 23, -13, 21, 0],
              "player_pos2_down":   [15, 45, 13, 21, 0],
              "player_pos2_up":     [1, 45, 13, 21, 0],
              "player_pos2_left":   [29, 45, 13, 21, 0],
              "player_pos2_right":  [29, 45, -13, 21, 0],
              "player_pos3_down":   [15, 67, 13, 21, 0],
              "player_pos3_up":     [1, 67, 13, 21, 0],
              "player_pos3_left":   [29, 67, 13, 21, 0],
              "player_pos3_right":  [29, 67, -13, 21, 0],
              "player_pos4_down":   [15, 89, 13, 21, 0],
              "player_pos4_up":     [1, 89, 13, 21, 0],
              "player_pos4_left":   [29, 89, 13, 21, 0],
              "player_pos4_right":  [29, 89, -13, 21, 0],
              "player_shoot":       [71, 23, 13, 21, 0],

              "egghead":              [1, 111, 11, 15, 0],
              "egghead_pos0_down":    [1, 111, 11, 15, 0],
              "egghead_pos0_up":      [1, 127, 11, 15, 0],
              "egghead_pos0_left":    [1, 111, 11, 15, 0],
              "egghead_pos0_right":   [1, 111, -11, 15, 0],
              "egghead_pos1_down":    [13, 111, 11, 15, 0],
              "egghead_pos1_up":      [13, 127, 11, 15, 0],
              "egghead_pos1_left":    [13, 111, 11, 15, 0],
              "egghead_pos1_right":   [13, 111, -11, 15, 0],
              "egghead_pos2_down":    [25, 111, 11, 15, 0],
              "egghead_pos2_up":      [25, 127, 11, 15, 0],
              "egghead_pos2_left":    [25, 111, 11, 15, 0],
              "egghead_pos2_right":   [25, 111, -11, 15, 0],

              "mimic":                  [34, 236, 17, 20, 0],
              "mimic_bite":             [16, 238, 17, 18, 0],

              "wall":               [0, 240, 16, 16, 0]
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
