
class SpriteManager:
    class SpritesTuple:
        def __init__(self):
            self.sprites = []             # Названия спрайтов
            self.spritesShowTime = []     # Время показа спрайтов

    def __init__(self, baseSpriteName: str):
        """
        Менеджер спрайтов.
        """
        self.__step = 0
        self.__baseName = baseSpriteName        # Базовое имя спрайта(имя спрайта должно начинаться с базового имени)

        self.__isMoving = False
        self.__spritesMoving = SpriteManager.SpritesTuple()   # Стандартные спрайты передвижения юнита
        self.__direction = "_down"                            # Направление движения спрайта

        self.__spritesAttack = SpriteManager.SpritesTuple()   # Стандартные спрайты атаки

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

    def addSpriteModifier(self, sprite: str, time: float = 0.3):
        """
        Добавление спрайта передвижения юнита.
        :param sprite: Название спрайта.
        :param time: Время отображения спрайта.
        """
        self.__spritesMoving.sprites.append(self.__baseName + sprite)
        self.__spritesMoving.spritesShowTime.append(time)

    def getSpriteMoving(self, speed: float = 1,  applyDir=False):
        """
        Получение спрайта для текущего шага.
        :return имя спрайта.
        """
        if not applyDir:        # Движение без направления(не направленные виды спрайта без "_<direction>" в имени)
            return self.__spritesMoving.sprites[int(self.__step)]

        if self.__isMoving:     # Передвижение с направлением
            # Увеличение шага
            self.__step += self.__spritesMoving.spritesShowTime[int(self.__step)] * speed
            self.__step = self.__step % len(self.__spritesMoving.spritesShowTime)

        else:
            self.__step = 0     # Отрисовка спрайта без движения

        return self.__spritesMoving.sprites[int(self.__step)] + self.__direction

    @property
    def baseSpriteName(self):
        return self.__baseName
