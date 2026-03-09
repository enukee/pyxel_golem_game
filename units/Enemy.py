import math
from abc import ABC, abstractmethod
import random

import const
from units import GameActor, Player, Stats
from map import MatrixMap
from draw import Scene


class Enemy(GameActor, ABC):
    def __init__(self, x: float, y: float, player: Player, baseSpriteName: str,
                 stats: Stats, detectionRadius: float, attackRadius: float):
        """
        Базовый класс врага.
        :param x: Начальная координата X.
        :param y: Начальная координата Y.
        :param baseSpriteName: Базовое имя спрайта.
        :param stats: Характеристики врага.
        :param detectionRadius: Радиус обнаружения.
        :param attackRadius: Радиус атаки.
        """
        super().__init__(x, y, baseSpriteName, stats)
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
        self.player.getDamage(self._stats.attack * self._stats.attackSpeed)

    def isPlayerNearby(self, radiusSquare: float):
        """
        Поиск игрока в радиусе radiusSquare.
        :param radiusSquare: Радиус поиска.
        :return: Возвращает True если игрок находится в заданном радиусе.
        """
        dx = self.player.x - self.x
        dy = self.player.y - self.y
        return dx * dx + dy * dy <= radiusSquare

    def update(self, tileMap: MatrixMap, delta_time: float = const.DELTA_TIME) -> bool:
        """
        Обновление(перемещение) врага.
        :param tileMap: Карта тайлов.
        :param delta_time:  Время между кадрами.
        :return: Возвращает False если юнит жив.
        """
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

        return False

    @abstractmethod
    def movementToTarget(self, tileMap: MatrixMap, delta_time: float = const.DELTA_TIME):
        """
        Перемещение к игроку.
        :param tileMap: Карта тайлов.
        :param delta_time:  Время между кадрами.
        """
        super().setDir(int(self.player.x - self.x), int(self.player.y - self.y))
        super().update(tileMap, delta_time)

    @abstractmethod
    def randomMovement(self, tileMap: MatrixMap, delta_time: float = const.DELTA_TIME):
        """
        Перемещение в случайном направлении.
        :param tileMap: Карта тайлов.
        :param delta_time:  Время между кадрами.
        """
        # Движение в случайном направлении
        super().update(tileMap, delta_time)

        # Случайное изменение направления (опционально)
        if random.random() < 0.05:  # 5% шанс сменить направление
            super().setDir(random.choice([-1, 0, 1]), random.choice([-1, 0, 1]))


class EggheadEnemy(Enemy):
    def __init__(self, x: float, y: float, player: Player, stats: Stats):
        """
        Юнит врага Egghead.
        :param x: Начальная координата X.
        :param y: Начальная координата Y.
        :param player: Ссылка на игрока.
        :param stats: Характеристики врага.
        """
        super().__init__(x, y, player, "egghead",
                         stats, 80, 13)

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

    def movementToTarget(self, tileMap: MatrixMap, delta_time: float = const.DELTA_TIME):
        """
        Перемещение к игроку.
        :param tileMap: Карта тайлов.
        :param delta_time:  Время между кадрами.
        """
        super().movementToTarget(tileMap)

    def randomMovement(self, tileMap: MatrixMap, delta_time: float = const.DELTA_TIME):
        """
        Перемещение в случайном направлении.
        :param tileMap: Карта тайлов.
        :param delta_time:  Время между кадрами.
        """
        super().randomMovement(tileMap)

    def draw(self, scene: Scene):
        """
        Отрисовка врага.
        :param scene: Сцена для отображения объектов
        """
        self.spriteManager.setDir(super().dirX, super().dirY)  # Установка направления движения
        spriteName, shifts = self.spriteManager.getSprite(self._currentSpeed, applyDir=True)  # Получение имя спрайта

        x = int(self.x + shifts[0])
        y = int(self.y + shifts[1]) - const.getHeightSprite(self.spriteManager.baseSpriteName)
        scene.drawSprite(spriteName, x, y)


