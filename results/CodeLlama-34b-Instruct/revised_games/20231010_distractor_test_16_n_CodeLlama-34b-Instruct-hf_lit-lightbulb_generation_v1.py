class ContainerVolumeWeightObject(VolumeWeightObject, Container):
    def __init__(self, name, volume, weight, containedVolume, containsLiquid, waterOutPerTick, isOn, isAnswerable):
        VolumeWeightObject.__init__(self, name, volume, weight)
        Container.__init__(self, name)
        self.properties["containedVolume"] = containedVolume
        self.properties["containsLiquid"] = containsLiquid
        self.properties["waterOutPerTick"] = waterOutPerTick
        self.properties["isOn"] = isOn
        self.properties["isAnswerable"] = isAnswerable

    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name
