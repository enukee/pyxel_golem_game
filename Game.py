import const
from events import Events, PyxelController
from map import MatrixMap
from units import Player, Stats, UnitsManager
from events import Controller
from draw import Scene, Drawer


class Game:
    def __init__(self, drawer: Drawer, control: Controller):
        """
        Объект игры.
        :param drawer: Инструмент отображения.
        :param control: Инструмент получения событий.
        """
        self.tileMap = MatrixMap()
        self.player = Player(30, 200, Stats(100, 12, 10, 50, 5))

        chanceEnemy = {
            "mimic":    0.65,
            "egg_head": 0.35
        }
        self.units = UnitsManager(self.player, self.tileMap, chanceEnemy)

        self.scene = Scene(drawer, self.player.x - const.WINDOW_WIDTH // 2,
                           self.player.y - const.WINDOW_HEIGHT // 2)
        self.events = Events(control)

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
        return self.units.update(self.events, self.tileMap)

    def draw(self):
        self.tileMap.draw(self.scene, self.player.x, self.player.y)
        self.units.draw(self.scene)
