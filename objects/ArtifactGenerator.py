from copy import deepcopy
from random import choices

from objects._Artifact import *


class ArtifactGenerator:
    def __init__(self):
        artifacts = {
            SilverFork(): .34,
            FlowerVine(): .12,
            MedicinalClover(): .05,
            ScarletBug(): .03,
            SilverRing(): .1,
            MagicAmanita(): .02,
        }

        self.keys = list(artifacts.keys())
        self.chance = list(artifacts.values())

    def genArtifactsBox(self, n):
        artList = []
        for _ in range(n):
            artifact = choices(self.keys, weights=self.chance, k=1)[0]
            artList.append(deepcopy(artifact))

        return artList
