from typing import Union

from draw import Drawer
from events import Controller


class Button:
    def __init__(self, posX: int, posY: int, width: int, height: int, title: str = "button"):
        """
        Кнопка интерфейса.
        :param posX: Позиция кнопки по оис X.
        :param posY: Позиция кнопки по оис Y.
        :param width: Ширина кнопки.
        :param height: Высота кнопки.
        :param title: Надпись кнопки.
        """
        self.__posX = posX
        self.__posY = posY
        self.__width = width
        self.__height = height

        self.__title = title

        self.handler = None

    def draw(self, drawer: Drawer):
        """
        Отрисовка кнопки.
        :param drawer: Инструмент отрисовки.
        """
        drawer.drawButton(self.__posX, self.__posY, self.__width, self.__height, self.__title)

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


class Screen:
    def __init__(self):
        """
        Базовый класс любого окна в игре(например меню и инвентарь).
        """
        self.__buttons = []     # Набор кнопок окна.

    def addBtn(self, btn: Button):
        """
        Добавление кнопки.
        :param btn: Кнопка с уникальным(для этого окна именем).
        """
        if self._findBtn(btn.title) == -1:      # Надпись кнопки является уникальным ключом.
            self.__buttons.append(btn)

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
