import const
from draw import Drawer


class Scene:
    def __init__(self, drawer: Drawer, cameraX: int, cameraY: int):
        """
        Сцена для отображения объектов
        :param drawer: Инструмент отрисовки объектов на сцене.
        """
        self.drawer = drawer
        self.cameraPosX = cameraX
        self.cameraPosY = cameraY

    def changingView(self, playerX: int, playerY: int, lerpFactor: float = 0.1):
        """
        Изменение точки обзора.
        :param playerX: Координата x игрока.
        :param playerY: Координата y игрока.
        :param lerpFactor: Скорость сглаживания перемещения камеры.
        """
        def lerp(a: float, b: float, t: float) -> float:
            # Линейная интерполяция между a и b с коэффициентом t (0.0 <= t <= 1.0)
            return a + (b - a) * t

        self.cameraPosX = lerp(self.cameraPosX, playerX - const.WINDOW_WIDTH // 2, lerpFactor)
        self.cameraPosY = lerp(self.cameraPosY, playerY - const.WINDOW_HEIGHT // 2, lerpFactor)
        self.drawer.setCamera(int(self.cameraPosX), int(self.cameraPosY))

    def changeView(self, cameraX: int, cameraY: int):
        self.cameraPosX, self.cameraPosY = cameraX, cameraY
        self.drawer.setCamera(int(self.cameraPosX), int(self.cameraPosY))

    def drawSprite(self, sprite: str, x: int, y: int, reverseX: bool = False, reverseY: bool = False):
        """
        Отображение спрайта на сцене.
        :param sprite: Тип спрайта.
        :param x: Положение левого верхнего угла спрайта по x.
        :param y: Положение левого верхнего угла спрайта по y.
        :param reverseX: Флаг отображения спрайта по x.
        :param reverseY: Флаг отображения спрайта по y.
        """
        if sprite in const.SPRITE_POS:
            spritePos = const.SPRITE_POS[sprite]

        else:
            spritePos = const.SPRITE_POS["stub_sprite"]

        spritePos[2] *= -1 if reverseX else 1
        spritePos[3] *= -1 if reverseY else 1
        self.drawer.drawSprite(spritePos, x, y)

    def drawTile(self, tile: str, x: int, y: int):
        """
        Отображение тайла на сцене.
        :param tile: Тип тайла.
        :param x: Положение левого верхнего угла тайла по x.
        :param y: Положение левого верхнего угла тайла по y.
        """
        if tile in const.TILE_STRUCTURE:
            # self.drawer.drawTileBorders(x, y, const.TILE_SIZE, const.TILE_SIZE)

            tileSectors = const.TILE_STRUCTURE[tile]
            self.drawer.drawTile(tileSectors, x, y)

    def drawIcon(self, icon: str, x: int, y: int):
        """
        Отображение иконки.
        :param icon: Тип иконки.
        :param x: Положение левого верхнего угла иконки по x.
        :param y: Положение левого верхнего угла иконки по y.
        """
        if icon in const.ICON_POS:
            spritePos = const.ICON_POS[icon]

        else:
            spritePos = const.ICON_POS["eye"]

        # Размер иконки 16x16 размер блока 18x18
        # иконка должна находится посередине
        self.drawer.drawIcon(spritePos, x + 1, y + 1)

    def drawHealth(self, value: int):
        self.drawer.drawHealth(value)
