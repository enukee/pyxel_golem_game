from draw import Drawer
from game_windows.Screen import Screen, BlockBox, TextBox, Block


class ScreenWithBlockBox(Screen):
    def __init__(self, drawer: Drawer):
        """
        Окно содержащее блоки с предметами.
        !!! Может содержать только 2 контейнера с блоками(предметов).
        Т.е. одновременно можно перемещать блоки только между 2 контейнерами.
        """
        super().__init__(drawer)

        self.__statsArtTextBox = None

        self.__firstBox = None
        self.__secondBox = None

        self.__firstArtList = dict()
        self.__secondArtList = dict()

    def setFirstBox(self, box: BlockBox, artList: dict):
        self.__firstBox = box
        self.__firstArtList = artList

    def setSecondBox(self, box: BlockBox, artList: dict):
        self.__secondBox = box
        self.__secondArtList = artList

    def setStatsBox(self, textBox: TextBox):
        self.__statsArtTextBox = textBox

    def updateHandlers(self):
        if self.__firstBox is not None and self.__secondBox is not None:
            self.__addHandlerShowStats(self.__firstBox)
            self.__addHandlerShowStats(self.__secondBox)

    def updateArtSelect(self):
        pass

    def updateArtPosition(self):
        pass

    def __addHandlerShowStats(self, box):
        def showStats(block):
            if self.__statsArtTextBox is None:
                return

            num = box.getBlockNum(block.title)
            if -1 != num:
                if num in self.__firstArtList:
                    self.__statsArtTextBox.text = self.__firstArtList[num].description
                elif num in self.__secondArtList:
                    self.__statsArtTextBox.text = self.__secondArtList[num].description

            self.updateArtSelect()

        def getArtifact(block: Block):
            """
            Вынимает артефакт из списка и возвращает:
            artifact - сам артефакт,
            artList - словарь в котором он лежал,
            num - его ключ в словаре,
            x, y - позиция x и y экрана в котором был расположен артефакт.
            """
            num = self.__firstBox.getBlockNum(block.title)
            if num == -1:
                num = self.__secondBox.getBlockNum(block.title)

                if num in self.__secondArtList:
                    artifact = self.__secondArtList.pop(num)
                else:
                    artifact = None

                artList = self.__secondArtList
                x, y = self.__secondBox.getPos(num)

            else:
                if num in self.__firstArtList:
                    artifact = self.__firstArtList.pop(num)
                else:
                    artifact = None

                artList = self.__firstArtList
                x, y = self.__firstBox.getPos(num)

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

            self.updateArtPosition()

        super().setHandlerLeft(box.title, showStats)
        super().setHandlerRight(box.title, swapArtifact)
