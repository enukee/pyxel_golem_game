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

        self.unitManager = None

        # Смещение юнита при столкновении с другим юнитом
        self.pushOffsetX = 0
        self.pushOffsetY = 0

    def tryMove(self, dx: float, dy: float, tile_map: MatrixMap) -> bool:
        """
        Передвижение с проверкой.
        :param dx: Сдвиг по оси X.
        :param dy: Сдвиг по оси Y.
        :param tile_map: Карта тайлов.
        :return: Флаг успешного передвижения.
        """
        dx += self.pushOffsetX
        dy += self.pushOffsetY

        self.pushOffsetX, self.pushOffsetY = 0, 0
        ret = True

        # Проверка превышения правой границы с учётом ширины спрайта
        spriteWidth = const.getWidthSprite(self.currentSprite)
        if not tile_map.isWalkable(self.x + dx + spriteWidth, self.y):
            dx = min(dx, 0)
            ret = False

        # Проверка превышения нижней границы с учётом высоты спрайта
        spriteHeight = const.getHeightSprite(self.currentSprite)
        if not tile_map.isWalkable(self.x, self.y + dy + spriteHeight):
            dy = min(dy, 0)
            ret = False

        new_x, new_y = self.__x + dx, self.__y + dy
        newStandY = new_y + spriteHeight
        if tile_map.isWalkable(new_x, newStandY):
            if self.unitManager is None:
                self.__x, self.__y = new_x, new_y
            else:
                unit = self.unitManager.isWalkable(new_x,
                                                   newStandY - const.CONST_WIDTH_ALL_UNIT,
                                                   self)
                if unit is None:
                    self.__x, self.__y = new_x, new_y
                else:
                    unit.setPush(dx, dy)
                    self.pushUnit(unit)
                    unit.pushUnit(self)

        else:
            ret = False

        return ret

    def setPush(self, x, y):
        """
        Смещение объекта из вне(в отличии, от tryMove не запускает обновление координат,
        а лишь устанавливает смещение используемое при следующем передвижении).
        :param x: Смещение по X
        :param y: Смещение по Y
        """
        self.pushOffsetX, self.pushOffsetY = x, y

    def pushUnit(self, unit):
        """
        В этом методе можно задать обработку столкновения с юнитом
        :param unit: Юнит с котором столкнулся self
        """
        pass

    def draw(self, scene: Scene, delta_time: float = const.DELTA_TIME):
        scene.drawSprite(self.currentSprite, int(self.x), int(self.y))

    def setSprite(self, sprite):
        self.currentSprite = sprite

    def setUnitManager(self, unitManager):
        self.unitManager = unitManager

    @property
    def x(self):
        """
        :return: Координата по оси Y верхнего левого угла спрайта
        """
        return self.__x

    @property
    def y(self):
        """
        :return: Координата по оси Y верхнего левого угла спрайта
        """
        return self.__y

    @property
    def standY(self):
        """
        :return: Координата по Y соответсвующая позиции в которой "стоит" объект
        (координата нижнего левого угла относительно спрайта)
        """
        return self.__y + const.getHeightSprite(self.currentSprite)

    @property
    def standPos(self):
        """
        Возвращает прямоугольник в котором "стоит" объект
        :return: Координата x левого верхнего угла, координата y левого верхнего угла, ширина, высота
        """
        return (self.__x, self.standY - const.CONST_WIDTH_ALL_UNIT,
                const.getWidthSprite(self.currentSprite), const.CONST_WIDTH_ALL_UNIT)
