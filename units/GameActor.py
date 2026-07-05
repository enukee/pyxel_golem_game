from abc import ABC, abstractmethod

import const
from events import Events
from map.MatrixMap import MatrixMap
from draw import Scene
from units import MovableObjects, SpriteManager, Stats


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

        # Флаг, что юнит не убит
        self.isAlive = True

        # Менеджер спрайтов
        self.spriteManager = SpriteManager(baseSpriteName)

        # Параметры юнита
        self._currentHealth = self._stats.health
        self._currentSpeed = self._stats.speed
        self._maxSpeed = self._stats.speed + self._stats.acceleration * 6

        # Время последний атаки
        self.lastAttackTime = 0

    def draw(self, scene: Scene, delta_time: float = const.DELTA_TIME):
        """
        Отображение спрайта.
        :param scene:  Сцена для отображения спрайтов.
        :param delta_time: Время между кадрами.
        """
        self.spriteManager.setDir(self.dirX, self.dirY)  # Установка направления игрока
        spriteName, shift = self.spriteManager.getSprite(self._currentSpeed * delta_time,
                                                         applyDir=True)  # Получение имя спрайта

        super().setSprite(spriteName)
        super().draw(scene, delta_time)

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
    def update(self, events: Events, tileMap: MatrixMap, delta_time: float = const.DELTA_TIME):
        """
        Обновление(перемещение) юнита.
        :param events:  Инструмент получения событий.
        :param tileMap: Карта тайлов.
        :param delta_time:  Время между кадрами.
        """
        # Увеличение скорости с учётом ускорения
        self._currentSpeed = min(max(self._currentSpeed + self._stats.acceleration * delta_time, 0), self._maxSpeed)

        # Вычисление смещения за текущий кадр
        step_x = self._dirX * self._currentSpeed * delta_time
        step_y = self._dirY * self._currentSpeed * delta_time

        # Обновление позиции
        super().tryMove(step_x, step_y, tileMap)

    def speedReset(self):
        """
        Сброс скорости объекта до начальной.
        """
        self._currentSpeed = self._stats.speed

    def getDamage(self, val):
        # Настройка отладки
        if not const.DEBUG_SET_TURNING_ON_DAMAGE:
            return

        if self._stats.takingDamage(val) is not None:
            self.isAlive = False
