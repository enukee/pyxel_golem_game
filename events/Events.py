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
        self._openInventory = []
        self._closeInventory = []

    @property
    def frameCount(self):
        return self._controller.getFrameCount()

    def update(self):
        """
        Обработка событий.
        """
        if self._isInventoryAvailable:
            # Закрытие инвентаря
            if self._controller.isInventoryButtonPressed():
                for handler in self._closeInventory:
                    handler()

                self._drawer.mouseVisible(False)
                self._isInventoryAvailable = False

        else:
            # Получаем направление движения игрока от контроллера
            dirX, dirY = self._controller.getDirection()

            # Обработка события движения игрока
            for handler in self._playerMovementHandler:
                handler(dirX, dirY)

            # Обработка события атаки
            if self._controller.isShootButtonPressed():
                for handler in self._playerAttackHandler:
                    handler(self.frameCount)

            # Открытие инвентаря
            if self._controller.isInventoryButtonPressed():
                for handler in self._openInventory:
                    handler()

                self._drawer.mouseVisible(True)
                self._isInventoryAvailable = True

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
        """
        Метод для добавления обработчика открытия инвентаря.
        :param handler: Обработчик.
        """
        self._openInventory.append(handler)

    def addCloseInventoryHandler(self, handler):
        """
        Метод для добавления обработчика закрытия инвентаря.
        :param handler: Обработчик.
        """
        self._closeInventory.append(handler)

    def isInventoryAvailable(self):
        return self._isInventoryAvailable

    def updateWindow(self, window):
        window.update(self._controller)
