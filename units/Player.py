import const
from map.MatrixMap import MatrixMap
from draw import Scene
from units import GameActor


class Player(GameActor):
    def __init__(self, x: float, y: float):
        super().__init__(x, y, "player", 100, 1, 1, 1, 0.1)

        # Установка последовательности смены спрайтов во время движения
        self.spriteManager.addSpriteModifier("_pos0")
        self.spriteManager.addSpriteModifier("_pos1")
        self.spriteManager.addSpriteModifier("_pos2")
        self.spriteManager.addSpriteModifier("_pos1")
        self.spriteManager.addSpriteModifier("_pos0")
        self.spriteManager.addSpriteModifier("_pos3")
        self.spriteManager.addSpriteModifier("_pos4")
        self.spriteManager.addSpriteModifier("_pos3")

    def draw(self, scene: Scene):
        self.spriteManager.setDir(super().dirX, super().dirY)       # Установка направления игрока
        spriteName = self.spriteManager.getSpriteMoving(self._currentSpeed, applyDir=True)    # Получение имя спрайта

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

