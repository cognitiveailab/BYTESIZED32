#
#   WaterContainer
#

class WaterContainer(Container):
    def __init__(self, name):
        GameObject.__init__(self, name)
        Container.__init__(self, name)

        self.properties["isWaterContainer"] = True
        self.properties["isMoveable"] = True
        self.properties["isOpenable"] = False
        self.properties["isOpen"] = True
        self.properties["containerPrefix"] = "in"
        self.properties["containedVolume"] = 0
        self.properties["containsLiquid"] = False

    def makeDescriptionStr(self, makeDetailed=False):
        outStr = f"a {self.name}"

        if self.properties["containsLiquid"]:
            outStr += " containing liquid"
        else:
            outStr += " that is empty"

        return outStr
