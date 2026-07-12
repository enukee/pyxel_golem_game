import const
from draw import Screen, Drawer, Button, TextBox
from events import Controller
from units import Stats


class Inventory(Screen):
    def __init__(self, playerStats: Stats):
        """
        Окно инвентаря игрока и характеристик.
        """
        super().__init__()

        self.stats = playerStats

        self.statsTxBox = TextBox(15, 50,
                                  80, 100,
                                  self.stats.getAllStats(), "stats")

        # Добавление окна отображения характеристик.
        super().addTxBox(self.statsTxBox)

    def update(self, control: Controller):
        super().update(control)

    def draw(self, drawer: Drawer):
        self.statsTxBox.text = self.stats.getAllStats()
        super().draw(drawer)
