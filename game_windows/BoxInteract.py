from draw import Drawer
from game_windows.Screen import TextBox, BlockBox
from game_windows.ScreenWithBlockBox import ScreenWithBlockBox


class BoxInteract(ScreenWithBlockBox):
    def __init__(self, drawer: Drawer, atrInventory: dict):
        """
        Окно для взаимодействия игрока с сундуком,
        позволяет переложить предметы в инвентарь.
        :param atrInventory артефакты сложенные в инвентарь
        """
        super().__init__(drawer)

        # Отображения характеристик предмета
        self.artifactTxBox = TextBox(30, 160,
                                     190, 50,
                                     "", "art_stats")
        super().addTxBox(self.artifactTxBox)
        super().setStatsBox(self.artifactTxBox)

        # Контейнер с артефактами из инвентаря
        self.__artInventory = atrInventory
        self.inventoryBox = BlockBox(50, 50,
                                     4, 4,
                                     "inventory_box")
        self.inventoryBox.fill()
        super().addBlBox(self.inventoryBox)
        self.setFirstBox(self.inventoryBox, self.__artInventory)

        # Контейнер с артефактами из сундука
        self.__artBox = dict()
        self.currentBox = BlockBox(150, 50,
                                   4, 4,
                                   "current_box")
        self.currentBox.fill()
        super().addBlBox(self.currentBox)
        self.setSecondBox(self.currentBox, self.__artBox)

        super().updateHandlers()

    def setArtifactsInBox(self, artifacts):
        self.__artBox = artifacts
        self.setSecondBox(self.currentBox, self.__artBox)

