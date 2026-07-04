# размер тайла (TILE_SIZE x TILE_SIZE)
TILE_SIZE = 256
TILE_SECTOR_SIZE = TILE_SIZE // 2

# Размер окна
WINDOW_WIDTH = 320
WINDOW_HEIGHT = 240

# Частота кадров
FPS = 60
# Время между кадрами
DELTA_TIME = 1 / FPS

BUTTON_MENU_WIDTH = 40
BUTTON_MENU_HEIGHT = 20

BUTTON_MENU_POS_X = (WINDOW_WIDTH - BUTTON_MENU_WIDTH) / 2

CONST_WIDTH_ALL_UNIT = 4


def getWidthSprite(sprite: str):
    if sprite in SPRITE_POS:
        return abs(SPRITE_POS[sprite][2])

    return None


def getHeightSprite(sprite: str):
    if sprite in SPRITE_POS:
        return abs(SPRITE_POS[sprite][3])

    return None


def rectanglesIntersect(x1, y1, width1, height1, x2, y2, width2, height2):
    left1 = x1
    right1 = x1 + width1
    top1 = y1
    bottom1 = y1 + height1

    left2 = x2
    right2 = x2 + width2
    top2 = y2
    bottom2 = y2 + height2

    if right1 < left2 or right2 < left1:
        return False

    if bottom1 < top2 or bottom2 < top1:
        return False

    return True


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

              "base_bullet_right": [103, 6, 5, 1, 0],
              "base_bullet_left": [103, 6, -5, 1, 0],
              "base_bullet_up": [103, 6, 5, 1, 90],
              "base_bullet_down": [103, 6, 5, -1, 90],
              "fire_bullet": [97, 2, 5, 5, 0],
              "fire_bullet_rotate90": [97, 2, 5, 5, 90],
              "fire_bullet_rotate180": [97, 2, -5, -5, 0],
              "fire_bullet_rotate270": [97, 2, -5, -5, 90],
              "lightning_bullet_right": [103, 2, 7, 3, 0],
              "lightning_bullet_left": [103, 2, -7, 3, 0],
              "lightning_bullet_up": [103, 2, 7, 3, 90],
              "lightning_bullet_down": [103, 2, 7, -3, 90],
              "enemy_bullet_right": [92, 2, 4, 4, 0],
              "enemy_bullet_left": [92, 2, -4, 4, 0],
              "enemy_bullet_up": [92, 2, 4, 4, 90],
              "enemy_bullet_down": [92, 2, 4, -4, 90],


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
