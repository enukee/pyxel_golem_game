from abc import abstractmethod, ABC


class Drawer(ABC):
    @abstractmethod
    def drawSprite(self, spritePos: list, x: int, y: int):
        pass

    @abstractmethod
    def drawIcon(self, iconPos: list, x: int, y: int):
        pass

    @abstractmethod
    def drawTileBorders(self, x: int, y: int):
        pass

    @abstractmethod
    def drawTile(self, sectors: list, x: int, y: int):
        pass

    @abstractmethod
    def drawButton(self, x: int, y: int, width: int, height: int, title: str):
        pass

    @abstractmethod
    def drawBackground(self):
        pass

    def setCamera(self, x: int, y: int):
        pass

    def drawHealth(self, val: int):
        pass
