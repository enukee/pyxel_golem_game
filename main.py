import pyxel

import const
from Game import Game
from Menu import Menu
from draw import PyxelDrawer
from events import PyxelController


class Start:
    def __init__(self):
        self.drawer = PyxelDrawer(const.WINDOW_WIDTH, const.WINDOW_HEIGHT, "Game")
        self.control = PyxelController()

        self.game = None
        self.mainMenu = Menu()

        def startGame():
            self.game = Game(self.drawer, self.control)
            self.drawer.mouseVisible(False)

        def exitApp():
            pyxel.quit()

        self.mainMenu.setHandler("play", startGame)
        self.mainMenu.setHandler("exit", exitApp)

        pyxel.mouse(True)
        pyxel.run(self.update, self.draw)

    def update(self):
        if self.game is not None:
            if self.game.update():
                self.game = None
                self.drawer.mouseVisible(True)
                self.drawer.setCamera(0, 0)

        else:
            self.mainMenu.update(self.control)

    def draw(self):
        if self.game is not None:
            # Очистка экрана
            pyxel.cls(15)
            self.game.draw()

        else:
            self.mainMenu.draw(self.drawer)


if __name__ == "__main__":
    Start()
