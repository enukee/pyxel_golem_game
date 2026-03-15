from events import Controller

import pyxel


class PyxelController(Controller):
    def __init__(self):
        super().__init__(pyxel.KEY_A, pyxel.KEY_D, pyxel.KEY_S, pyxel.KEY_W,
                         pyxel.KEY_KP_ENTER, pyxel.KEY_E,
                         pyxel.MOUSE_BUTTON_LEFT)

    def isBtnPress(self, btn) -> bool:
        return pyxel.btn(btn)

    def getMouse(self):
        return pyxel.mouse_x, pyxel.mouse_y

    def getFrameCount(self):
        return pyxel.frame_count
