from events import Controller


class Events:
    def __init__(self, controller: Controller):
        """
        Конструктор класса Events.
        :param controller: Объект отвечающий за управление игрой
        """
        self._controller = controller
        self._isInventoryAvailable = False  # Флаг, указывающий, доступен ли инвентарь игрока
        self._playerMovementHandler = []    # Список обработчиков движения игрока
        self._playerAttackHandler = []    # Список обработчиков движения игрока

    @property
    def frameCount(self):
        return self._controller.getFrameCount()

    def update(self):
        """
        Обработка событий.
        """
        if not self._isInventoryAvailable:
            # Получаем направление движения игрока от контроллера
            dirX, dirY = self._controller.getDirection()

            # Обработка события движения игрока
            for handler in self._playerMovementHandler:
                handler(dirX, dirY)

            # Обработка события атаки
            if self._controller.isShootButtonPressed():
                for handler in self._playerAttackHandler:
                    handler(self.frameCount)

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
