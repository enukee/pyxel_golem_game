from map.MatrixMap import MatrixMap


class MovableObjects:
    def __init__(self, x: float, y: float):
        """
        Объект способный передвигаться.
        :param x: Координата x объекта.
        :param y: Координата y объекта.
        """
        self.__x, self.__y = x, y

    def tryMove(self, dx: float, dy: float, tile_map: MatrixMap) -> bool:
        """
        Передвижение с проверкой.
        :param dx: Сдвиг по оси X.
        :param dy: Сдвиг по оси Y.
        :param tile_map: Карта тайлов.
        :return: Флаг успешного передвижения.
        """
        new_x, new_y = self.__x + dx, self.__y + dy
        if tile_map.isWalkable(new_x, new_y):
            self.__x, self.__y = new_x, new_y
            return True
        return False

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y
