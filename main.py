import pyxel

import const
from events import Events
from map import MatrixMap
from units import Player
from events import PyxelController
from draw import Scene


class Game:
    def __init__(self):
        self.tileMap = MatrixMap()
        self.player = Player(30, 200)

        self.scene = Scene(const.WINDOW_WIDTH, const.WINDOW_HEIGHT, "Game")
        self.events = Events(PyxelController())

        def movement(dirX, dirY):
            self.player.update(dirX, dirY, self.tileMap)

        self.events.addPlayerMovementHandler(movement)

        pyxel.run(self.update, self.draw)

    def update(self):
        self.events.update()

    def draw(self):
        # Очистка экрана
        pyxel.cls(15)

        self.tileMap.draw(self.scene, self.player.x, self.player.y)
        self.player.draw(self.scene)


if __name__ == "__main__":
    Game()
