from abc import ABC

import const
from draw import Drawer, Scene
from events import Controller


class BaseWindowsWidget(ABC):
    def __init__(self, posX: int, posY: int, width: int, height: int, title: str):
        self.__posX = posX
        self.__posY = posY
        self.__width = width
        self.__height = height

        self.__title = title

    @property
    def posX(self):
        return self.__posX

    @property
    def posY(self):
        return self.__posY

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    @property
    def title(self):
        return self.__title


class Button(BaseWindowsWidget):
    def __init__(self, posX: int, posY: int, width: int, height: int, title: str = "button"):
        """
        Кнопка интерфейса.
        :param posX: Позиция кнопки по оис X.
        :param posY: Позиция кнопки по оис Y.
        :param width: Ширина кнопки.
        :param height: Высота кнопки.
        :param title: Надпись кнопки.
        """
        super().__init__(posX, posY, width, height, title)

        self.__handlerLeft = None
        self.__handlerRight = None

    def update(self, control: Controller):
        if (control.isMouseClickedLeft(self.posX, self.posY, self.width, self.height)
                and self.__handlerLeft):
            self.__handlerLeft(self)

        if (control.isMouseClickedRight(self.posX, self.posY, self.width, self.height)
                and self.__handlerRight):
            self.__handlerRight(self)

    def draw(self, scene: Scene):
        """
        Отрисовка кнопки.
        :param scene: Сцена отрисовки.
        """
        scene.drawer.drawButton(self.posX, self.posY, self.width, self.height, self.title)

    def setHandlerLeft(self, handler):
        self.__handlerLeft = handler

    def setHandlerRight(self, handler):
        self.__handlerRight = handler


class TextBox(BaseWindowsWidget):
    def __init__(self, posX: int, posY: int, width: int, height: int, text: str = "text", title: str = None):
        """
        Поле для отображения текста.
        :param posX: Позиция кнопки по оис X.
        :param posY: Позиция кнопки по оис Y.
        :param width: Ширина кнопки.
        :param height: Высота кнопки.
        :param text: Текст в поле.
        """
        super().__init__(posX, posY, width, height, title)

        self.__text = text

    def draw(self, scene: Scene):
        """
        Отрисовка текстового поля.
        :param scene: Сцена отрисовки.
        """
        scene.drawer.drawTextBox(self.posX, self.posY, self.width, self.height, self.text)

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, text):
        self.__text = text


class Block(Button):
    # Сохранение выбранного блока
    selectBlock = None

    def __init__(self, posX: int, posY: int, width: int, height: int, title: str = "button"):
        """
        Блок для хранения предмета или навыка в контейнере блоков интерфейса.
        :param posX: Позиция блока по оис X.
        :param posY: Позиция блока по оис Y.
        :param width: Ширина блока.
        :param height: Высота блока.
        :param title: Надпись блока.
        """
        super().__init__(posX, posY, width, height, title)

    def update(self, control: Controller):
        # При нажатии на блок он становится выбранным
        if control.isMouseClickedLeft(self.posX, self.posY, self.width, self.height):
            Block.selectBlock = self

        super().update(control)

    def draw(self, scene: Scene):
        """
        Отрисовка блока с иконкой.
        :param scene: Сцена отрисовки.
        """
        if Block.selectBlock == self:
            scene.drawer.drawSelectBlock(self.posX, self.posY, self.width, self.height)
        else:
            scene.drawer.drawBlock(self.posX, self.posY, self.width, self.height)


