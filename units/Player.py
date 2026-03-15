import const
from events import Events
from map.MatrixMap import MatrixMap
from draw import Scene
from units import GameActor, Stats
from units import BaseBullet


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

        self.isAlive = True

        self.bullets = []

    def draw(self, scene: Scene, delta_time: float = const.DELTA_TIME):
        """
        Отрисовка игрока.
        :param delta_time: Время между кадрами.
        :param scene: Сцена для отображения объектов
        """
        self.spriteManager.setDir(super().dirX, super().dirY)       # Установка направления игрока
        spriteName, shift = self.spriteManager.getSprite(self._currentSpeed * delta_time, applyDir=True)    # Получение имя спрайта

        scene.changingView(int(self.x), int(self.y))
        scene.drawSprite(spriteName,
                         int(self.x), int(self.y) - const.getHeightSprite(self.spriteManager.baseSpriteName))

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
            super().speedReset()

        else:
            super().update(events, tileMap, delta_time)

        # Отрисовка всех снарядов
        for bul in self.bullets:
            bul.update(tileMap)

        return not self.isAlive

    def attack(self, frameCount):
        if frameCount - self.lastAttackTime > self._stats.attackSpeed:
            self.lastAttackTime = frameCount
            self.bullets.append(BaseBullet(self.x, self.y - const.getHeightSprite(
                self.spriteManager.baseSpriteName) / 2, self.spriteManager.dirX, self.spriteManager.dirY))

    def getDamage(self, val):
        if self._stats.takingDamage(val) is not None:
            self.isAlive = False

