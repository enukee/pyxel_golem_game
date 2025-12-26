import const
from MatrixMap import MatrixMap
from draw import Scene
from units import GameActor


class Player(GameActor):
    def __init__(self, x: float, y: float):
        super().__init__(x, y, "player_down", 100, 1, 1, 1, 0.1)

    def draw(self, scene: Scene):
        scene.changingView(int(self.x) - const.WINDOW_WIDTH // 2, int(self.y) - const.WINDOW_HEIGHT // 2)
        scene.drawSprite(self.baseSprite, int(self.x), int(self.y) - const.getHeightSprite(self.baseSprite))

    def update(self, dirX: float, dirY: float, tileMap: MatrixMap,  delta_time: float = 1):
        if dirX == 0 and dirY == 0:
            super().speedReset()
            return

        super().update(dirX, dirY, tileMap, delta_time)

    def die(self):
        pass

