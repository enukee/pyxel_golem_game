import pyxel

from MatrixMap import *


class Game:
    def __init__(self):
        self.scene = Scene(const.WINDOW_WIDTH, const.WINDOW_HEIGHT, "Game")
        self.tileMap = MatrixMap()

        pyxel.run(self.update, self.draw)

    def update(self):
        pass

    def draw(self):
        # Очистка экрана
        pyxel.cls(1)
        self.tileMap.draw(self.scene, 300, 300)


if __name__ == "__main__":
    Game()
