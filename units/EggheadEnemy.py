import const
from draw import Scene
from events import Events
from map import MatrixMap
from objects import Stats
from units import Player
from units.Enemy import Enemy


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

        self.spriteManager.addAction(const.ACTION_NONE, True)
        self.spriteManager.addSprite(const.ACTION_NONE, "_pos0")
        self.spriteManager.setBaseAction(const.ACTION_NONE)

        self.spriteManager.addAction(const.ACTION_MOVING, True)
        self.spriteManager.addSprite(const.ACTION_MOVING, "_pos0")
        self.spriteManager.addSprite(const.ACTION_MOVING, "_pos1")
        self.spriteManager.addSprite(const.ACTION_MOVING, "_pos0")
        self.spriteManager.addSprite(const.ACTION_MOVING, "_pos2")

        self.spriteManager.addAction(const.ACTION_ATTACK, True, True)
        self.spriteManager.addSprite(const.ACTION_ATTACK, "_pos0")
        self.spriteManager.addSprite(const.ACTION_ATTACK, "_pos0", shiftY=-1)
        self.spriteManager.addSprite(const.ACTION_ATTACK, "_pos0", shiftY=-2)
        self.spriteManager.addSprite(const.ACTION_ATTACK, "_pos0", shiftY=-1)

    def attack(self, frameCount):
        super().attack(frameCount)

    def movementToTarget(self, events: Events, tileMap: MatrixMap, delta_time: float = const.DELTA_TIME):
        """
        Перемещение к игроку.
        :param events:  Инструмент получения событий.
        :param tileMap: Карта тайлов.
        :param delta_time:  Время между кадрами.
        """
        super().movementToTarget(events, tileMap, delta_time)

    def randomMovement(self, events: Events, tileMap: MatrixMap, delta_time: float = const.DELTA_TIME):
        """
        Перемещение в случайном направлении.
        :param events:  Инструмент получения событий.
        :param tileMap: Карта тайлов.
        :param delta_time:  Время между кадрами.
        """
        super().randomMovement(events, tileMap, delta_time)

    def draw(self, scene: Scene, delta_time: float = const.DELTA_TIME):
        """
        Отрисовка врага.
        :param delta_time: Время между кадрами.
        :param scene: Сцена для отображения объектов
        """
        self.spriteManager.setDir(super().dirX, super().dirY)  # Установка направления движения
        spriteName, shifts = self.spriteManager.getSprite(self._currentSpeed * delta_time)  # Получение имя спрайта

        x = int(self.x + shifts[0])
        y = int(self.y + shifts[1])

        # Установка спрайта гарантирует корректный расчёт столкновения спрайтов
        super().setSprite(spriteName)
        scene.drawSprite(spriteName, x, y)
