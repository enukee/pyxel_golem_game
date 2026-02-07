from abc import ABC, abstractmethod

import const
from map.MatrixMap import MatrixMap
from draw import Scene
from units import MovableObjects, SpriteManager


class GameActor(MovableObjects, ABC):
    class Stats:
        def __init__(self, health: int, armor: int, attackSpeed: float, baseSpeed: float, acceleration: float):
            """
            Параметры существа.
            :param health: Здоровье в процентах.
            :param armor: Броня в процентах.
            :param attackSpeed: Скорость атаки.
            :param baseSpeed: Начальная скорость.
            :param acceleration: Ускорение.
            """
            # Параметры объекта
            self.__health = health
            self.__armor = armor
            self.__attackSpeed = attackSpeed
            self.__baseSpeed = baseSpeed
            self.__acceleration = acceleration

        @abstractmethod
        def die(self):
            pass

        @property
        def health(self):
            return self.__health

        @health.setter
        def health(self, value):
            if value < 0:
                self.die()

            if value > 100:
                value = 100

            self.__health = value

        @property
        def armor(self):
            return self.__armor

        @property
        def attackSpeed(self):
            return self.__attackSpeed

        @property
        def baseSpeed(self):
            return self.__baseSpeed

        @property
        def acceleration(self):
            return self.__acceleration

    def __init__(self, x: float, y: float, baseSpriteName: str,
                 health: int, armor: int, attackSpeed: float, baseSpeed: float, acceleration: float):
        """
        Объект имеющий характеристики и способный передвигаться в пространстве.
        :param x: Координата x объекта.
        :param y: Координата y объекта.
        :param health: Значение здоровья в процентах.
        :param armor: Значение брони в процентах.
        :param attackSpeed: Скорость атаки.
        :param baseSpeed: Начальная скорость.
        :param acceleration: Ускорение.
        """
        super().__init__(x, y)

        # Характеристики объекта
        self._stats = self.Stats(health, armor, attackSpeed, baseSpeed, acceleration)

        self._dirX = 0
        self._dirY = 0

        # Менеджер спрайтов
        self.spriteManager = SpriteManager(baseSpriteName)

        # Параметры объекта
        self._currentSpeed = self._stats.baseSpeed
        self._maxSpeed = baseSpeed + acceleration * 20

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
        Перемещение объекта по вектору (dirX, dirY).
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
