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

        retValue, dx, dy = self.__tryMoveBySpriteSize(dx, dy, tile_map)

        new_x, new_y, width, height = self.__getStandPosWithOffset(dx, dy)
        newStandY = new_y + height - const.CONST_WIDTH_ALL_UNIT
        if tile_map.isWalkable(new_x, newStandY):
            if self.unitManager is None:
                self.__setOffset(dx, dy)
            else:
                unit = self.unitManager.isWalkable(new_x,
                                                   newStandY,
                                                   self)
                if unit is None:
                    self.__setOffset(dx, dy)
                else:
                    unit.setPush(dx, dy)
                    self.pushUnit(unit)
                    unit.pushUnit(self)

        else:
            retValue = False

        return retValue

    def __tryMoveBySpriteSize(self, dx: float, dy: float, tile_map: MatrixMap):
        new_x, new_y, width, height = self.__getStandPosWithOffset(dx, dy)
        retValue = True

        # Проверка превышения правой границы с учётом ширины спрайта
        if not tile_map.isWalkable(new_x + width, new_y):
            dx = min(dx, 0)
            retValue = False

        # Проверка превышения нижней границы с учётом высоты спрайта
        if not tile_map.isWalkable(new_x, new_y + height):
            dy = min(dy, 0)
            retValue = False

        return retValue, dx, dy

    def __getStandPosWithOffset(self, dx, dy):
        new_x, new_y, width, height = self.standPos
        return new_x + dx, new_y + dy, width, height

    def __setOffset(self, dx, dy):
        self.__x, self.__y = self.__x + dx, self.__y + dy

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
        :return: Координата по оси X верхнего левого угла спрайта
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
        (координата нижнего правого угла относительно спрайта)
        """
        return self.__y + const.getHeightSprite(self.currentSprite)

    @property
    def rightX(self):
        """
        :return: Координата по X, являющаяся правой границей спрайта.
        (координата нижнего правого угла относительно спрайта)
        """
        return self.__x + const.getWidthSprite(self.currentSprite)

    @property
    def standPos(self):
        """
        Возвращает прямоугольник в котором "стоит" объект
        :return: Координата x левого верхнего угла, координата y левого верхнего угла, ширина, высота
        """
        return (self.__x, self.standY - const.CONST_WIDTH_ALL_UNIT,
                const.getWidthSprite(self.currentSprite), const.CONST_WIDTH_ALL_UNIT)
