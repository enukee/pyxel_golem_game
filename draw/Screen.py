from typing import Union
from abc import ABC

from draw import Drawer
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

        self.handler = None

    def draw(self, drawer: Drawer):
        """
        Отрисовка кнопки.
        :param drawer: Инструмент отрисовки.
        """
        drawer.drawButton(self.posX, self.posY, self.width, self.height, self.title)


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

        # Имя поля
        self.__title = title

    def draw(self, drawer: Drawer):
        """
        Отрисовка текстового поля.
        :param drawer: Инструмент отрисовки.
        """
        drawer.drawTextBox(self.posX, self.posY, self.width, self.height, self.text)

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, text):
        self.__text = text


class Screen:
    def __init__(self):
        """
        Базовый класс любого окна в игре(например меню и инвентарь).
        """
        self.__buttons = []  # Набор кнопок окна.
        self.__textBoxs = []  # Набор текстовых полей окна.

    def addBtn(self, btn: Button):
        """
        Добавление кнопки.
        :param btn: Кнопка с уникальным(для этого окна именем).
        """
        if self._findBtn(btn.title) == -1:  # Надпись кнопки является уникальным ключом.
            self.__buttons.append(btn)

    def addTxBox(self, txBox: TextBox):
        """
        Добавление текстового поля.
        :param txBox: Текстовое поле с уникальным именем.
        """
        if self._findBtn(txBox.title) == -1:  # Название поля является уникальным ключом.
            self.__textBoxs.append(txBox)

    def setHandler(self, buttonTitle: str, handler):
        """
        Установка обработчика нажатия на кнопку.
        :param buttonTitle: Надпись на кнопке.
        :param handler: Обработчик события нажатия.
        """
        btn = self._findBtn(buttonTitle)
        if btn != -1:
            btn.handler = handler

    def _findBtn(self, buttonTitle: str) -> Union[int, Button]:
        """
        Поиск кнопки окна.
        :param buttonTitle: Надпись кнопки.
        :return: Кнопка с заданной надписью(возвращает -1 если такой кнопки нет).
        """
        for btn in self.__buttons:
            if btn.title == buttonTitle:
                return btn

        return -1

    def update(self, control: Controller):
        """
        Обновление окна.
        :param control: Инструмент для отслеживания событий всего окна.
        """
        for btn in self.__buttons:
            if control.isMouseClicked(btn.posX, btn.posY, btn.width, btn.height) and btn.handler:
                btn.handler()

    def draw(self, drawer: Drawer):
        """
        Отображение окна.
        :param drawer: Инструмент отображения объектов.
        """
        drawer.drawBackground()
        for btn in self.__buttons:
            btn.draw(drawer)

        for tx in self.__textBoxs:
            tx.draw(drawer)
