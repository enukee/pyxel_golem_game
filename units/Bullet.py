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
        self.maxDistance = maxDistance
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
        self.currentSpeed = max(self.currentSpeed + self.acceleration / 2 * delta_time, 0)

        # Если скорость нулевая заряд ещё существует некоторое время idlenessTime
        if self.currentSpeed == 0:
            self.idlenessCounter += 1
            if self.idlenessCounter > self.idlenessTime:
                self.isActive = False

        # Вычисление смещения за текущий кадр
        step_x = self.direction_x * self.currentSpeed * delta_time
        step_y = self.direction_y * self.currentSpeed * delta_time

        # Обновление позиции
        super().tryMove(step_x, step_y, tile_map)

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
    def __init__(self, startX, startY, directionX, directionY):
        super().__init__(startX, startY, directionX, directionY,
                         5, -0.5, 60, 40,
                         9, 5, 10,
                         "fire_bullet")

    def draw(self, scene: Scene):
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

        scene.drawSprite(sprite, int(self.x), int(self.y))


class EnemyBullet(Bullet):
    def __init__(self, startX, startY, directionX, directionY):
        super().__init__(startX, startY, directionX, directionY,
                         2, 0.5, 70, 0,
                         5, 5, 10,
                         "enemy_bullet")

    def draw(self, scene: Scene):
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

        scene.drawSprite(sprite, int(self.x), int(self.y))


class MultiShellBullet(Bullet, ABC):
    def __init__(self, startX: float, startY: float, directionX: float, directionY: float,
                 baseSpeed: float, acceleration: float, maxDistance: float, idlenessTime: float,
                 damage: int, criticalDamageChance: float, criticalDamage: float, sprite: str, offsets: list):
        """Инициализация пули с несколькими зарядами."""
        super().__init__(startX, startY, directionX, directionY, baseSpeed, acceleration, maxDistance,
                         idlenessTime, damage, criticalDamageChance, criticalDamage, sprite)
        self.offsets = offsets  # Список смещений для дополнительных оболочек
        self.offsets.append({"offsetWidth": 0, "offsetHeight": 0})  # Добавление нулевого смещения

    @abstractmethod
    def drawBullet(self, scene: Scene, spriteName: str, x: int, y: int):
        """Абстрактный метод для отрисовки одного заряда пули."""
        pass

    def draw(self, scene: Scene):
        """
        Отрисовка всех зарядов пули.
        :param scene: Сцена для отображения спрайтов.
        """
        if not self.isActive:
            return

        # Вычисление границ, в которых могут находиться оболочки
        def getSizeBorder(vecX: float, vecY: float, dist: float):
            if vecX == 0:
                return 0, dist
            if vecY == 0:
                return dist, 0
            arg = math.atan(vecX / vecY)
            return math.sin(arg) * dist, math.cos(arg) * dist

        rightBorder, leftBorder, upperBorder, lowerBorder = 0, 0, 0, 0
        distX, distY = getSizeBorder(self.direction_x, self.direction_y, self.maxDistance)

        bulletSize = abs(const.SPRITE_POS[self.spriteType + "_right"][2])

        # Определение границ в зависимости от направления
        if self.direction_x > 0:
            sprite = self.spriteType + "_right"
            rightBorder = distX - 2 * bulletSize

        elif self.direction_x < 0:
            sprite = self.spriteType + "_left"
            leftBorder = - distX + 2 * bulletSize

        else:
            rightBorder = self.maxDistance
            leftBorder = - self.maxDistance

        if self.direction_y > 0:
            sprite = self.spriteType + "_up"
            lowerBorder = distY - 2 * bulletSize

        elif self.direction_y < 0:
            sprite = self.spriteType + "_down"
            upperBorder = - distY + 2 * bulletSize

        else:
            lowerBorder = self.maxDistance
            upperBorder = - self.maxDistance

        # Определение, какие смещения использовать (по ширине или высоте)
        if abs(self.direction_y) < abs(self.direction_x):
            offsetX, offsetY = "offsetWidth", "offsetHeight"

        else:
            offsetX, offsetY = "offsetHeight", "offsetWidth"

        # Отрисовка всех зарядов пули
        for i in self.offsets:
            x = int(self.x - i[offsetX])
            y = int(self.y - i[offsetY])
            if ((leftBorder < x - self.startPosX < rightBorder) and
                    (upperBorder < y - self.startPosY < lowerBorder)):
                self.drawBullet(scene, sprite, x, y)


class BaseBullet(MultiShellBullet):
    def __init__(self, startX, startY, directionX, directionY):
        offsets = [{"offsetWidth": -8, "offsetHeight": -4}, {"offsetWidth": -14, "offsetHeight": 0}]
        super().__init__(startX, startY, directionX, directionY,
                         80, 1, 100, 0,
                         3, 5, 10,
                         "base_bullet", offsets)

    def drawBullet(self, scene: Scene, spriteName: str, x: int, y: int):
        scene.drawSprite(spriteName, x, y)

    def draw(self, scene: Scene):
        super().draw(scene)


class LightningBullet(MultiShellBullet):
    def __init__(self, startX, startY, directionX, directionY):
        lightningSize = abs(const.SPRITE_POS["lightning_bullet_right"][2])
        offset = [{"offsetWidth": lightningSize, "offsetHeight": 0}, {"offsetWidth": 2 * lightningSize, "offsetHeight": 0}]

        super().__init__(startX, startY, directionX, directionY,
                         8, 0, 90, 0,
                         6, 5, 10,
                         "lightning_bullet", offset)

    def drawBullet(self, scene: Scene, spriteName: str, x: int, y: int):
        if self.distance_traveled % 10 > 4:
            scene.drawSprite(spriteName, x, y)

        else:
            scene.drawSprite(spriteName, x, y, reverseY=True)

    def draw(self, scene: Scene):
        super().draw(scene)
