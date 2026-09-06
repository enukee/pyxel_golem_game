import const
from events import Events
from map import MatrixMap
from objects import Stats
from units import Player
from units.Enemy import JumpingEnemy


class MimicEnemy(JumpingEnemy):
    def __init__(self, x: float, y: float, player: Player, stats: Stats):
        """
        Юнит врага Mimic.
        """
        super().__init__(x, y, player, "box", stats,
                         90, 15,
                         10, 10)

        # Мимик спит пока к нему не приблизится игрок
        self.__isWakeUp = False
        self.__wakeUpSprite = "mimic"

        self.spriteManager.addAction(const.ACTION_NONE)
        self.spriteManager.addSprite(const.ACTION_NONE, "")
        self.spriteManager.setBaseAction(const.ACTION_NONE)

    def update(self, events: Events, tileMap: MatrixMap, delta_time: float = const.DELTA_TIME):
        if self.__isWakeUp:
            return super().update(events, tileMap, delta_time)

        if super().isPlayerNearby(const.MIMIC_WAKE_UP_DISTANCE**2):
            self.__isWakeUp = True
            self.spriteManager.baseSpriteName = self.__wakeUpSprite
            self.__setActionSprite()

        return False

    def __setActionSprite(self):
        self.spriteManager.addAction(const.ACTION_MOVING)
        self.spriteManager.addSprite(const.ACTION_MOVING, "", time=1.2)
        self.spriteManager.addSprite(const.ACTION_MOVING, "_bite", shiftY=2)

        self.spriteManager.addAction(const.ACTION_ATTACK)
        self.spriteManager.addSprite(const.ACTION_ATTACK, "")
        self.spriteManager.addSprite(const.ACTION_ATTACK, "_bite", shiftY=2)
