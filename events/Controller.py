from abc import ABC, abstractmethod


class Controller(ABC):
    def __init__(self, buttonLeft, buttonRight, buttonDown, buttonUp, buttonShoot,
                 buttonRaise, buttonInventory, mouseBtnLeft):
        self.buttonLeft = buttonLeft
        self.buttonRight = buttonRight
        self.buttonDown = buttonDown
        self.buttonUp = buttonUp
        self.buttonShoot = buttonShoot
        self.buttonRaise = buttonRaise
        self.buttonInventory = buttonInventory
        self.mouseBtnLeft = mouseBtnLeft

    @abstractmethod
    def isBtnPress(self, btn) -> bool:
        pass

    @abstractmethod
    def isBtnClick(self, btn) -> bool:
        pass

    @abstractmethod
    def getMouse(self):
        pass

    @abstractmethod
    def getFrameCount(self):
        pass

    def isMouseClicked(self, x: int, y: int, w: int, h: int):
        mouseX, mouseY = self.getMouse()
        return x < mouseX < x + w and y < mouseY < y + h and self.isBtnPress(self.mouseBtnLeft)

    def isLeftButtonPressed(self) -> bool:
        if self.isBtnPress(self.buttonLeft):
            return True

        return False

    def isRightButtonPressed(self) -> bool:
        if self.isBtnPress(self.buttonRight):
            return True

        return False

    def isDownButtonPressed(self) -> bool:
        if self.isBtnPress(self.buttonDown):
            return True

        return False

    def isUpButtonPressed(self) -> bool:
        if self.isBtnPress(self.buttonUp):
            return True

        return False

    def isShootButtonPressed(self) -> bool:
        """
        Кнопка стрельбы.
        """
        if self.isBtnPress(self.buttonShoot):
            return True

        return False

    def isInventoryButtonPressed(self) -> bool:
        """
        Кнопка открыть/закрыть инвентарь.
        """
        if self.isBtnClick(self.buttonInventory):
            return True

        return False

    def isRaiseButtonPressed(self) -> bool:
        """
        Кнопка открыть/закрыть сундук.
        """
        if self.isBtnPress(self.buttonRaise):
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
