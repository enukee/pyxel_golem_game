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

        # Добавление окна отображения характеристик игрока.
        self.statsTxBox = TextBox(235, 50,
                                  80, 100,
                                  self.stats.getAllStats(), "stats")
        super().addTxBox(self.statsTxBox)

        # Добавление окна отображения характеристик предмета.
        self.artifactTxBox = TextBox(10, 50,
                                     80, 50,
                                     "", "art_stats")
        super().addTxBox(self.artifactTxBox)

        self.__createInventory()
        self.__createActiveInventory()

        self.__artifacts = dict()

    def __createInventory(self):
        self.inventoryBox = BlockBox(80, 50,
                                     4, 4,
                                     "inventory_box")
        self.inventoryBox.fill()
        super().addBlBox(self.inventoryBox)
        self.__addHandlerShowStats(self.inventoryBox)

    def __createActiveInventory(self):
        self.activeInventoryBox = BlockBox(10, 10,
                                           7, 1,
                                           "active_inventory_box")
        self.activeInventoryBox.fill()
        super().addBlBox(self.activeInventoryBox)
        self.__addHandlerShowStats(self.activeInventoryBox)

    def __addHandlerShowStats(self, box):
        def showStats(block):
            num = box.getBlockNum(block.title)
            if -1 != num and num in self.__artifacts:
                self.artifactTxBox.text = self.__artifacts[num].description

        super().setHandler(box.title, showStats)

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
