from abc import ABC, abstractmethod

from units import MovableObjects


class InteractiveObjectCreator(ABC):
    def __init__(self, handler):
        """
        Каждый объект реагирует на взаимодействие в соответствии со своим типом.
        Для фабрики типа задаётся обработчик, который выполняется при каждом
        взаимодействии с объектом данного типа.
        """
        self.__handler = handler

    @abstractmethod
    def randomObj(self, x: int, y: int):
        pass


class BoxCreator(InteractiveObjectCreator):
    def __init__(self, handler):
        super().__init__(handler)

    def randomObj(self, x: int, y: int):
        return BoxObject(x, y, self)


class InteractiveObject(MovableObjects):
    def __init__(self, x: float, y: float, spriteName: str, creator: InteractiveObjectCreator):
        """
        Объект с которым возможно взаимодействовать.
        :param x: Координата x объекта.
        :param y: Координата y объекта.
        """
        super().__init__(x, y)
        super().setSprite(spriteName)

        # Ссылка на фабрику, необходима для получения обработчика типа
        self.creator = creator

    def update(self):
        pass


class BoxObject(InteractiveObject):
    def __init__(self, x: float, y: float, creator: BoxCreator):
        """
        Сундук с предметами.
        :param x: Координата x объекта.
        :param y: Координата y объекта.
        """
        super().__init__(x, y, "box", creator)


