from abc import ABC, abstractmethod


class Controller(ABC):
    @abstractmethod
    def isLeftButtonPressed(self) -> bool:
        pass

    @abstractmethod
    def isRightButtonPressed(self) -> bool:
        pass

    @abstractmethod
    def isDownButtonPressed(self) -> bool:
        pass

    @abstractmethod
    def isUpButtonPressed(self) -> bool:
        pass

    @abstractmethod
    def isShootButtonPressed(self) -> bool:
        pass

    @abstractmethod
    def isRaiseButtonPressed(self) -> bool:
        pass

    @abstractmethod
    def getDirection(self) -> (int, int):
        pass
