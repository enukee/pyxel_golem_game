import const
from draw import Scene
from map.MatrixMap import MatrixMap


class MovableObjects:
    def __init__(self, x: float, y: float):
        """
        Объект способный передвигаться.
        :param x: Координата x объекта.
        :param y: Координата y объекта.
        """
        self.__x, self.__y = x, y
        self.currentSprite = "stub_sprite"

    def tryMove(self, dx: float, dy: float, tile_map: MatrixMap) -> bool:
        """
        Передвижение с проверкой.
        :param dx: Сдвиг по оси X.
        :param dy: Сдвиг по оси Y.
        :param tile_map: Карта тайлов.
        :return: Флаг успешного передвижения.
        """
        ret = True

        # Проверка превышения правой границы с учётом ширины спрайта
        spriteWidth = abs(const.getWidthSprite(self.currentSprite))
        if not tile_map.isWalkable(self.x + dx + spriteWidth, self.y):
            dx = min(dx, 0)
            ret = False

        # Проверка превышения нижней границы с учётом высоты спрайта
        spriteHeight = abs(const.getHeightSprite(self.currentSprite))
        if not tile_map.isWalkable(self.x, self.y + dy + spriteHeight):
            dy = min(dy, 0)
            ret = False

        new_x, new_y = self.__x + dx, self.__y + dy
        if tile_map.isWalkable(new_x, new_y + spriteHeight):
            self.__x, self.__y = new_x, new_y

        else:
            ret = False

        return ret

    def draw(self, scene: Scene, delta_time: float = const.DELTA_TIME):
        scene.drawSprite(self.currentSprite, int(self.x), int(self.y))

    def setSprite(self, sprite):
        self.currentSprite = sprite

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y
