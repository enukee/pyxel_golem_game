from events import Controller

import pyxel


class PyxelController(Controller):
    def __init__(self):
        super().__init__(pyxel.KEY_A, pyxel.KEY_D, pyxel.KEY_S, pyxel.KEY_W,
                         pyxel.KEY_KP_ENTER, pyxel.KEY_E)

    def isBtnPress(self, btn):
        pyxel.btn(btn)
