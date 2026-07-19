import random

import const
from draw import Scene
from events import Events
from map import MatrixMap
from units import EggheadEnemy, MimicEnemy, Stats, BackgroundMapObject


class UnitsManager:
    def __init__(self, player, tileMap: MatrixMap, chanceEnemy: dict, countEnemy=200, countBackObj=900):
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
        self.player.setUnitManager(self)
        self.bullets = []

        for i in range(countEnemy):
            x, y = tileMap.randomPoint()
            enemy = self.randomEnemy(x, y)
            self.units.append(enemy)
            enemy.setUnitManager(self)

        print(len(self.units))
        points = tileMap.randomPoints()
        for i in points:
            self.units.append(BackgroundMapObject(i[0], i[1]))

        print(len(self.units))

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
                                    random.randint(5, 10),
                                    random.randint(50, 150),
                                    25, 0))

        elif enemy == "egg_head":
            return EggheadEnemy(x, y, self.player,
                                Stats(60,
                                      random.randint(3, 8),
                                      random.randint(70, 100),
                                      55, 0))

    def update(self, events: Events, tileMap: MatrixMap) -> bool:
        """
        Обновление юнитов.
        :param events:  Инструмент получения событий.
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
            # Фоновые объекты не нужно обновлять т.к. они чисто декоративные
            if isinstance(u, BackgroundMapObject):
                continue

            if u.update(events, tileMap) and u in self.nearbyUnits:
                # Удаление юнита из всех списков в случае его смерти
                self.units.remove(u)
                self.nearbyUnits.remove(u)

        # Добавление игрока в список отображаемых юнитов
        self.nearbyUnits.append(self.player)
        return self.player.update(events, tileMap)

    def draw(self, scene: Scene):
        """
        Отрисовка спрайтов.
        :param scene: Сцена.
        """
        self.nearbyUnits.sort(key=lambda x: x.standY)
        for u in self.nearbyUnits:
            u.draw(scene)

    def isWalkable(self, x2, y2, unit):
        for u in self.nearbyUnits:
            # Проверка, что это не один и тот же юнит
            if unit == u:
                continue

            # Фоновые объекты неосязаемы
            if isinstance(u, BackgroundMapObject):
                continue

            x1, y1, w1, h1 = u.standPos
            _, _, w2, h2 = unit.standPos
            if const.rectanglesIntersect(x1, y1, w1, h1, x2, y2, w2, h2):
                return u

        return None
