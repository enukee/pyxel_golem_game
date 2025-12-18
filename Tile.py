from abc import ABC, abstractmethod

import const
from Scene import Scene


class Tile(ABC):
    class TileZone:
        def __init__(self, x1: float, y1: float, x2: float, y2: float, walkable=False):
            """
            Зона внутри тайла.
            :param x1: Координата x левого верхнего угла TileZone.
            :param y1: Координата y левого верхнего угла TileZone.
            :param x2: Координата x правого нижнего угла TileZone.
            :param y2: Координата y правого нижнего угла TileZone.
            :param walkable: Флаг разрешающий передвижение внутри TileZone.
            """
            self.isWalkable = walkable
            self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2

    def __init__(self, i: int, j: int):
        """
        Фрагмент карты.
        :param i: Индекс столбца внутри матрицы тайлов.
        :param j: Индекс строки внутри матрицы тайлов.
        """
        self.__x, self.__y = i * const.TILE_SIZE, j * const.TILE_SIZE  # Глобальные координаты тайла
        self.__tileZones = []  # Список зон внутри тайла

    @abstractmethod
    def draw(self, scene: Scene):
        """
        Отображение тайла.
        :param scene: Сцена содержащая методы отрисовки объектов.
        """
        pass

    @abstractmethod
    def update(self):
        """
        Обновление тайла
        """
        pass

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    def addTileZone(self, x1: float, y1: float, x2: float, y2: float):
        """
        Добавление новой зоны тайла.
        :param x1: Координата x левого верхнего угла TileZone.
        :param y1: Координата y левого верхнего угла TileZone.
        :param x2: Координата x правого нижнего угла TileZone.
        :param y2: Координата y правого нижнего угла TileZone.
        """
        self.__tileZones.append(self.TileZone(x1, y1, x2, y2))

    def isWalkable(self, x: float, y: float) -> bool:
        """
        Проверка возможности передвижения в координатах (x, y).
        :param x: Координата x.
        :param y: Координата y.
        :return: Флаг разрешающий передвижение.
        """
        for zone in self.__tileZones:
            if (zone.x1 <= x <= zone.x2) and (zone.y1 <= y <= zone.y2):
                return zone.isWalkable
        return True

    def __repr__(self):
        return f"Tile('{self.__x}', {self.__y})"


class EmptyTile(Tile):  # Пустой тайл
    def __init__(self, i, j):
        super().__init__(i, j)
        super().addTileZone(0., 0., 1., 1.)

    def draw(self, scene: Scene):
        pass

    def update(self):
        pass

    def __repr__(self):
        return f"EmptyTile('{self.x}', {self.y})"


class HorizontalRoadTile(Tile):  # Тайл с горизонтальным коридором
    def __init__(self, i, j):
        super().__init__(i, j)
        super().addTileZone(0., 0., 1., 0.5)

    def draw(self, scene: Scene):
        scene.drawTile("horizontal_road", self.x, self.y)

    def update(self):
        pass

    def __repr__(self):
        return f"HorizontalRoadTile('{self.x}', {self.y})"


class VerticalRoadTile(Tile):  # Тайл с вертикальным коридором
    def __init__(self, i, j):
        super().__init__(i, j)
        super().addTileZone(0.5, 0., 1., 1.)

    def draw(self, scene: Scene):
        scene.drawTile("vertical_road", self.x, self.y)

    def update(self):
        pass

    def __repr__(self):
        return f"VerticalRoadTile('{self.x}', {self.y})"


class LowerLeftCornerTile(Tile):  # Тайл с поворотом налево(тупиком)
    def __init__(self, i, j):
        super().__init__(i, j)
        super().addTileZone(0.5, 0., 1., 0.5)

    def draw(self, scene: Scene):
        scene.drawTile("lower_left_corner", self.x, self.y)

    def update(self):
        pass

    def __repr__(self):
        return f"LowerLeftCornerTile('{self.x}', {self.y})"


class UpperRightCornerTile(Tile):  # Тайл с поворотом направо
    def __init__(self, i, j):
        super().__init__(i, j)
        super().addTileZone(0., 0., 0.5, 0.5)
        super().addTileZone(0.5, 0., 1., 1.)

    def draw(self, scene: Scene):
        scene.drawTile("upper_right_corner", self.x, self.y)

    def update(self):
        pass

    def __repr__(self):
        return f"UpperRightCorner('{self.x}', {self.y})"
