import math
from abc import ABC, abstractmethod

import const
from draw import Scene
from units import Bullet


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
