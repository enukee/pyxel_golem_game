from abc import ABC, abstractmethod
from random import randint

from events import Events
from map import MatrixMap
from objects import ArtifactGenerator
from units import MovableObjects


class InteractiveObjectCreator(ABC):
    def __init__(self, handler):
        """
        Каждый объект реагирует на взаимодействие в соответствии со своим типом.
        Для фабрики типа задаётся обработчик, который выполняется при каждом
        взаимодействии с объектом данного типа.
        """
        self.__handler = handler

    def getHandler(self):
        return self.__handler

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

    def interact(self):
        handler = self.creator.getHandler()
        handler(self)

    def update(self, events: Events, tileMap: MatrixMap):
        pass


class BoxObject(InteractiveObject):
    generator = ArtifactGenerator()

    def __init__(self, x: float, y: float, creator: BoxCreator):
        """
        Сундук с предметами.
        :param x: Координата x объекта.
        :param y: Координата y объекта.
        """
        super().__init__(x, y, "box", creator)

        size = randint(0, 16)
        self.__artifacts = dict(enumerate(BoxObject.generator.genArtifactsBox(size)))

    @property
    def artifacts(self):
        return self.__artifacts
