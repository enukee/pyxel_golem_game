import const
from events import Events, PyxelController
from map import MatrixMap
from units import Player, Stats, UnitsManager
from events import Controller
from draw import Scene, Drawer
from game_windows import Inventory


class Game:
    def __init__(self, drawer: Drawer, control: Controller):
        """
        Объект игры.
        :param drawer: Инструмент отображения.
        :param control: Инструмент получения событий.
        """
        self.tileMap = MatrixMap()
        playerStats = Stats(100, 12, 10, 50, 5)
        self.player = Player(30, 200, playerStats)

        # Окно инвентаря и характеристик
        self.inventory = Inventory(playerStats)

        chanceEnemy = {
            "mimic":    0.65,
            "egg_head": 0.35
        }
        self.units = UnitsManager(self.player, self.tileMap, chanceEnemy, 50)

        self.scene = Scene(drawer, self.player.x - const.WINDOW_WIDTH // 2,
                           self.player.y - const.WINDOW_HEIGHT // 2)
        self.events = Events(control, drawer)

        def movement(dirX, dirY):
            """
            Обработчик события движения игрока.
            :param dirX: Направление движения по оси X.
            :param dirY: Направление движения по оси Y.
            """
            self.player.setDir(dirX, dirY)

        self.events.addPlayerMovementHandler(movement)

        def attack(frameCount):
            """
            Обработчик события атаки игрока.
            """
            self.player.attack(frameCount)

        self.events.addPlayerAttackHandler(attack)

    def update(self) -> bool:
        self.events.update()

        # Обновление инвентаря
        if self.events.isInventoryAvailable():
            self.events.updateWindow(self.inventory)
            # Пока открыт инвентарь игра не может закончиться
            # так как игрок не может умереть
            return False

        # Юниты обновляются если не открыты какие-либо окна,
        # При открытии окон игра приостанавливается
        return self.units.update(self.events, self.tileMap)

    def draw(self):
        # Отрисовка инвентаря
        if self.events.isInventoryAvailable():
            self.inventory.draw()
            return

        self.tileMap.draw(self.scene, self.player.x, self.player.y)
        self.units.draw(self.scene)
