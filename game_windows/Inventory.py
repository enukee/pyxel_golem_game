import const
from draw import Screen, Drawer, Button, TextBox
from events import Controller


class Inventory(Screen):
    def __init__(self):
        """
        Окно инвентаря игрока и характеристик.
        """
        super().__init__()

        # Добавление окна отображения характеристик.
        super().addTxBox(TextBox(15, 50,
                                 40, 100,
                                 "play", "stats"))

    def update(self, control: Controller):
        super().update(control)

    def draw(self, drawer: Drawer):
        super().draw(drawer)
