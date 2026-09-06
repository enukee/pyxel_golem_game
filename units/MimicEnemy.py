import const
from objects import Stats
from units import Player
from units.Enemy import JumpingEnemy


class MimicEnemy(JumpingEnemy):
    def __init__(self, x: float, y: float, player: Player, stats: Stats):
        """
        Юнит врага Mimic.
        """
        super().__init__(x, y, player, "mimic", stats,
                         90, 15,
                         10, 10)

        self.spriteManager.addAction(const.ACTION_NONE)
        self.spriteManager.addSprite(const.ACTION_NONE, "")
        self.spriteManager.setBaseAction(const.ACTION_NONE)

        self.spriteManager.addAction(const.ACTION_MOVING)
        self.spriteManager.addSprite(const.ACTION_MOVING, "")
        self.spriteManager.addSprite(const.ACTION_MOVING, "")
        self.spriteManager.addSprite(const.ACTION_MOVING, "")
        self.spriteManager.addSprite(const.ACTION_MOVING, "")
        self.spriteManager.addSprite(const.ACTION_MOVING, "_bite", shiftY=2)

        self.spriteManager.addAction(const.ACTION_ATTACK)
        self.spriteManager.addSprite(const.ACTION_ATTACK, "")
        self.spriteManager.addSprite(const.ACTION_ATTACK, "_bite", shiftY=2)