class MimicEnemy(Enemy):
    def __init__(self, x: float, y: float, player: Player, stats: Stats):
        """
        Юнит врага Mimic.
        :param x: Начальная координата X.
        :param y: Начальная координата Y.
        :param player: Ссылка на игрока.
        :param stats: Характеристики врага.
        """
        super().__init__(x, y, player, "mimic", stats, 90, 15)

        self.jump_height = 10  # Максимальная высота прыжка
        self.jump_duration = 10  # Длительность прыжка в кадрах
        self.isJumping = False
        self.jump_progress = 0

        # Стартовая позиция при прыжке
        self.start_x = 0
        self.start_y = 0
        # Целевая позиция при прыжке
        self.target_x = 0
        self.target_y = 0

        self.spriteManager.addSpriteMoving("")
        self.spriteManager.addSpriteMoving("")
        self.spriteManager.addSpriteMoving("")
        self.spriteManager.addSpriteMoving("")
        self.spriteManager.addSpriteMoving("_bite", shiftY=2)

        self.spriteManager.addSpriteAttack("")
        self.spriteManager.addSpriteAttack("_bite", shiftY=2)

    def setDir(self, dirX, dirY):
        """
        Установка стартовых параметров при прыжке.
        :param dirX: Направление по оси X.
        :param dirY: Направление по оси Y.
        """
        super().setDir(dirX, dirY)      # Установка направления у базового класса
        self.start_x = self.x
        self.start_y = self.y
        # Вычисление целевой позиции при прыжке
        self.target_x = self.start_x + self.jump_duration * super().dirX
        self.target_y = self.start_y + self.jump_duration * super().dirY
        self.isJumping = True       # Флаг начала прыжка
        self.jump_progress = 0

    def attack(self):
        super().attack()

    def movementToTarget(self, tileMap: MatrixMap, delta_time: float = const.DELTA_TIME):
        """
        Перемещение в случайном направлении.
        :param tileMap: Карта тайлов.
        :param delta_time: Время между кадрами.
        """
        if self.isJumping:
            self.jumping(tileMap)

        else:
            self.setDir(int(self.player.x - self.x), int(self.player.y - self.y))

    def randomMovement(self, tileMap: MatrixMap, delta_time: float = const.DELTA_TIME):
        """
        Перемещение в случайном направлении.
        :param tileMap: Карта тайлов.
        :param delta_time:  Время между кадрами.
        """
        if self.isJumping:
            self.jumping(tileMap, delta_time)

        # Случайное изменение направления (опционально)
        elif random.random() < 0.05:  # 5% шанс сменить направление
            self.setDir(random.choice([-1, 0, 1]), random.choice([-1, 0, 1]))

    def jumping(self, tileMap: MatrixMap, delta_time: float = const.DELTA_TIME):
        """
        Итерация прыжка из точки (self.start_x, self.start_y) в точку (self.target_x, self.target_y).
        :param tileMap: Карта тайлов.
        :param delta_time: Время между кадрами.
        """
        self.jump_progress += 1
        step = delta_time * self._stats.speed
        self.jump_progress += step
        # Прогресс прыжка от 0 до 1
        progress = self.jump_progress / self.jump_duration

        if progress <= 1:
            # Вычисляем приращения dx и dy
            dx = (self.target_x - self.start_x) * (step / self.jump_duration)
            dy = (self.target_y - self.start_y) * (step / self.jump_duration) - self.jump_height * math.sin(
                math.pi * progress) + self.jump_height * math.sin(math.pi * (progress - step / self.jump_duration))

            # Перемещаем
            super().tryMove(dx, dy, tileMap)
        else:
            # Прыжок завершён
            self.isJumping = False

    def draw(self, scene: Scene):
        """
        Отрисовка врага.
        :param scene: Сцена для отображения объектов
        """
        self.spriteManager.setDir(super().dirX, super().dirY)  # Установка направления движения
        spriteName, shifts = self.spriteManager.getSprite(self._currentSpeed, applyDir=False)  # Получение имя спрайта

        x = int(self.x + shifts[0])
        y = int(self.y + shifts[1]) - const.getHeightSprite(self.spriteManager.baseSpriteName)
        scene.drawSprite(spriteName, x, y)
