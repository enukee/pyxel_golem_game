from draw import Drawer
import const

import pyxel


class PyxelDrawer(Drawer):
    def __init__(self, width: int, height: int, title: str):
        # Инициализация окна
        pyxel.init(width, height, title=title, fps=const.FPS)
        # Загрузка ресурсов(музыки и палитры)
        pyxel.load("../assets/res.pyxres")
        # Загрузка изображений
        pyxel.images[0].load(0, 0, "../assets/img_0.png")
        pyxel.images[1].load(0, 0, "../assets/img_1.png")

        self.x, self.y = 0, 0

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
        pyxel.blt(x, y, 1, iconPos[0], iconPos[1], iconPos[2], iconPos[3], 0)

    def drawTileBorders(self, x: int, y: int):
        """
        Отображение границ спрайта.
        :param x: Координата для отрисовки x.
        :param y: Координата для отрисовки y.
        """
        pyxel.rect(x - 1, y - 1, const.TILE_SIZE + 2, const.TILE_SIZE + 2, 7)

    def drawWall(self, x: int, y: int, w: int, h: int):
        wall = const.SPRITE_POS["wall"]
        size = wall[2]
        for i in range(0, h, size):
            for j in range(0, w, size):
                pyxel.blt(x + j, y + i, 0, wall[0], wall[1], wall[2], wall[3], 0, rotate=wall[4])

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
                    self.drawWall(x + j, y + i + 64, const.TILE_SECTOR_SIZE, 64)

                k += 1

    def drawBox(self, x: int, y: int, width: int, height: int):
        """
        Отображение поля на экране.
        """
        x -= 2
        y -= 2
        width += 2
        height += 2
        pyxel.rect(x, y, width, height, const.WIN_COLOR_BOX)
        pyxel.rectb(x + 1, y + 1, width - 2, height - 2, const.WIN_COLOR_BOX_EDGING)

    def drawBlock(self, x: int, y: int, width: int, height: int):
        """
        Отображение блока с иконкой.
        """
        pyxel.rect(x, y, width, height, const.WIN_COLOR_BLOCK)
        pyxel.rectb(x + 1, y + 1, width - 2, height - 2, const.WIN_COLOR_BLOCK_EDGING)

    def drawSelectBlock(self, x: int, y: int, width: int, height: int):
        """
        Отображение блока с иконкой.
        """
        self.drawBlock(x, y, width, height)
        pyxel.rectb(x + 1, y + 1, width - 2, height - 2, const.WIN_COLOR_BLOCK_EDGING_SELECT)

    def drawButton(self, x: int, y: int, width: int, height: int, title: str):
        """
        Отображение кнопки на экране.
        """
        self.drawBox(x, y, width, height)
        pyxel.text(x + 5, y + 7, title, const.WIN_COLOR_TEXT)

    def drawButtonPress(self, x: int, y: int, width: int, height: int, title: str):
        """
        Отображение нажатой кнопки на экране.
        """
        pyxel.rect(x, y, width, height, const.WIN_COLOR_BOX)
        pyxel.rectb(x + 1, y + 1, width - 2, height - 2, const.WIN_COLOR_BOX_EDGING_SELECT)
        pyxel.text(x + 5, y + 7, title, const.WIN_COLOR_TEXT)

    def drawTextBox(self, x: int, y: int, width: int, height: int, text: str):
        """
        Отображение текстового поля на экране.
        """
        self.drawBox(x, y, width, height)

        textList = text.split("/n")

        # Перебираем все подстроки в цикле
        strY = y + 7
        for s in textList:
            pyxel.text(x + 5, strY, s, const.WIN_COLOR_TEXT)
            strY += 7

    def drawBackground(self):
        """
        Отрисовка фона любого окна.
        """
        pyxel.cls(const.WIN_COLOR_BACKGROUND)

    def mouseVisible(self, visible: bool):
        pyxel.mouse(visible)

    def setCamera(self, x: int, y: int):
        """
        Установка камеры на координатах (x, y).
        :param x: Координата для отрисовки x.
        :param y: Координата для отрисовки y.
        """
        self.x, self.y = x, y
        pyxel.camera(x, y)

    def drawHealth(self, val: int):
        # Отрисовка полоски здоровья в левом верхнем углу
        pyxel.rect(self.x + 2, self.y + 2, 102, 5, 6)
        pyxel.rect(self.x + 3, self.y + 3, 100, 3, 0)
        pyxel.rect(self.x + 3, self.y + 3, val, 3, 8)
