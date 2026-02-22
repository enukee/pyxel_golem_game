from abc import ABC, abstractmethod


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


class Stats:

    # Ключи(имена) характеристик
    STAT_KEYS = ["health", "attack", "attack_speed", "speed", "acceleration"]

    def __init__(self, health: int, attack: int, attackSpeed: float, speed: float, acceleration: float):
        """
        Базовые параметры юнита.
        :param health: Базовое здоровье.
        :param attack: Очки брони.
        :param attackSpeed: Скорость атаки.
        :param speed: Начальная скорость.
        :param acceleration: Ускорение.
        """
        # Базовые параметры объекта
        self.__baseStats = [health, attack, attackSpeed, speed, acceleration]

        # Полные параметры объекта(с учётом всех усилений)
        self.__fullStats = self.__baseStats

    def getParam(self, name: str):
        """
        Получение параметра по ключу.
        :param name: Имя(ключ) параметра.
        :return: Значения параметра.
        """
        return self.__fullStats[Stats.STAT_KEYS.index(name)]

    def increase(self, incParam: IncreaseParam):
        """
        Увеличение параметра.
        :param incParam: Объект усиление параметра.
        """
        self.__fullStats[Stats.STAT_KEYS.index(incParam.name)] = incParam.increase(self.getParam(incParam.name))

    def reset(self):
        """
        Сброс параметров до базовых.
        """
        self.__fullStats = self.__baseStats

    @property
    def health(self):
        return self.__fullStats[Stats.STAT_KEYS.index("health")]

    @property
    def attack(self):
        return self.__fullStats[Stats.STAT_KEYS.index("attack")]

    @property
    def attackSpeed(self):
        return self.__fullStats[Stats.STAT_KEYS.index("attack_speed")]

    @property
    def speed(self):
        return self.__fullStats[Stats.STAT_KEYS.index("speed")]

    @property
    def acceleration(self):
        return self.__fullStats[Stats.STAT_KEYS.index("acceleration")]
