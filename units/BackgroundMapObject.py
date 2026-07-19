import random

import const
from events import Events
from map import MatrixMap
from units import MovableObjects


class BackgroundMapObject(MovableObjects):
    def __init__(self, x: float, y: float):
        """
        Объект имеющий характеристики и способный передвигаться в пространстве.
        :param x: Координата x объекта.
        :param y: Координата y объекта.
        """
        super().__init__(x, y)

        backObj = [key for key in const.SPRITE_POS if key.startswith("back_obj")]

        # Напольные объекты
        backObjOnFloor = []

        selectSprite = random.choice(backObj + backObjOnFloor)
        super().setSprite(selectSprite)

        self.__standY = None
        if selectSprite in backObjOnFloor:
            self.__standY = -1

    def update(self, events: Events, tileMap: MatrixMap,  delta_time: float = const.DELTA_TIME):
        pass

    @property
    def standY(self):
        # Некоторые объекты не должны сортироваться вместе со всеми юнитами
        # Если объект расположен на полу, то находится на заднем фоне
        # И в сравнении с другими юнитами должен быть расположен дальше от камеры
        if self.__standY is None:
            return super().standY

        return self.__standY
