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

    @property
    def value(self):
        return self.__value


class IncreaseBySummation(IncreaseParam):
    def __init__(self, name: str, value):
        """
        Увеличение некоторого параметра суммированием.
        :param name: Имя характеристики.
        :param value: Значение прибавки к характеристике.
        """
        super().__init__(name, value)

    def increase(self, base):
        return base + self.value


class PercentageIncrease(IncreaseParam):
    def __init__(self, name: str, value):
        """
        Процентное увеличение некоторого параметра.
        :param name: Имя характеристики.
        :param value: Значение прибавки к характеристике.
        """
        if not -100 <= abs(value) <= 100:
            raise ValueError('The value must be a percentage.')

        super().__init__(name, 1 + value / 100)

    def increase(self, base):
        return base * self.value


class Artifact(GameObject):
    def __init__(self, description: str, icon: str):
        super().__init__(0, 0, icon)

        self.__increase = []

        # Описание предмета
        self.__description = description

    def addIncrease(self, inc: IncreaseParam):
        self.__increase.append(inc)

    def applyIncrease(self, stats):
        for inc in self.__increase:
            stats.increase(inc)

    @property
    def description(self):
        return self.__description

    def update(self):
        pass

    def draw(self, scene: Scene):
        super().draw(scene)


class SilverFork(Artifact):
    def __init__(self):
        description = ("Silver Fork"
                       "\nattack: +5%")
        super().__init__(description, "fork")

        super().addIncrease(PercentageIncrease("attack", 4))


class FlowerVine(Artifact):
    def __init__(self):
        description = ("Flower Vine"
                       "\nattack: +7 points")
        super().__init__(description, "vine")

        super().addIncrease(IncreaseBySummation("attack", 7))


class MedicinalClover(Artifact):
    def __init__(self):
        description = ("Medicinal Clover"
                       "\nhealth: +25 points"
                       "\nspeed: +3 points")
        super().__init__(description, "clover")

        super().addIncrease(IncreaseBySummation("health", 25))
        super().addIncrease(IncreaseBySummation("speed", 3))


class ScarletBug(Artifact):
    def __init__(self):
        description = ("Scarlet beetle"
                       "\nattack speed: +3 points")
        super().__init__(description, "bug")

        super().addIncrease(IncreaseBySummation("attack_speed", 5))


class SilverRing(Artifact):
    def __init__(self):
        description = ("Silver Ring "
                       "\nattack_speed: -30%"
                       "\nattack: +30%")
        super().__init__(description, "ring")

        super().addIncrease(PercentageIncrease("attack_speed", -30))
        super().addIncrease(PercentageIncrease("attack", +30))


class MagicAmanita(Artifact):
    def __init__(self):
        description = ("Magic Amanita "
                       "\nhealth: -10 points"
                       "\nattack: +5%")
        super().__init__(description, "amanita")

        super().addIncrease(IncreaseBySummation("health", -10))
        super().addIncrease(PercentageIncrease("attack", 5))
