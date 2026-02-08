import math
from abc import ABC, abstractmethod
import random

import const
from units import GameActor, Player
from map import MatrixMap
from draw import Scene


class Enemy(GameActor, ABC):
    def __init__(self, x: float, y: float, player: Player, baseSpriteName: str, health: int, armor: int,
                 attackSpeed: float, baseSpeed: float,
                 acceleration: float, detectionRadius: float, attackRadius: float):
        """
        Базовый класс врага.
        :param x: Начальная координата X.
        :param y: Начальная координата Y.
        :param baseSpriteName: Базовое имя спрайта.
        :param health: Здоровье в процентах.
        :param armor: Броня в процентах.
        :param attackSpeed: Скорость атаки.
        :param baseSpeed: Начальная скорость.
        :param acceleration: Ускорение.
        :param detectionRadius: Радиус обнаружения.
        :param attackRadius: Радиус атаки.
        """
        super().__init__(x, y, baseSpriteName, health, armor, attackSpeed, baseSpeed, acceleration)
        self.bullet = None
        # Радиус обнаружения игрока
        self.detectionRadiusSquare = detectionRadius * detectionRadius
        # Радиус атаки
        self.attackRadiusSquare = attackRadius * attackRadius

        super().setDir(random.choice([-1, 0, 1]), random.choice([-1, 0, 1]))

        # Ссылка на игрока
        self.player = player

    @abstractmethod
    def attack(self):
        """
        Атака если игрок находится в радиусе атаки.
        """
        self.spriteManager.startAttack()

    def isPlayerNearby(self, radiusSquare: float):
        """
        Поиск игрока в радиусе radiusSquare.
        :param radiusSquare: Радиус поиска.
        :return: Возвращает True если игрок находится в заданном радиусе.
        """
        dx = self.player.x - self.x
        dy = self.player.y - self.y
        return dx * dx + dy * dy <= radiusSquare

    def update(self, tileMap: MatrixMap, delta_time: float = 1):
        if self.isPlayerNearby(self.detectionRadiusSquare):     # Поиск игрока в радиусе обнаружения
            # Игрок рядом: передвижение к игроку
            if self.isPlayerNearby(self.attackRadiusSquare):
                # Игрок в радиусе атаки
                self.attack()
                super().setDir(0, 0)
            else:
                self.movementToTarget(tileMap, delta_time)

        else:
            # Игрока нет рядом: свободное передвижение
            self.randomMovement(tileMap, delta_time)

    @abstractmethod
    def movementToTarget(self, tileMap: MatrixMap, delta_time: float = 1):
        super().setDir(int(self.player.x - self.x), int(self.player.y - self.y))
        super().update(tileMap, delta_time)
        print("move to target")

    @abstractmethod
    def randomMovement(self, tileMap: MatrixMap, delta_time: float = 1):
        # Движение в случайном направлении
        super().update(tileMap, delta_time)

        # Случайное изменение направления (опционально)
        if random.random() < 0.05:  # 5% шанс сменить направление
            super().setDir(random.choice([-1, 0, 1]), random.choice([-1, 0, 1]))

        print("random move")


class EggheadEnemy(Enemy):
    def __init__(self, x: float, y: float, player: Player):
        super().__init__(x, y, player, "egghead",
                         80, 13, 2, 1, 0, 80, 10)

        self.spriteManager.addSpriteMoving("_pos0")
        self.spriteManager.addSpriteMoving("_pos1")
        self.spriteManager.addSpriteMoving("_pos0")
        self.spriteManager.addSpriteMoving("_pos2")

        self.spriteManager.addSpriteAttack("_pos0")
        self.spriteManager.addSpriteAttack("_pos0", shiftY=-1)
        self.spriteManager.addSpriteAttack("_pos0", shiftY=-2)
        self.spriteManager.addSpriteAttack("_pos0", shiftY=-1)

    def attack(self):
        super().attack()

    def movementToTarget(self, tileMap: MatrixMap, delta_time: float = 1):
        super().movementToTarget(tileMap)

    def randomMovement(self, tileMap: MatrixMap, delta_time: float = 1):
        super().randomMovement(tileMap)

    def draw(self, scene: Scene):
        self.spriteManager.setDir(super().dirX, super().dirY)  # Установка направления движения
        spriteName, shifts = self.spriteManager.getSprite(self._currentSpeed, applyDir=True)  # Получение имя спрайта
        print(spriteName)
        x = int(self.x + shifts[0])
        y = int(self.y + shifts[1]) - const.getHeightSprite(self.spriteManager.baseSpriteName)
        scene.drawSprite(spriteName, x, y)
