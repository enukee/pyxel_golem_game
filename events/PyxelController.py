from events import Controller

import pyxel


class PyxelController(Controller):
    def __init__(self):
        self.buttonLeft = pyxel.KEY_A
        self.buttonRight = pyxel.KEY_D
        self.buttonDown = pyxel.KEY_S
        self.buttonUp = pyxel.KEY_W
        self.buttonShoot = pyxel.KEY_KP_ENTER
        self.buttonRaise = pyxel.KEY_E

    def isLeftButtonPressed(self) -> bool:
        if pyxel.btn(self.buttonLeft):
            return True

        return False

    def isRightButtonPressed(self) -> bool:
        if pyxel.btn(self.buttonRight):
            return True

        return False

    def isDownButtonPressed(self) -> bool:
        if pyxel.btn(self.buttonDown):
            return True

        return False

    def isUpButtonPressed(self) -> bool:
        if pyxel.btn(self.buttonUp):
            return True

        return False

    def isShootButtonPressed(self) -> bool:
        if pyxel.btn(self.buttonShoot):
            return True

        return False

    def isRaiseButtonPressed(self) -> bool:
        if pyxel.btn(self.buttonRaise):
            return True

        return False

    def getDirection(self) -> (int, int):
        dx, dy = 0, 0

        if self.isLeftButtonPressed():
            dx += -1

        if self.isRightButtonPressed():
            dx += 1

        if self.isUpButtonPressed():
            dy += -1

        if self.isDownButtonPressed():
            dy += 1

        return dx, dy
