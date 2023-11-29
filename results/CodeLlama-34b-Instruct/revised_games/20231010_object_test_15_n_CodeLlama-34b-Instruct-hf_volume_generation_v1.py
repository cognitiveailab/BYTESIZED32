class World:
    def __init__(self):
        self.objects = []

    def addObject(self, obj):
        self.objects.append(obj)

    def getAllContainedObjectsRecursive(self):
        outList = []
        for obj in self.objects:
            outList.append(obj)
            outList.extend(obj.getAllContainedObjectsRecursive())
        return outList
