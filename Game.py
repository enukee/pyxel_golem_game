import const
from events import Events
from map import MatrixMap
from units import Player
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
        self.player = Player(30, 200)

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
            self.player.update(self.tileMap)

        self.events.addPlayerMovementHandler(movement)

    def update(self):
        self.events.update()

    def draw(self):
        self.tileMap.draw(self.scene, self.player.x, self.player.y)
        self.player.draw(self.scene)
