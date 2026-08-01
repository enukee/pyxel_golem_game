from draw import Drawer
from events import Controller


class Events:
    def __init__(self, controller: Controller, drawer: Drawer):
        """
        Конструктор класса Events.
        :param controller: Объект отвечающий за управление игрой
        """
        self._controller = controller
        self._drawer = drawer
        self._isInventoryAvailable = False  # Флаг, указывающий, доступен ли инвентарь игрока

        self._playerMovementHandler = []    # Список обработчиков движения игрока
        self._playerAttackHandler = []    # Список обработчиков движения игрок
        self._inventoryIsOpenHandler = []          # Обработчики события при обновлении инвентаря
        self._interactionHandler = []               # Обработчик при событии взаимодействия с некоторым объектом

    @property
    def frameCount(self):
        return self._controller.getFrameCount()

    def update(self):
        """
        Обработка событий.
        """
        self.__updateInventory()

        if not self.gameInPause():
            self.__updateGameEvents()

    def gameInPause(self):
        """
        При открытии любого игрового окна игра ставится на паузу.
        Если открыто какое-либо окно возвращает True.
        """
        return self._isInventoryAvailable

    def __updateInventory(self):
        if self._controller.isInventoryButtonPressed():
            self._isInventoryAvailable = not self._isInventoryAvailable
            self._drawer.mouseVisible(self._isInventoryAvailable)

        if self._isInventoryAvailable:
            for handler in self._inventoryIsOpenHandler:
                handler()

    def __updateGameEvents(self):
        # Получаем направление движения игрока от контроллера
        dirX, dirY = self._controller.getDirection()

        # Обработка события движения игрока
        for handler in self._playerMovementHandler:
            handler(dirX, dirY)

        # Обработка события атаки
        if self._controller.isShootButtonPressed():
            for handler in self._playerAttackHandler:
                handler(self.frameCount)

        # Обработка события взаимодействия с объектом
        if self._controller.isInteractButtonPressed():
            for handler in self._interactionHandler:
                handler()

    def addPlayerMovementHandler(self, handler):
        """
        Метод для добавления обработчика движения игрока.
        :param handler: Обработчика движения игрока(принимает два аргумента: направление по оси X и по оси Y).
        """
        self._playerMovementHandler.append(handler)

    def addPlayerAttackHandler(self, handler):
        """
        Метод для добавления обработчика атаки игрока.
        :param handler: Обработчик атаки игрока(принимает два аргумента: направление по оси X и по оси Y).
        """
        self._playerAttackHandler.append(handler)

    def addOpenInventoryHandler(self, handler):
        self._inventoryIsOpenHandler.append(handler)

    def addInteractHandler(self, handler):
        self._interactionHandler.append(handler)

    def isInventoryAvailable(self):
        return self._isInventoryAvailable
