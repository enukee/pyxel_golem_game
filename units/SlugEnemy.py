import const
from objects import Stats
from units import Player
from units.Enemy import JumpingEnemy


class SlugEnemy(JumpingEnemy):
    def __init__(self, x: float, y: float, player: Player, stats: Stats):
        """
        Юнит врага Mimic.
        """
        super().__init__(x, y, player, "slug", stats,
                         200, 10,
                         30, 30)

        self.spriteManager.addAction(const.ACTION_NONE)
        self.spriteManager.addSprite(const.ACTION_NONE, "")
        self.spriteManager.setBaseAction(const.ACTION_NONE)

        self.spriteManager.addAction(const.ACTION_MOVING)
        self.spriteManager.addSprite(const.ACTION_MOVING, "")
