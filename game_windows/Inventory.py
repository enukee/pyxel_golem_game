from draw import Drawer
from game_windows.Screen import Screen, TextBox, BlockBox, Block
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
        self.artifactTxBox = TextBox(30, 160,
                                     190, 50,
                                     "", "art_stats")
        super().addTxBox(self.artifactTxBox)

        self.__createInventory()
        self.__createActiveInventory()

        self.__artifacts = dict()
        self.__activeArtifacts = dict()

    def __createInventory(self):
        self.inventoryBox = BlockBox(100, 50,
                                     4, 4,
                                     "inventory_box")
        self.inventoryBox.fill()
        super().addBlBox(self.inventoryBox)
        self.__addHandlerShowStats(self.inventoryBox)

    def __createActiveInventory(self):
        self.activeInventoryBox = BlockBox(80, 10,
                                           7, 1,
                                           "active_inventory_box")
        self.activeInventoryBox.fill()
        super().addBlBox(self.activeInventoryBox)
        self.__addHandlerShowStats(self.activeInventoryBox)

    def __addHandlerShowStats(self, box):
        def showStats(block):
            num = box.getBlockNum(block.title)
            if -1 != num:
                if num in self.__artifacts:
                    self.artifactTxBox.text = self.__artifacts[num].description
                elif num in self.__activeArtifacts:
                    self.artifactTxBox.text = self.__activeArtifacts[num].description

        def getArtifact(block: Block):
            """
            Вынимает артефакт из списка и возвращает:
            artifact - сам артефакт,
            artList - словарь в котором он лежал,
            num - его ключ в словаре,
            x, y - позиция x и y экрана в котором был расположен артефакт.
            """
            num = self.inventoryBox.getBlockNum(block.title)
            if num == -1:
                num = self.activeInventoryBox.getBlockNum(block.title)

                if num in self.__activeArtifacts:
                    artifact = self.__activeArtifacts.pop(num)
                else:
                    artifact = None

                artList = self.__activeArtifacts
                x, y = self.activeInventoryBox.getPos(num)

            else:
                if num in self.__artifacts:
                    artifact = self.__artifacts.pop(num)
                else:
                    artifact = None

                artList = self.__artifacts
                x, y = self.inventoryBox.getPos(num)

            return artifact, artList, num, x, y

        def swapArtifact(block):
            if Block.selectBlock is None:
                return

            artifact1, artList1, num1, x1, y1 = getArtifact(Block.selectBlock)
            artifact2, artList2, num2, x2, y2 = getArtifact(block)

            if artifact1 is not None:
                artifact1.x, artifact1.y = x2, y2
                artList2[num2] = artifact1

            if artifact2 is not None:
                artifact2.x, artifact2.y = x1, y1
                artList1[num1] = artifact2

            self.statsUpdate()

        super().setHandlerLeft(box.title, showStats)
        super().setHandlerRight(box.title, swapArtifact)

    def statsUpdate(self):
        self.stats.reset()
        for _, art in self.__activeArtifacts.items():
            art.applyIncrease(self.stats)

    def update(self, control: Controller):
        super().update(control)

    def draw(self):
        self.statsTxBox.text = self.stats.getAllStats()
        super().draw()
        for _, art in self.__artifacts.items():
            art.draw(self._scene)

        for _, art in self.__activeArtifacts.items():
            art.draw(self._scene)

    def pushArtifact(self, artifact):
        for i in range(self.inventoryBox.maxCount):
            if i not in self.__artifacts:
                artifact.x, artifact.y = self.inventoryBox.getPos(i)
                self.__artifacts[i] = artifact
                return
