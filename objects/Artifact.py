from abc import ABC, abstractmethod

from draw import Scene
from objects import GameObject


class IncreaseParam(ABC):
    def __init__(self, name: str, value):
        """
        Увеличение некоторого параметра.
        :param name: Имя характеристики.
        :param value: Значение прибавки к характеристике.
        """
        self.__name = name
        self.__value = value

    @property
    def name(self):
        return self.__name

    @abstractmethod
    def increase(self, base):
        """
        Увеличение параметра.
        :param base: Базовое значение параметра.
        :return: Обновлённое значение параметра.
        """
        pass


class IncreaseBySummation(IncreaseParam):
    def __init__(self, name: str, value):
        """
        Увеличение некоторого параметра суммированием.
        :param name: Имя характеристики.
        :param value: Значение прибавки к характеристике.
        """
        super().__init__(name, value)

    def increase(self, base):
        return base + self.__value


class PercentageIncrease(IncreaseParam):
    def __init__(self, name: str, value):
        """
        Процентное увеличение некоторого параметра.
        :param name: Имя характеристики.
        :param value: Значение прибавки к характеристике.
        """
        if not 0 < abs(value) < 100:
            raise ValueError('The value must be a percentage.')

        super().__init__(name, 1 + value / 100)

    def increase(self, base):
        return base * self.__value


class Artifact(GameObject):
    def __init__(self, description: str, icon: str):
        super().__init__(0, 0, icon)

        self.__increase = []

        # Описание предмета
        self.__description = description

    @property
    def description(self):
        return self.__description

    def update(self):
        pass

    def draw(self, scene: Scene):
        super().draw(scene)


class SilverFork(Artifact):
    def __init__(self):
        description = "73473647"

        super().__init__(description, "fork")


class SilverRing(Artifact):
    def __init__(self):
        description = "ring"

        super().__init__(description, "ring")


class LuckyClover(Artifact):
    def __init__(self):
        description = "cldejiejdjeifjrfj"

        super().__init__(description, "clover")
