import const
from debug_settings import DEBUG_SET_RENDER_BACKGROUND_OBJ
from draw import Scene
from events import Events
from map import MatrixMap
from units import EggheadEnemy, MimicEnemy, Stats, BackgroundMapObject
from units.EnemyCreator import EnemyCreator


class UnitsContainer:
    def __init__(self, player, tileMap: MatrixMap, countEnemy=200, countBackObj=900):
        """
        Контейнер юнитов, отображает и обновляет юниты на карте.
        :param player: Игрок.
        :param tileMap: Карта тайлов.
        """
        self.units = []         # Список всех юнитов на карте
        self.nearbyUnits = []   # Список отображаемых юнитов

        self.player = player
        self.player.setUnitManager(self)
        self.bullets = []

        enemyCreator = EnemyCreator(self.player)
        for i in range(countEnemy):
            x, y = tileMap.randomPoint()
            enemy = enemyCreator.randomEnemy(x, y)
            self.units.append(enemy)
            enemy.setUnitManager(self)

        if DEBUG_SET_RENDER_BACKGROUND_OBJ:
            points = tileMap.randomPoints()
            for i in points:
                self.units.append(BackgroundMapObject(i[0], i[1]))

    def update(self, events: Events, tileMap: MatrixMap) -> bool:
        """
        Обновление юнитов.
        :param events:  Инструмент получения событий.
        :param tileMap: Карта тайлов.
        :return: Возвращает False если игрок жив.
        """
        # Получение списка юнитов вблизи
        self.nearbyUnits = list(self.__nearbyUnitGenerator())

        # Обновление отображаемых юнитов
        for u in self.nearbyUnits:
            # Фоновые объекты не нужно обновлять т.к. они чисто декоративные
            if isinstance(u, BackgroundMapObject):
                continue

            if u in self.nearbyUnits and u.update(events, tileMap):
                # Удаление юнита из всех списков в случае его смерти
                self.units.remove(u)
                self.nearbyUnits.remove(u)

        # Добавление игрока в список отображаемых юнитов
        self.nearbyUnits.append(self.player)
        return self.player.update(events, tileMap)

    def __nearbyUnitGenerator(self):
        """
        Генератор отбора юнитов вблизи.
        """
        # Габариты окна отрисовки спрайтов
        left = self.player.x - const.WINDOW_WIDTH
        right = left + 2 * const.WINDOW_WIDTH

        up = self.player.y - const.WINDOW_HEIGHT
        down = up + 2 * const.WINDOW_HEIGHT

        for u in self.units:
            if left < u.x < right and up < u.y < down:
                yield u

    def draw(self, scene: Scene):
        """
        Отрисовка спрайтов.
        :param scene: Сцена.
        """
        self.nearbyUnits.sort(key=lambda x: x.standY)
        for u in self.nearbyUnits:
            u.draw(scene)

    def isWalkable(self, x2, y2, unit):
        """
        Проверка сталкивается ли unit с каким-либо другим юнитом.
        """
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
