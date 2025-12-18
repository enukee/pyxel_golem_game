from Drawer import Drawer
import const

import pyxel


class PyxelDrawer(Drawer):
    def __init__(self, width: int, height: int, title: str):
        # Инициализация окна
        pyxel.init(width, height, title=title)
        # Загрузка изображений
        pyxel.images[0].load(0, 0, "assets/img_0.png")
        # Загрузка ресурсов(музыки и палитры)
        pyxel.load("assets/res.pyxres")

    def drawSprite(self, spritePos: list, x: int, y: int):
        """
        Отображение спрйта.
        :param spritePos: Позиция спрайта на img0.
        :param x: Координата для отрисовки x.
        :param y: Координата для отрисовки y.
        """
        pyxel.blt(x, y, 0, spritePos[0], spritePos[1], spritePos[2], spritePos[3], 0, rotate=spritePos[4])

    def drawIcon(self, iconPos: list, x: int, y: int):
        """
        Отображение иконки перка.
        :param iconPos: Позиция перка на img1.
        :param x: Координата для отрисовки x.
        :param y: Координата для отрисовки y.
        """
        pass

    def drawTileBorders(self, x: int, y: int):
        """
        Отображение границ спрайта.
        :param x: Координата для отрисовки x.
        :param y: Координата для отрисовки y.
        """
        pyxel.rect(x - 1, y - 1, const.TILE_SIZE + 2, const.TILE_SIZE + 2, 7)

    def drawTile(self, sectors: list, x: int, y: int):
        """
        Отображение тайла.
        :param sectors: Сектора спрайта
        :param x: Координата для отрисовки x.
        :param y: Координата для отрисовки y.
        """
        k = 0
        for i in [0, 128]:
            for j in [0, 128]:
                if sectors[k] == 0:
                    pyxel.rect(x + j, y + i, const.TILE_SECTOR_SIZE, const.TILE_SECTOR_SIZE, 0)

                elif sectors[k] == 1:
                    pyxel.rect(x + j, y + i + 100, const.TILE_SECTOR_SIZE, 28, 9)

                k += 1
