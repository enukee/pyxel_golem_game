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
        self._isInteractBoxAvailable = False

        self._playerMovementHandler = []    # Список обработчиков движения игрока
        self._playerAttackHandler = []    # Список обработчиков движения игрок
        self._inventoryUpdateHandler = []          # Обработчики события при обновлении инвентаря
        self._interactionUpdateHandler = []               # Обработчик при событии взаимодействия с некоторым объектом
        self._interactionOpenHandler = []

    @property
    def frameCount(self):
        return self._controller.getFrameCount()

    def update(self):
        """
        Обработка событий.
        """
        self.__updateInventory()

        self.__updateInteractBox()

        if not self.gameInPause():
            self.__updateGameEvents()

    def gameInPause(self):
        """
        При открытии любого игрового окна игра ставится на паузу.
        Если открыто какое-либо окно возвращает True.
        """
        return self._isInventoryAvailable or self._isInteractBoxAvailable

    def __updateInventory(self):
        # Если игра на паузе и инвентарь не доступен(обрабатывается другое окно),
        # то инвентарь не обновляется
        if self.gameInPause() and not self._isInventoryAvailable:
            return

        if self._controller.isInventoryButtonPressed():
            self._isInventoryAvailable = not self._isInventoryAvailable
            self._drawer.mouseVisible(self._isInventoryAvailable)

        if self._isInventoryAvailable:
            for handler in self._inventoryUpdateHandler:
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

    def __updateInteractBox(self):
        # Если игра на паузе и окно взаимодействия с сундуком не доступен(обрабатывается другое окно),
        # то окно взаимодействия с сундуком не обновляется
        if self.gameInPause() and not self._isInteractBoxAvailable:
            return

        if self._controller.isInteractButtonPressed():
            self._isInteractBoxAvailable = not self._isInteractBoxAvailable
            self._drawer.mouseVisible(self._isInteractBoxAvailable)

            # Если взаимодействовать не с чем не открываем окно
            for handler in self._interactionOpenHandler:
                if not handler():
                    self._isInteractBoxAvailable = False

        # Обработка события взаимодействия с сундуком
        if self._isInteractBoxAvailable:
            for handler in self._interactionUpdateHandler:
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

    def addUpdateInventoryHandler(self, handler):
        self._inventoryUpdateHandler.append(handler)

    def addUpdateInteractHandler(self, handler):
        self._interactionUpdateHandler.append(handler)

    def addOpenInteractHandler(self, handler):
        self._interactionOpenHandler.append(handler)

    def isInventoryAvailable(self):
        return self._isInventoryAvailable

    def isInteractBoxAvailable(self):
        return self._isInteractBoxAvailable
