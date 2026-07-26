import pyxel

import const
from Game import Game
from debug_settings import mapSaveImg, DEBUG_MAKE_IMG_MAP
from game_windows import Menu
from draw import PyxelDrawer
from events import PyxelController


class Start:
    def __init__(self):
        self.drawer = PyxelDrawer(const.WINDOW_WIDTH, const.WINDOW_HEIGHT, "Game")
        self.control = PyxelController()

        self.game = None
        self.mainMenu = Menu(self.drawer)

        def startGame(btn):
            self.game = Game(self.drawer, self.control)
            self.drawer.mouseVisible(False)

            if DEBUG_MAKE_IMG_MAP:
                self.game.player._MovableObjects__x = 0
                self.game.player._MovableObjects__y = 0

        def exitApp(btn):
            self.drawer.exit()

        if DEBUG_MAKE_IMG_MAP:
            startGame(None)

        self.mainMenu.setHandlerLeft("play", startGame)
        self.mainMenu.setHandlerLeft("exit", exitApp)

        pyxel.mouse(True)
        pyxel.run(self.update, self.draw)

    def update(self):
        if self.game is not None:
            if self.game.update():
                self.game = None
                self.drawer.mouseVisible(True)
                self.drawer.setCamera(0, 0)

            if DEBUG_MAKE_IMG_MAP:
                self.game.player._MovableObjects__x += 500
                self.game.player._MovableObjects__y += 500

        else:
            self.mainMenu.update(self.control)

    def draw(self):
        if self.game is not None:
            if DEBUG_MAKE_IMG_MAP:
                self.drawer.setCamera(0, 0)

            # Очистка экрана
            self.drawer.drawBackground()
            self.game.draw()
            if (DEBUG_MAKE_IMG_MAP and self.game.player.x > const.TILE_SIZE*const.TILE_COUNT
                    and self.game.player.y > const.TILE_SIZE*const.TILE_COUNT):
                mapSaveImg(self.drawer)
                self.drawer.exit()

        else:
            self.mainMenu.draw()


if __name__ == "__main__":
    Start()
