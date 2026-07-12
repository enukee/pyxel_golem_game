import const
from draw import Screen, Drawer, Button
from events import Controller


class Menu(Screen):
    def __init__(self):
        """
        Главное меню игры.
        """
        super().__init__()

        # Добавление кнопки начала игры.
        super().addBtn(Button(const.BUTTON_MENU_POS_X, int(const.WINDOW_HEIGHT * 2 / 3),
                              const.BUTTON_MENU_WIDTH, const.BUTTON_MENU_HEIGHT, "play"))

        # Добавление кнопки выхода из игры.
        super().addBtn(Button(const.BUTTON_MENU_POS_X, int(const.WINDOW_HEIGHT * 2 / 3 + const.BUTTON_MENU_HEIGHT * 1.5),
                              const.BUTTON_MENU_WIDTH, const.BUTTON_MENU_HEIGHT, "exit"))

    def update(self, control: Controller):
        super().update(control)

    def draw(self, drawer: Drawer):
        super().draw(drawer)
