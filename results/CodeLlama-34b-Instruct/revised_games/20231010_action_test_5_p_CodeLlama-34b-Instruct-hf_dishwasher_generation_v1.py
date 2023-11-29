class Device(GameObject):
    def __init__(self, name):
        GameObject.__init__(self, name)
        self.properties["isDevice"] = True

class Screwdriver(Device):
    def __init__(self):
        Device.__init__(self, "screwdriver")

        # Set the properties of this object
        self.properties["isScrewdriver"] = True
