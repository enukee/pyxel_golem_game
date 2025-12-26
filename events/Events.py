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

    def update(self):
        """
        Обработка событий.
        """
        # Обработка события движения игрока
        if not self._isInventoryAvailable:
            # Получаем направление движения игрока от контроллера
            dirX, dirY = self._controller.getDirection()
            for handler in self._playerMovementHandler:
                handler(dirX, dirY)

    def addPlayerMovementHandler(self, handler):
        """
        Метод для добавления обработчика движения игрока.
        :param handler: Обработчика движения игрока(принимает два аргумента: направление по оси X и по оси Y).
        """
        self._playerMovementHandler.append(handler)
