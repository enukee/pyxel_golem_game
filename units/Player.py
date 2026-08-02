import const
from events import Events
from map.MatrixMap import MatrixMap
from draw import Scene
from objects import Stats
from units import GameActor
from units import FireBullet


class Player(GameActor):
    def __init__(self, x: float, y: float, stats: Stats):
        """
        Класс игрока.
        :param x: Координата по оси X.
        :param y: Координата по оси Y.
        :param stats: Характеристики игрока.
        """
        super().__init__(x, y, "player", stats)

        # Установка последовательности смены спрайтов во время движения
        self.spriteManager.addSpriteMoving("_pos0")
        self.spriteManager.addSpriteMoving("_pos1")
        self.spriteManager.addSpriteMoving("_pos2")
        self.spriteManager.addSpriteMoving("_pos1")
        self.spriteManager.addSpriteMoving("_pos0")
        self.spriteManager.addSpriteMoving("_pos3")
        self.spriteManager.addSpriteMoving("_pos4")
        self.spriteManager.addSpriteMoving("_pos3")

        self.bullets = []

    def draw(self, scene: Scene, delta_time: float = const.DELTA_TIME):
        """
        Отрисовка игрока.
        :param delta_time: Время между кадрами.
        :param scene: Сцена для отображения объектов
        """
        scene.changingView(int(self.x), int(self.y))

        super().draw(scene, delta_time)

        # Отрисовка всех снарядов
        for bul in self.bullets:
            bul.draw(scene)

        self._stats.draw(scene)

    def update(self, events: Events, tileMap: MatrixMap,  delta_time: float = const.DELTA_TIME):
        """
        Обновление(перемещение) игрока.
        :param events: Инструмент получения событий.
        :param tileMap: Карта тайлов.
        :param delta_time:  Время между кадрами.
        :return: Возвращает False если игрок жив.
        """
        if super().dirX == 0 and super().dirY == 0:
            self._currentSpeed = 0

        elif self._currentSpeed == 0:
            super().speedReset()

        else:
            super().update(events, tileMap, delta_time)

        # Отрисовка всех снарядов
        for bul in self.bullets:
            bul.update(tileMap)

        return not self._stats.isAlive()

    def attack(self, frameCount):
        if frameCount - self.lastAttackTime > self._stats.attackSpeed:
            self.lastAttackTime = frameCount
            y = self.y + const.getHeightSprite(self.spriteManager.baseSpriteName) / 2

            # Костыль, если игрок стреляет вниз, то координата y сдвинута так,
            # чтобы игрок не попадал сам по себе
            if self.spriteManager.dirY == 1:
                y += 10

            bullet = FireBullet(self.x, y,
                                self.spriteManager.dirX,
                                self.spriteManager.dirY,
                                self._currentSpeed)
            bullet.setUnitManager(self.unitManager)
            self.bullets.append(bullet)
