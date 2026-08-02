from draw import Drawer
from game_windows.Screen import TextBox, BlockBox
from game_windows.ScreenWithBlockBox import ScreenWithBlockBox
from objects import Stats


class Inventory(ScreenWithBlockBox):
    def __init__(self, drawer: Drawer, playerStats: Stats):
        """
        Окно инвентаря игрока и характеристик.
        """
        super().__init__(drawer)

        # Характеристики игрока
        self.stats = playerStats

        # Добавление окна отображения характеристик игрока.
        self.statsTxBox = TextBox(235, 50,
                                  80, 100,
                                  self.stats.getAllStats(), "stats")
        super().addTxBox(self.statsTxBox)

        # Добавление окна отображения характеристик предмета.
        self.artifactTxBox = TextBox(30, 160,
                                     190, 50,
                                     "", "art_stats")
        super().addTxBox(self.artifactTxBox)
        super().setStatsBox(self.artifactTxBox)

        self.__artifacts = dict()
        self.__activeArtifacts = dict()

        self.__createInventory()
        self.__createActiveInventory()
        super().updateHandlers()

    def __createInventory(self):
        self.inventoryBox = BlockBox(100, 50,
                                     4, 4,
                                     "inventory_box")
        self.inventoryBox.fill()
        super().addBlBox(self.inventoryBox)
        super().setFirstBox(self.inventoryBox, self.__artifacts)

    def __createActiveInventory(self):
        self.activeInventoryBox = BlockBox(80, 10,
                                           7, 1,
                                           "active_inventory_box")
        self.activeInventoryBox.fill()
        super().addBlBox(self.activeInventoryBox)
        super().setSecondBox(self.activeInventoryBox, self.__activeArtifacts)

    def updateArtPosition(self):
        self.stats.reset()
        for _, art in self.__activeArtifacts.items():
            art.applyIncrease(self.stats)

    def draw(self):
        self.statsTxBox.text = self.stats.getAllStats()
        super().draw()

    def pushArtifact(self, artifact):
        for i in range(self.inventoryBox.maxCount):
            if i not in self.__artifacts:
                artifact.x, artifact.y = self.inventoryBox.getPos(i)
                self.__artifacts[i] = artifact
                return

    @property
    def artifacts(self):
        return self.__artifacts
