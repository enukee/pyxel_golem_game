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

        backObj = ['back_obj_grass', 'back_obj_flower', 'back_obj_stone',
                   'back_obj_grass_r', 'back_obj_flower_r', 'back_obj_stone_r',
                   'back_obj_bush', 'back_obj_bush_r']

        backObjOnFloor = ['back_obj_stone_floor_1', 'back_obj_stone_floor_2',
                          'back_obj_stone_floor_3', 'back_obj_stone_floor_4',
                          'back_obj_stone_floor_2_1', 'back_obj_stone_floor_2_2',
                          'back_obj_stone_floor_2_3', 'back_obj_stone_floor_2_4']

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
