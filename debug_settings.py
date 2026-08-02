# ________________________________________________________________
# Настройки отладки
from draw import Drawer

# Отрисовка объектов фона,
# не влияет на процесс игры
DEBUG_SET_RENDER_BACKGROUND_OBJ = False

# Выкл./Вкл. нанесение урона по врагам и игроку.
# Установите False для выключения урона
DEBUG_SET_TURNING_ON_DAMAGE = True

# Отрисовка всех тайлов карты
# Если значение False, то отображаются лишь ближайшие к игроку тайлы
DEBUG_SET_RENDER_ALL_MAP = False

# Режим сохранения карты,
# Если True, то при включении сохраняет карту как png и закрывает игру,
# Необходимо включить так же DEBUG_SET_RENDER_ALL_MAP
DEBUG_MAKE_IMG_MAP = False
# Отображение сетки тайлов при создании изображения карты
DEBUG_MAKE_IMG_MAP_GRID = False


def mapSaveImg(drawer: Drawer):
    """
    Сохранение карты как изображения
    """
    if DEBUG_MAKE_IMG_MAP_GRID:
        drawer.drawGrid()
    drawer.saveImg("../screenshot_map.png")
