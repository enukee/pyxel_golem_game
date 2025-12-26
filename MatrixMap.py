import MapGenerator as g
import Tile
import const
from draw import Scene


class MatrixMap:
    def __init__(self, size=11):
        """
        Матрица игрового поля содержащая тайлы.
        :param size: Размер игрового поля в тайлах.
        """
        self.__size = size

        # Генерация карты дорог
        matrix = g.MapGenerator.generateMap(self.__size, self.__size)
        # Преобразование карты в матрицу состоящую из тайлов
        self.__matrix = [
            [
                Tile.HorizontalRoadTile(j, i) if num == 1 else
                Tile.VerticalRoadTile(j, i) if num == 2 else
                Tile.LowerLeftCornerTile(j, i) if num == 3 else
                Tile.UpperRightCornerTile(j, i) if num == 4 else
                Tile.EmptyTile(j, i)
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
