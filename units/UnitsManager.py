import random

import const
from draw import Scene
from map import MatrixMap
from units import EggheadEnemy, MimicEnemy, Stats


class UnitsManager:
    def __init__(self, player, tileMap: MatrixMap, chanceEnemy: dict, countEnemy=200):
        """
        Менеджер юнитов, отображает и обновляет юниты на карте.
        :param player: Игрок.
        :param tileMap: Карта тайлов.
        """
        self.units = []         # Список всех юнитов на карте
        self.nearbyUnits = []   # Список отображаемых юнитов

        # Вероятности появления врага
        self.keysEnemy = list(chanceEnemy.keys())
        self.chance = list(chanceEnemy.values())

        self.player = player

        for i in range(countEnemy):
            x, y = tileMap.randomPoint()
            self.units.append(self.randomEnemy(x, y))

    def randomEnemy(self, x: int, y: int):
        """
        Создание случайного юнита.
        :param x: Стартовая позиция юнита по оси X.
        :param y: Стартовая позиция юнита по оси Y.
        :return: Юнит.
        """

        # Выбор врага
        enemy = random.choices(self.keysEnemy, weights=self.chance, k=1)[0]

        if enemy == "mimic":
            return MimicEnemy(x, y, self.player,
                              Stats(80,
                                    random.randint(10, 30),
                                    random.randint(1, 10) * 0.001,
                                    40, 0))

        elif enemy == "egg_head":
            return EggheadEnemy(x, y, self.player,
                                Stats(60,
                                      random.randint(15, 30),
                                      random.randint(1, 10) * 0.001,
                                      50, 0))

    def update(self, tileMap: MatrixMap) -> bool:
        """
        Обновление юнитов.
        :param tileMap: Карта тайлов.
        :return: Возвращает False если игрок жив.
        """
        # Габариты окна отрисовки спрайтов
        left = self.player.x - const.WINDOW_WIDTH
        right = left + 2 * const.WINDOW_WIDTH

        up = self.player.y - const.WINDOW_HEIGHT
        down = up + 2 * const.WINDOW_HEIGHT

        # Генератор отбора юнитов вблизи
        def gen():
            for u in self.units:
                if left < u.x < right and up < u.y < down:
                    yield u

        # Получение списка юнитов вблизи
        self.nearbyUnits = list(gen())

        # Обновление отображаемых юнитов
        for u in self.nearbyUnits:
            if u.update(tileMap) and u in self.nearbyUnits:
                # Удаление юнита из всех списков в случае его смерти
                self.units.remove(u)
                self.nearbyUnits.remove(u)

        # Добавление игрока в список отображаемых юнитов
        self.nearbyUnits.append(self.player)
        return self.player.update(tileMap)

    def draw(self, scene: Scene):
        """
        Отрисовка спрайтов.
        :param scene: Сцена.
        """
        self.nearbyUnits.sort(key=lambda x: x.y)
        for u in self.nearbyUnits:
            u.draw(scene)
