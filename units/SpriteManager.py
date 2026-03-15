
class SpriteManager:
    class SpritesTuple:
        def __init__(self):
            """
            Набор модификаторов спрайтов.
            """
            self.sprites = []               # Названия спрайтов
            self.spritesShowTime = []       # Время показа спрайтов
            self.spritesShift = []          # Сдвиг спрайта при отрисовке

        @property
        def count(self):
            """
            Количество спрайтов.
            """
            return len(self.sprites)

    def __init__(self, baseSpriteName: str):
        """
        Менеджер спрайтов.
        :param baseSpriteName: Базовое имя спрайта.
        """
        self.__step = 0
        self.__baseName = baseSpriteName        # Базовое имя спрайта(имя спрайта должно начинаться с базового имени)

        self.__isMoving = False
        self.__spritesMoving = SpriteManager.SpritesTuple()   # Стандартные спрайты передвижения юнита
        self.__direction = "_down"                            # Направление движения спрайта

        self.__isStartAttack = False
        self.__spritesAttack = SpriteManager.SpritesTuple()   # Стандартные спрайты атаки

    def startAttack(self):
        """
        Начало атаки.
        """
        if not self.__isStartAttack:
            self.__isStartAttack = True
            self.__step = 0

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
            self.__isMoving = False
        else:
            self.__isMoving = True
            if dirY > 0:
                self.__direction = "_down"
            elif dirY < 0:
                self.__direction = "_up"
            elif dirX > 0:
                self.__direction = "_right"
            elif dirX < 0:
                self.__direction = "_left"

    def getSprite(self, speed: float = 1,  applyDir=False):
        """
        Получение спрайта для текущего шага в зависимости от флагов.
        :param speed: Время между кадрами.
        :param applyDir: Флаг добавления модификатора направления.
        :return: Имя спрайта.
        """
        dir = self.__direction if applyDir else ""

        if self.__spritesAttack.count and self.__isStartAttack:      # Если режим атаки активен
            return self.getSpriteAttack(speed) + dir, self.__spritesAttack.spritesShift[int(self.__step)]

        return self.getSpriteMoving(speed) + dir, self.__spritesMoving.spritesShift[int(self.__step)]

    def addSpriteAttack(self, sprite: str, time: float = 0.3, shiftX=0, shiftY=0):
        """
        Добавление спрайта передвижения атаки.
        :param sprite: Название спрайта.
        :param time: Время отображения спрайта.
        :param shiftX: Сдвиг спрайта по оси X.
        :param shiftY: Сдвиг спрайта по оси Y.
        """
        self.__spritesAttack.sprites.append(self.__baseName + sprite)
        self.__spritesAttack.spritesShowTime.append(time)
        self.__spritesAttack.spritesShift.append([shiftX, shiftY])

    def getSpriteAttack(self, speed: float = 1):
        """
        Получение спрайта для текущего шага.
        :param speed: Время между кадрами.
        :return имя спрайта.
        """
        # Увеличение шага
        self.__step += self.__spritesAttack.spritesShowTime[int(self.__step)] * speed
        if round(self.__step) >= self.__spritesAttack.count:
            self.__step = 0
            self.__isStartAttack = False        # Анимация атаки срабатывает один раз
            # после флаг активности атаки сбрасывается автоматически

        return self.__spritesAttack.sprites[int(self.__step)]

    def addSpriteMoving(self, sprite: str, time: float = 0.3, shiftX=0, shiftY=0):
        """
        Добавление спрайта передвижения юнита.
        :param sprite: Название спрайта.
        :param time: Время отображения спрайта.
        :param shiftX: Сдвиг спрайта по оси X.
        :param shiftY: Сдвиг спрайта по оси Y.
        """
        self.__spritesMoving.sprites.append(self.__baseName + sprite)
        self.__spritesMoving.spritesShowTime.append(time)
        self.__spritesMoving.spritesShift.append([shiftX, shiftY])

    def getSpriteMoving(self, speed: float = 1):
        """
        Получение спрайта для текущего шага.
        :param speed: Время между кадрами.
        :return имя спрайта.
        """
        if self.__isMoving:     # Передвижение с направлением
            # Увеличение шага
            self.__step += self.__spritesMoving.spritesShowTime[int(self.__step)] * speed
            self.__step = self.__step % self.__spritesMoving.count

        else:
            self.__step = 0     # Отрисовка спрайта без движения

        return self.__spritesMoving.sprites[int(self.__step)]

    @property
    def baseSpriteName(self):
        return self.__baseName
