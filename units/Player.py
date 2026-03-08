import const
from map.MatrixMap import MatrixMap
from draw import Scene
from units import GameActor, Stats


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

    def draw(self, scene: Scene):
        """
        Отрисовка игрока.
        :param scene: Сцена для отображения объектов
        """
        self.spriteManager.setDir(super().dirX, super().dirY)       # Установка направления игрока
        spriteName, shift = self.spriteManager.getSprite(self._currentSpeed, applyDir=True)    # Получение имя спрайта

        scene.changingView(int(self.x) - const.WINDOW_WIDTH // 2, int(self.y) - const.WINDOW_HEIGHT // 2)
        scene.drawSprite(spriteName,
                         int(self.x), int(self.y) - const.getHeightSprite(self.spriteManager.baseSpriteName))

        self._stats.draw(scene)

    def update(self, tileMap: MatrixMap,  delta_time: float = 1):
        """
        Обновление(перемещение) игрока.
        :param tileMap: Карта тайлов.
        :param delta_time:  Время между кадрами.
        :return: Возвращает False если игрок жив.
        """
        if super().dirX == 0 and super().dirY == 0:
            super().speedReset()
            return

        super().update(tileMap, delta_time)

        return not self.isAlive

    def getDamage(self, val):
        if self._stats.takingDamage(val) is None:
            self.isAlive = False

