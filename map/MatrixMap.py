import math
import random

from scipy.stats.qmc import PoissonDisk

from map import MapGenerator
from map.Tile import *
import const
from draw import Scene


def generate_poisson(r, k, width, height):
    # Результат и активный список
    points = []
    active = []

    # Первая точка в центре
    first_point = (width / 2, height / 2)
    points.append(first_point)
    active.append(first_point)

    while active:
        # Выбираем случайную точку из активного списка
        idx = random.randint(0, len(active) - 1)
        center = active[idx]

        # Пробуем сгенерировать k точек вокруг неё
        found = False
        for _ in range(k):
            # Случайный угол и расстояние от r до 2r
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(r, 2 * r)
            new_x = center[0] + distance * math.cos(angle)
            new_y = center[1] + distance * math.sin(angle)

            # Проверяем, что точка внутри области
            if not (0 <= new_x < width and 0 <= new_y < height):
                continue

            # Проверяем минимальное расстояние до всех существующих точек
            valid = True
            for point in points:
                dx = new_x - point[0]
                dy = new_y - point[1]
                if dx * dx + dy * dy < r * r:
                    valid = False
                    break

            if valid:
                points.append((new_x, new_y))
                active.append((new_x, new_y))
                found = True
                break

        # Удаляем центр из активного списка, если не удалось сгенерировать новую точку
        if not found:
            active.pop(idx)

    return points


class MatrixMap:
    def __init__(self, size=11):
        """
        Матрица игрового поля содержащая тайлы.
        :param size: Размер игрового поля в тайлах.
        """
        self.__size = size

        # Генерация карты дорог
        matrix = MapGenerator.generateMap(self.__size, self.__size)
        # Преобразование карты в матрицу состоящую из тайлов
        self.__matrix = [
            [
                HorizontalRoadTile(j, i) if num == 1 else
                VerticalRoadTile(j, i) if num == 2 else
                LowerLeftCornerTile(j, i) if num == 3 else
                UpperRightCornerTile(j, i) if num == 4 else
                EmptyTile(j, i)
                for j, num in enumerate(row)
            ]
            for i, row in enumerate(matrix)
        ]

    def draw(self, scene: Scene, x: float, y: float):
        """
        Отображение видимых тайлов.
        :param scene: Сцена содержащая методы отрисовки тайлов.
        :param x: Положение игрока по x.
        :param y: Положение игрока по y.
        """
        for row in [-const.TILE_SIZE, 0, const.TILE_SIZE]:
            for col in [-const.TILE_SIZE, 0, const.TILE_SIZE]:
                tile = self.getTile(x + col, y + row)
                if tile is not None:
                    tile.draw(scene)

    def getTile(self, worldX: float, worldY: float) -> Tile:
        """
        Получение тайла по глобальным координатам.
        :param worldX: Глобальная координата x.
        :param worldY: Глобальная координата y.
        :return: Тайл находящийся на этих координатах.
        """
        # Проверка, что координаты находятся в пределах матрицы тайлов
        globalSize = self.__size * const.TILE_SIZE
        if not (0 <= worldX < globalSize and 0 <= worldY < globalSize):
            return None

        tile_x, tile_y = int(worldX // const.TILE_SIZE), int(worldY // const.TILE_SIZE)
        return self.__matrix[tile_y][tile_x]

    def isWalkable(self, worldX: float, worldY: float):
        """
        Проверка возможности передвижения в координатах (x, y).
        :param worldX: Глобальная координата x.
        :param worldY: Глобальная координата y.
        :return: Флаг разрешающий передвижение.
        """
        tile = self.getTile(worldX, worldY)
        if tile is None:
            return False

        local_x = (worldX % const.TILE_SIZE) / const.TILE_SIZE
        local_y = (worldY % const.TILE_SIZE) / const.TILE_SIZE

        return tile.isWalkable(local_x, local_y)

    def randomPoint(self):
        size = self.__size * const.TILE_SIZE
        x, y = (random.randint(0, size),
                random.randint(0, size))
        while not self.isWalkable(x, y):
            x, y = (random.randint(0, size),
                    random.randint(0, size))

        return x, y

    def randomPoints(self):
        size = self.__size * const.TILE_SIZE
        radius = 40
        poisson = PoissonDisk(
            d=2,
            radius=radius/size,
            optimization="random-cd"
        )
        points = poisson.random(n=200)
        result = []
        for i in points:
            x, y = i[0] * size, i[1] * size
            if self.isWalkable(x, y):
                result.append([int(x), int(y)])

        return result
