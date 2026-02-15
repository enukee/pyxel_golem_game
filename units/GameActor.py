from abc import ABC, abstractmethod

import const
from map.MatrixMap import MatrixMap
from draw import Scene
from units import MovableObjects, SpriteManager


class Stats:
    def __init__(self, health: int, armor: int, attackSpeed: float, speed: float, acceleration: float):
        """
        Базовые параметры юнита.
        :param health: Базовое здоровье.
        :param armor: Очки брони.
        :param attackSpeed: Скорость атаки.
        :param speed: Начальная скорость.
        :param acceleration: Ускорение.
        """
        # Параметры объекта
        self.__health = health
        self.__armor = armor
        self.__attackSpeed = attackSpeed
        self.__speed = speed
        self.__acceleration = acceleration

    @abstractmethod
    def die(self):
        pass

    @property
    def health(self):
        return self.__health

    @health.setter
    def health(self, value):
        self.__health = value

    @property
    def armor(self):
        return self.__armor

    @property
    def attackSpeed(self):
        return self.__attackSpeed

    @property
    def baseSpeed(self):
        return self.__speed

    @property
    def acceleration(self):
        return self.__acceleration


class GameActor(MovableObjects, ABC):
    def __init__(self, x: float, y: float, baseSpriteName: str, stats: Stats):
        """
        Объект имеющий характеристики и способный передвигаться в пространстве.
        :param x: Координата x объекта.
        :param y: Координата y объекта.
        :param stats: Характеристики юнита.
        """
        super().__init__(x, y)

        # Характеристики объекта
        self._stats = stats

        self._dirX = 0
        self._dirY = 0

        # Менеджер спрайтов
        self.spriteManager = SpriteManager(baseSpriteName)

        # Параметры юнита
        self._currentHealth = self._stats.health
        self._currentSpeed = self._stats.baseSpeed
        self._maxSpeed = self._stats.baseSpeed + self._stats.acceleration * 20

    @abstractmethod
    def draw(self, scene: Scene):
        """
        Отображение спрайта.
        :param scene:  Сцена для отображения спрайтов.
        """
        pass

    def setDir(self, dirX, dirY):
        if dirX != 0:
            self._dirX = dirX / abs(dirX)
        else:
            self._dirX = dirX

        if dirY != 0:
            self._dirY = dirY / abs(dirY)
        else:
            self._dirY = dirY

    @property
    def dirX(self):
        return self._dirX

    @property
    def dirY(self):
        return self._dirY

    @abstractmethod
    def update(self, tileMap: MatrixMap, delta_time: float = 1):
        """
        Обновление(перемещение) юнита.
        :param tileMap: Карта тайлов.
        :param delta_time:  Время между кадрами.
        """
        # Увеличение скорости с учётом ускорения
        self._currentSpeed = min(max(self._currentSpeed + self._stats.acceleration * delta_time, 0), self._maxSpeed)

        # Вычисление смещения за текущий кадр
        step_x = self._dirX * self._currentSpeed * delta_time
        step_y = self._dirY * self._currentSpeed * delta_time

        # Проверка, что объект не превысил правую границу(с учётом ширины спрайта)
        spriteWidth = const.getWidthSprite(self.spriteManager.baseSpriteName) + 2
        if not tileMap.isWalkable(self.x + spriteWidth, self.y):
            step_x = min(step_x, 0)

        # Обновление позиции
        super().tryMove(step_x, step_y, tileMap)

    def speedReset(self):
        """
        Сброс скорости объекта до начальной.
        """
        self._currentSpeed = self._stats.baseSpeed
