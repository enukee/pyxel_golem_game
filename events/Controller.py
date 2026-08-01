from abc import ABC, abstractmethod


class Controller(ABC):
    def __init__(self, buttonLeft, buttonRight, buttonDown, buttonUp, buttonShoot,
                 buttonInteract, buttonInventory, mouseBtnLeft, mouseBtnRight):
        self.buttonLeft = buttonLeft
        self.buttonRight = buttonRight
        self.buttonDown = buttonDown
        self.buttonUp = buttonUp
        self.buttonShoot = buttonShoot
        self.buttonInteract = buttonInteract
        self.buttonInventory = buttonInventory
        self.mouseBtnLeft = mouseBtnLeft
        self.mouseBtnRight = mouseBtnRight

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

    def __isMouseInArea(self, x: int, y: int, w: int, h: int):
        """
        Проверка, что курсор находится в некоторой области (x, y) размером w на h.
        """
        mouseX, mouseY = self.getMouse()
        return x < mouseX < x + w and y < mouseY < y + h

    def isMouseClickedLeft(self, x: int, y: int, w: int, h: int):
        """
        Нажатие левой кнопки мыши в некоторой области (x, y) размером w на h.
        """
        return self.__isMouseInArea(x, y, w, h) and self.isBtnClick(self.mouseBtnLeft)

    def isMouseClickedRight(self, x: int, y: int, w: int, h: int):
        """
        Нажатие левой кнопки мыши в некоторой области (x, y) размером w на h.
        """
        return self.__isMouseInArea(x, y, w, h) and self.isBtnClick(self.mouseBtnRight)

    def isLeftButtonPressed(self) -> bool:
        """
        Нажата ли кнопка движения влево.
        """
        if self.isBtnPress(self.buttonLeft):
            return True

        return False

    def isRightButtonPressed(self) -> bool:
        """
        Нажата ли кнопка движения вправо.
        """
        if self.isBtnPress(self.buttonRight):
            return True

        return False

    def isDownButtonPressed(self) -> bool:
        """
        Нажата ли кнопка движения вниз.
        """
        if self.isBtnPress(self.buttonDown):
            return True

        return False

    def isUpButtonPressed(self) -> bool:
        """
        Нажата ли кнопка движения вверх.
        """
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

    def isInteractButtonPressed(self) -> bool:
        """
        Кнопка взаимодействия с объектом.
        """
        if self.isBtnClick(self.buttonInteract):
            return True

        return False

    def getDirection(self) -> (int, int):
        """
        Получить направление движения игрока в формате.
        """
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
