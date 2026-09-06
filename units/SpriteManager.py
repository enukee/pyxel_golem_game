import const


class SpriteInfo:
    def __init__(self, name, time, shiftX, shiftY):
        # Название
        self.spriteName = name
        # Время показа спрайта
        self.time = time
        # Сдвиг спрайта при отрисовке
        self.shiftX = shiftX
        self.shiftY = shiftY


class SpriteManager:
    class SpritesTuple:
        def __init__(self, isApplyDir=False, isSingleExecute=False):
            """
            Набор спрайтов для одного движения действия.
            """
            self.__sprites = []

            # Добавление модификатора направления (если имеются разные спрайты
            # в зависимости от направления движения)
            self.__isApplyDir = isApplyDir
            # Выполняется единожды (после показа каждого спрайта действия завершается)
            self.__isSingleExecute = isSingleExecute

        def addSprite(self, name, time, shift):
            """
            Добавление спрайта в анимацию.
            @param name: Модификатор спрайта(добавляется к базовому имени спрайта).
            @param time: Время показа данного спрайта.
            @param shift: Список из координат смещения спрайта при показе.
            """
            self.__sprites.append(
                SpriteInfo(name, time, shift[0], shift[1])
            )

        def getSpriteInfo(self, i):
            if self.count < i:
                raise "Набор спрайтов содержит только " + str(self.count) + " спрайтов"

            return self.__sprites[i]

        @property
        def count(self):
            return len(self.__sprites)

        @property
        def isApplyDir(self):
            return self.__isApplyDir

        @property
        def isSingleExecute(self):
            return self.__isSingleExecute

    def __init__(self, baseSpriteName: str):
        """
        Менеджер спрайтов.
        :param baseSpriteName: Базовое имя спрайта.
        """
        self.__step = 0
        # Базовое имя спрайта(имя спрайта должно начинаться с базового имени)
        self.__baseName = baseSpriteName

        # Имя текущего действия
        self.__currentAction = const.ACTION_NONE
        # Имя базового действия на которое будет переключено
        # после выполнения действия выполняемого единожды
        self.__baseAction = const.ACTION_NONE
        # Набор спрайтов для каждого действия
        self.__sprites = {}
        # Направление движения спрайта
        self.__direction = "_down"

    def setBaseAction(self, actionName):
        """
        Действия на которое будет переключено
        после выполнения действия выполняемого единожды
        """
        if actionName not in self.__sprites:
            self.__baseAction = actionName

    def addAction(self, actionName, isApplyDir=False, isSingleExecute=False):
        if actionName not in self.__sprites:
            self.__sprites[actionName] = SpriteManager.SpritesTuple(isApplyDir, isSingleExecute)

    def setAction(self, actionName):
        if actionName in self.__sprites:
            self.__currentAction = actionName

    def addSprite(self, actionName, spriteModifier, time: float = 0.3, shiftX=0, shiftY=0):
        """
                Добавление спрайта к действию.
                :param actionName: Название действия.
                :param spriteModifier: Модификатор названия спрайта добавляемый к базовому имени.
                :param time: Время отображения спрайта.
                :param shiftX: Сдвиг спрайта по оси X.
                :param shiftY: Сдвиг спрайта по оси Y.
                """
        if actionName not in self.__sprites:
            return

        self.__sprites[actionName].addSprite(
            self.__baseName + spriteModifier, time, [shiftX, shiftY]
        )

    @property
    def dirX(self):
        if self.__direction == "_left":
            return -1

        elif self.__direction == "_right":
            return 1

        return 0

    @property
    def dirY(self):
        if self.__direction == "_up":
            return -1

        elif self.__direction == "_down":
            return 1

        return 0

    def setDir(self, dirX: int, dirY: int):
        """
        Установка определённого направления
        :param dirX: Направление по оси X
        :param dirY: Направление по оси Y
        """
        if dirX == 0 and dirY == 0:
            return
        else:
            if dirY > 0:
                self.__direction = "_down"
            elif dirY < 0:
                self.__direction = "_up"
            elif dirX > 0:
                self.__direction = "_right"
            elif dirX < 0:
                self.__direction = "_left"

    def __getCurSpriteTuple(self):
        if self.__currentAction not in self.__sprites:
            raise "Текущее действие не найдено в наборе существующих действий"

        currentAction = self.__sprites[self.__currentAction]
        if currentAction.count == 0:
            raise "Данное действие не содержит спрайтов"

        return currentAction

    def getSprite(self, speed: float = 1):
        """
        Получение спрайта для текущего шага в зависимости от флагов.
        :param speed: Время между кадрами.
        :return: Имя спрайта.
        """
        currentAction = self.__getCurSpriteTuple()

        # Если у спрайта есть условие "выполнять единожды",
        # то проверяем не закончился цикл выполнения
        if round(self.__step) >= currentAction.count:
            self.__step = 0
            if currentAction.isSingleExecute:
                self.__currentAction = self.__baseAction
                currentAction = self.__getCurSpriteTuple()

        curSprite = currentAction.getSpriteInfo(round(self.__step))
        self.__step += curSprite.time * speed

        spriteName = curSprite.spriteName
        if currentAction.isApplyDir:
            spriteName += self.__direction

        return spriteName, [curSprite.shiftX, curSprite.shiftY]

    @property
    def baseSpriteName(self):
        return self.__baseName

    @property
    def currentAction(self):
        return self.__currentAction
