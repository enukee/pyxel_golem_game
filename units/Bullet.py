import math
from abc import ABC, abstractmethod

import const
from draw import Scene
from map import MatrixMap
from units import MovableObjects


class Bullet(MovableObjects, ABC):
    def __init__(self, startX: float, startY: float, directionX: float, directionY: float,
                 baseSpeed: float, acceleration: float, maxDistance: float, idlenessTime: float,
                 damage: int, criticalDamageChance: float, criticalDamage: float, sprite: str):
        """
        Абстрактный класс пули.
        :param startX: Начальная координата X.
        :param startY: Начальная координата Y.
        :param directionX: Направление по оси X (вектор).
        :param directionY: Направление по оси Y (вектор).
        :param baseSpeed: Базовая скорость пули.
        :param acceleration: Ускорение пули (может быть отрицательным для замедления).
        :param maxDistance: Максимальная дистанция, которую может пролететь пуля.
        :param idlenessTime: Время "простоя" пули, если её скорость стала нулевой.
        :param damage: Базовый урон пули.
        :param criticalDamageChance: Шанс критического урона (в процентах).
        :param criticalDamage: Урон при критическом попадании.
        :param sprite: Имя спрайта пули.
        """
        super().__init__(startX, startY)

        self.spriteType = sprite

        self.baseSpeed = baseSpeed
        self.acceleration = acceleration
        self.maxDistance = baseSpeed * maxDistance * const.DELTA_TIME + self.acceleration * (maxDistance * const.DELTA_TIME**2) / 2
        self.idlenessTime = idlenessTime
        self.damage = damage
        self.criticalDamageChance = criticalDamageChance
        self.criticalDamage = criticalDamage
        self.effects = []

        # Начальные координаты пули
        self.startPosX, self.startPosY = startX, startY
        self.isActive = True    # Флаг активности пули
        self.distance_traveled = 0.0    # Пройденная дистанция
        self.currentSpeed = self.baseSpeed  # Текущая скорость пули
        self.idlenessCounter = 0    # Счётчик времени простоя

        # Нормализация вектора направления
        direction_length = (directionX ** 2 + directionY ** 2) ** 0.5
        if direction_length > 0:
            self.direction_x = directionX / direction_length
            self.direction_y = directionY / direction_length
        else:
            raise ValueError("The zero vector {direction_x, direction_y} is not allowed.")

    def update(self, tile_map: MatrixMap, delta_time: float = const.DELTA_TIME):
        """
        Обновление состояния пули.
        :param tile_map: Матрица тайлов.
        :param delta_time: Время между кадрами.
        """
        if not self.isActive:
            return

        # Увеличение скорости с учётом ускорения
        self.currentSpeed = max(self.currentSpeed + self.acceleration, 0)

        # Если скорость нулевая заряд ещё существует некоторое время idlenessTime
        if self.currentSpeed == 0:
            self.idlenessCounter += 1
            if self.idlenessCounter > self.idlenessTime:
                self.isActive = False

        # Вычисление смещения за текущий кадр
        step_x = self.direction_x * self.currentSpeed * delta_time
        step_y = self.direction_y * self.currentSpeed * delta_time

        # Обновление позиции
        if not super().tryMove(step_x, step_y, tile_map):
            self.isActive = False
            return

        # Подсчёт пройденной дистанции
        step_distance = (step_x ** 2 + step_y ** 2) ** 0.5
        self.distance_traveled += step_distance

        # Проверка на превышение максимальной дистанции
        if self.distance_traveled >= self.maxDistance:
            self.isActive = False

    def isAlive(self) -> bool:
        """Проверка, активна ли пуля."""
        return self.isActive


class FireBullet(Bullet):
    def __init__(self, startX, startY, directionX, directionY, baseSpeedOwner):
        super().__init__(startX, startY, directionX, directionY,
                         baseSpeedOwner + 80, -0.5, 60, 40,
                         9, 5, 10,
                         "fire_bullet")

    def draw(self, scene: Scene, delta_time: float = const.DELTA_TIME):
        if not self.isActive:
            return

        # Анимация вращения спрайта в зависимости от пройденной дистанции
        step = self.distance_traveled % 16
        if step <= 4:
            sprite = self.spriteType

        elif step <= 8:
            sprite = self.spriteType + "_rotate90"

        elif step <= 12:
            sprite = self.spriteType + "_rotate180"

        else:
            sprite = self.spriteType + "_rotate270"

        super().setSprite(sprite)
        super().draw(scene)


class EnemyBullet(Bullet):
    def __init__(self, startX, startY, directionX, directionY, baseSpeedOwner):
        super().__init__(startX, startY, directionX, directionY,
                         baseSpeedOwner + 100, 9, 70, 0,
                         5, 5, 10,
                         "enemy_bullet")

    def draw(self, scene: Scene, delta_time: float = const.DELTA_TIME):
        if not self.isActive:
            return

        # Выбор спрайта в зависимости от направления движения
        if abs(self.direction_x) > abs(self.direction_y):
            if self.direction_x > 0:
                sprite = self.spriteType + "_right"
            else:
                sprite = self.spriteType + "_left"

        else:
            if self.direction_y > 0:
                sprite = self.spriteType + "_up"
            else:
                sprite = self.spriteType + "_down"

        super().setSprite(sprite)
        super().draw(scene)
