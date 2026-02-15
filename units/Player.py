import const
from map.MatrixMap import MatrixMap
from draw import Scene
from units import GameActor, Stats


class Player(GameActor):
    def __init__(self, x: float, y: float, stats: Stats):
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

    def draw(self, scene: Scene):
        self.spriteManager.setDir(super().dirX, super().dirY)       # Установка направления игрока
        spriteName, shift = self.spriteManager.getSprite(self._currentSpeed, applyDir=True)    # Получение имя спрайта

        scene.changingView(int(self.x) - const.WINDOW_WIDTH // 2, int(self.y) - const.WINDOW_HEIGHT // 2)
        scene.drawSprite(spriteName,
                         int(self.x), int(self.y) - const.getHeightSprite(self.spriteManager.baseSpriteName))

    def update(self, tileMap: MatrixMap,  delta_time: float = 1):
        if super().dirX == 0 and super().dirY == 0:
            super().speedReset()
            return

        super().update(tileMap, delta_time)

    def die(self):
        pass

