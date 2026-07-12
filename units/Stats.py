from typing import Union

from draw import Scene
from objects import IncreaseParam


class Stats:
    # Ключи(имена) характеристик
    STAT_KEYS = ["health", "attack", "attack_speed", "speed", "acceleration"]

    INC_STAT_KEYS = ["health"]

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

        # Текущие параметры
        self.__currentStats = [health]

    def draw(self, scene: Scene):
        scene.drawHealth(self.currentHealth)

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

    def healing(self, val: int):
        self.health = min(self.health + val, self.__fullStats[Stats.STAT_KEYS.index("health")])

    def takingDamage(self, val: int) -> Union[None, int]:
        self.currentHealth -= val
        if self.currentHealth <= 0:
            return 1
        return None

    def isAlive(self):
        if self.currentHealth <= 0:
            return False
        return True

    @property
    def currentHealth(self):
        return self.__currentStats[Stats.INC_STAT_KEYS.index("health")]

    @currentHealth.setter
    def currentHealth(self, curHealth):
        self.__currentStats[Stats.INC_STAT_KEYS.index("health")] = curHealth

    @property
    def health(self):
        return self.__fullStats[Stats.STAT_KEYS.index("health")]

    @health.setter
    def health(self, health):
        self.__fullStats[Stats.INC_STAT_KEYS.index("health")] = health

    @property
    def attack(self):
        return self.__fullStats[Stats.STAT_KEYS.index("attack")]

    @attack.setter
    def attack(self, attack):
        self.__fullStats[Stats.INC_STAT_KEYS.index("attack")] = attack

    @property
    def attackSpeed(self):
        return self.__fullStats[Stats.STAT_KEYS.index("attack_speed")]

    @attackSpeed.setter
    def attackSpeed(self, attackSpeed):
        self.__fullStats[Stats.INC_STAT_KEYS.index("attack_speed")] = attackSpeed

    @property
    def speed(self):
        return self.__fullStats[Stats.STAT_KEYS.index("speed")]

    @speed.setter
    def speed(self, speed):
        self.__fullStats[Stats.INC_STAT_KEYS.index("speed")] = speed

    @property
    def acceleration(self):
        return self.__fullStats[Stats.STAT_KEYS.index("acceleration")]

    @acceleration.setter
    def acceleration(self, acceleration):
        self.__fullStats[Stats.INC_STAT_KEYS.index("acceleration")] = acceleration

    def getAllStats(self):
        return ("Health: " + str(self.currentHealth) + "/" + str(self.health) +
                "/nAttack: " + str(self.attack) +
                "/nAttack speed: " + str(self.attackSpeed) +
                "/nSpeed: " + str(self.speed) +
                "/nAcceleration: " + str(self.acceleration))
