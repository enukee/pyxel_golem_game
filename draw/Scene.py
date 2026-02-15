import const
from draw import PyxelDrawer


class Scene:
    def __init__(self, width: int, height: int, title: str):
        """
        Сцена для отображения объектов.
        :param width: Ширина окна.
        :param height: Высота окна.
        :param title: Название окна.
        """
        self.drawer = PyxelDrawer(width, height, title)

    def changingView(self, x: int, y: int):
        """
        Изменение точки обзора.
        :param x: Координата x левого верхнего угла сцены.
        :param y: Координата y левого верхнего угла сцены.
        """
        self.drawer.setCamera(x, y)

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

