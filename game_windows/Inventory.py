import const
from draw import Screen, Drawer, TextBox, BlockBox, Scene
from events import Controller
from units import Stats


class Inventory(Screen):
    def __init__(self, drawer: Drawer, playerStats: Stats):
        """
        Окно инвентаря игрока и характеристик.
        """
        super().__init__(drawer)

        # Характеристики игрока
        self.stats = playerStats

        self.statsTxBox = TextBox(235, 50,
                                  80, 100,
                                  self.stats.getAllStats(), "stats")

        # Добавление окна отображения характеристик.
        super().addTxBox(self.statsTxBox)

        self.inventoryBox = BlockBox(80, 50,
                                     4, 4,
                                     "inventory_box")

        self.inventoryBox.fill()

        # Добавление контейнера с предметами.
        super().addBlBox(self.inventoryBox)

        self.__artifacts = dict()

    def update(self, control: Controller):
        super().update(control)

    def draw(self):
        self.statsTxBox.text = self.stats.getAllStats()
        super().draw()
        for _, art in self.__artifacts.items():
            art.draw(self._scene)

    def pushArtifact(self, artifact):
        for i in range(self.inventoryBox.maxCount):
            if i not in self.__artifacts:
                artifact.x, artifact.y = self.inventoryBox.getPos(i)
                self.__artifacts[i] = artifact
                return
