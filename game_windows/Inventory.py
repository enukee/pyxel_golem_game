import const
from draw import Screen, Drawer, Button, TextBox, BlockBox
from events import Controller
from units import Stats


class Inventory(Screen):
    def __init__(self, drawer: Drawer, playerStats: Stats):
        """
        Окно инвентаря игрока и характеристик.
        """
        super().__init__(drawer)

        self.stats = playerStats

        self.statsTxBox = TextBox(235, 50,
                                  80, 100,
                                  self.stats.getAllStats(), "stats")

        # Добавление окна отображения характеристик.
        super().addTxBox(self.statsTxBox)

        self.inventoryBox = BlockBox(80, 50,
                                     4, 4,
                                     "inventory_box")

        self.inventoryBox.pushBlock(0, 0, "art1")
        self.inventoryBox.pushBlock(1, 0, "art2")
        self.inventoryBox.pushBlock(3, 0, "art3 ")
        self.inventoryBox.pushBlock(3, 3, "art3 ")

        # Добавление контейнера с предметами.
        super().addBlBox(self.inventoryBox)

    def update(self, control: Controller):
        super().update(control)

    def draw(self):
        self.statsTxBox.text = self.stats.getAllStats()
        super().draw()