class BlockBox(BaseWindowsWidget):
    def __init__(self, posX: int, posY: int, sizeX: int, sizeY: int, title: str):
        """
        Виджет хранящий блоки(предметы, навыки)
        :param posX: Положение по X виджета.
        :param posY: Положение по Y виджета.
        :param sizeX: Количество слотов блоков по горизонтали.
        :param sizeY: Количество слотов блоков по вертикали.
        """
        super().__init__(
            posX,
            posY,
            sizeX * const.BLOCK_SIZE + (sizeX + 2) * const.BLOCK_SIZE_OFFSET,
            sizeY * const.BLOCK_SIZE + (sizeY + 2) * const.BLOCK_SIZE_OFFSET,
            title)

        self._table = dict()
        self._max_size_table = sizeX * sizeY

        self._sizeX = sizeX
        self._sizeY = sizeY

    def genAllBlockName(self):
        for i in range(self._sizeX):
            for j in range(self._sizeY):
                yield self.title + str(i) + str(j)

    def fill(self):
        for i in range(self._sizeX):
            for j in range(self._sizeY):
                self.pushBlock(i, j, self.title + str(i) + str(j))

    def getBlockNum(self, title: str):
        for i, blk in self._table.items():
            if blk.title == title:
                return i

        return -1

    def pushBlock(self, i: int, j: int, blockName: str):
        if (len(self._table) < self._max_size_table and
                i < self._sizeX and j < self._sizeY):
            x = self.posX + i * const.BLOCK_SIZE + (i + 1) * const.BLOCK_SIZE_OFFSET
            y = self.posY + j * const.BLOCK_SIZE + (j + 1) * const.BLOCK_SIZE_OFFSET
            self._table[self.getNum(j, i)] = Block(x, y, const.BLOCK_SIZE, const.BLOCK_SIZE, blockName)

    def update(self, control: Controller):
        for _, bl in self._table.items():
            bl.update(control)

    def draw(self, scene: Scene):
        """
        Отрисовка контейнера блоков.
        :param scene: Сцена отрисовки.
        """
        scene.drawer.drawBox(self.posX, self.posY, self.width, self.height)
        for _, bl in self._table.items():
            bl.draw(scene)

    @property
    def maxCount(self):
        return self._max_size_table

    def getNum(self, i, j):
        return self._sizeX * i + j

    def getPos(self, n: int):
        """
        Вычисление позиции блока на экране по позиции в таблице.
        :param n: Номер блока по порядку.
        :return: Координаты x и y.
        """
        x, y, = -1, -1

        i, j = n % self._sizeX, int(n / self._sizeX)
        if i < self._sizeX and j < self._sizeY:
            x = self.posX + i * const.BLOCK_SIZE + (i + 1) * const.BLOCK_SIZE_OFFSET
            y = self.posY + j * const.BLOCK_SIZE + (j + 1) * const.BLOCK_SIZE_OFFSET

        return x, y

    def find(self, title: str):
        """
        Поиск блока контейнера.
        :param title: Надпись уникальная для этого окна.
        :return: Элемент с заданной надписью(возвращает -1 если такой кнопки нет).
        """
        for _, blk in self._table.items():
            if blk.title == title:
                return blk

        return -1

    def setHandlerLeft(self, handler):
        for _, blk in self._table.items():
            blk.setHandlerLeft(handler)

    def setHandlerRight(self, handler):
        for _, blk in self._table.items():
            blk.setHandlerRight(handler)


class Screen:
    def __init__(self, drawer: Drawer):
        """
        Базовый класс любого окна в игре(например меню и инвентарь).
        """
        # Свой объект сцены имеющий собственные координаты экрана
        self._scene = Scene(drawer, 0, 0)

        self.__buttons = []  # Набор кнопок окна.
        self.__textBoxs = []  # Набор текстовых полей окна.
        self.__blockBox = []  # Набор контейнеров с блоками.

    def addBtn(self, btn: Button):
        """
        Добавление кнопки с уникальным (для этого окна) именем.
        """
        if self._find(btn.title) == -1:
            self.__buttons.append(btn)

    def addTxBox(self, txBox: TextBox):
        """
        Добавление текстового поля с уникальным (для этого окна) именем.
        """
        if self._find(txBox.title) == -1:
            self.__textBoxs.append(txBox)

    def addBlBox(self, blBox: BlockBox):
        """
        Добавление текстового поля с уникальным (для этого окна) именем.
        """
        if self._find(blBox.title) == -1:
            self.__blockBox.append(blBox)

    def setHandlerLeft(self, objTitle: str, handler):
        """
        Установка обработчика нажатия на кнопку.
        :param objTitle: Надпись на кнопке.
        :param handler: Обработчик события нажатия.
        """
        obj = self._find(objTitle)
        if obj != -1:
            obj.setHandlerLeft(handler)

    def setHandlerRight(self, objTitle: str, handler):
        """
        Установка обработчика нажатия на кнопку.
        :param objTitle: Надпись на кнопке.
        :param handler: Обработчик события нажатия.
        """
        obj = self._find(objTitle)
        if obj != -1:
            obj.setHandlerRight(handler)

    def _find(self, title: str):
        """
        Поиск кнопки окна.
        :param title: Надпись уникальная для этого окна.
        :return: Элемент с заданной надписью(возвращает -1 если такой кнопки нет).
        """
        for btn in self.__buttons:
            if btn.title == title:
                return btn

        for txBx in self.__textBoxs:
            if txBx.title == title:
                return txBx

        for blBx in self.__blockBox:
            if blBx.title == title:
                return blBx

        return -1

    def update(self, control: Controller):
        """
        Обновление окна.
        :param control: Инструмент для отслеживания событий всего окна.
        """
        for btn in self.__buttons:
            btn.update(control)

        for bl in self.__blockBox:
            bl.update(control)

    def draw(self):
        """
        Отображение окна.
        """
        self._scene.drawer.drawBackground()
        self._scene.changeView(0, 0)

        for btn in self.__buttons:
            btn.draw(self._scene)

        for tx in self.__textBoxs:
            tx.draw(self._scene)

        for bl in self.__blockBox:
            bl.draw(self._scene)
