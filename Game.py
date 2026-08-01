import const
from events import Events, PyxelController
from map import MatrixMap
from objects import SilverFork
from objects.Artifact import SilverRing, MagicAmanita, FlowerVine, MedicinalClover, ScarletBug
from units import Player, Stats, UnitsContainer, InteractiveObject
from events import Controller
from draw import Scene, Drawer
from game_windows import Inventory
from units.InteractiveObject import BoxCreator


class Game:
    def __init__(self, drawer: Drawer, control: Controller):
        """
        Объект игры.
        :param drawer: Инструмент отображения.
        :param control: Инструмент получения событий.
        """
        self.tileMap = MatrixMap(const.TILE_COUNT)
        playerStats = Stats(100, 12, 10, 50, 5)
        self.player = Player(30, 200, playerStats)

        # Окно инвентаря и характеристик
        self.inventory = Inventory(drawer, playerStats)
        self.inventory.pushArtifact(SilverFork())
        self.inventory.pushArtifact(FlowerVine())
        self.inventory.pushArtifact(MedicinalClover())
        self.inventory.pushArtifact(ScarletBug())
        self.inventory.pushArtifact(SilverRing())
        self.inventory.pushArtifact(MagicAmanita())

        def boxOpenHandler():
            pass

        boxCreator = BoxCreator(boxOpenHandler)

        self.units = UnitsContainer(self.player, self.tileMap, 50)

        self.scene = Scene(drawer, self.player.x - const.WINDOW_WIDTH // 2,
                           self.player.y - const.WINDOW_HEIGHT // 2)
        self.events = Events(control, drawer)
        self.__initHandlers(control)

    def __initHandlers(self, control: Controller):
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

        def updateInventory():
            self.inventory.update(control)

        self.events.addOpenInventoryHandler(updateInventory)

        def interactWithObj():
            objects = self.units.findUnitsInRadius(self.player.x, self.player.y,
                                                   const.INTERACT_RADIUS_WITH_OBJECT)
            for obj in objects:
                if isinstance(obj, InteractiveObject):
                    obj.update()

        self.events.addInteractHandler(interactWithObj)

    def update(self) -> bool:
        self.events.update()

        # Обновление инвентаря
        if self.events.isInventoryAvailable():
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
