from abc import ABC, abstractmethod

from draw import Scene


class GameObject(ABC):
    def __init__(self, x: float, y: float, icon: str):
        self.__x, self.__y = x, y
        self.icon = icon

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def draw(self, scene: Scene):
        scene.drawIcon(self.icon, int(self.__x), int(self.__y))

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, x: float):
        self.__x = x

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, y: float):
        self.__y = y
