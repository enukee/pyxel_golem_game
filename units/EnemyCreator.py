from random import randint, choices

import const
from objects import Stats
from units import MimicEnemy, EggheadEnemy


class EnemyCreator:
    def __init__(self, player):
        self.player = player

        # Вероятности появления врага
        self.keysEnemy = list(const.CHANCE_ENEMY.keys())
        self.chance = list(const.CHANCE_ENEMY.values())

    def randomEnemy(self, x: int, y: int):
        """
        Создание случайного юнита.
        :param x: Стартовая позиция юнита по оси X.
        :param y: Стартовая позиция юнита по оси Y.
        :return: Юнит.
        """

        # Выбор врага
        enemy = choices(self.keysEnemy, weights=self.chance, k=1)[0]

        if enemy == "mimic":
            return MimicEnemy(x, y, self.player,
                              Stats(80,
                                    randint(5, 10),
                                    randint(50, 150),
                                    25, 0))

        elif enemy == "egg_head":
            return EggheadEnemy(x, y, self.player,
                                Stats(60,
                                      randint(3, 8),
                                      randint(70, 100),
                                      55, 0))
