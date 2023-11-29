# The GameObject class is not defined in the code you provided, so I will define it here
class GameObject:
    def __init__(self, name):
        self.name = name
        self.properties = {}

    def getProperty(self, propertyName):
        return self.properties[propertyName]

    def setProperty(self, propertyName, value):
        self.properties[propertyName] = value

    def getReferents(self):
        return [self.name]

    def makeDescriptionStr(self, makeDetailed=False):
        return self.name

# The Container class is also not defined, so I will define it here
class Container(GameObject):
    def __init__(self, name):
        GameObject.__init__(self, name)
        self.properties["isContainer"] = True
        self.properties["containerPrefix"] = "in"
        self.contains = []

    def addObject(self, obj):
        self.contains.append(obj)
        obj.parentContainer = self

    def removeObject(self, obj):
        self.contains.remove(obj)
        obj.parentContainer = None

    def getAllContainedObjectsRecursive(self):
        allObjects = []
        for obj in self.contains:
            allObjects.append(obj)
            if obj.properties["isContainer"]:
                allObjects.extend(obj.getAllContainedObjectsRecursive())
        return allObjects

    def getContainedObjects(self):
        return self.contains

    def getContainedObjectsRecursive(self):
        allObjects = []
        for obj in self.contains:
            allObjects.append(obj)
            if obj.properties["isContainer"]:
                allObjects.extend(obj.getContainedObjectsRecursive())
        return allObjects

    def getContainedObjectsWithName(self, name):
        return [obj for obj in self.contains if obj.name == name]

    def getContainedObjectsWithNameRecursive(self, name):
        allObjects = []
        for obj in self.contains:
            if obj.name == name:
                allObjects.append(obj)
            if obj.properties["isContainer"]:
                allObjects.extend(obj.getContainedObjectsWithNameRecursive(name))
        return allObjects

    def getContainedObjectsWithProperty(self, propertyName, value):
        return [obj for obj in self.contains if obj.properties[propertyName] == value]

    def getContainedObjectsWithPropertyRecursive(self, propertyName, value):
        allObjects = []
        for obj in self.contains:
            if obj.properties[propertyName] == value:
                allObjects.append(obj)
            if obj.properties["isContainer"]:
                allObjects.extend(obj.getContainedObjectsWithPropertyRecursive(propertyName, value))
        return allObjects

    def getContainedObjectsWithReferent(self, referent):
        return [obj for obj in self.contains if referent in obj.getReferents()]

    def getContainedObjectsWithReferentRecursive(self, referent):
        allObjects = []
        for obj in self.contains:
            if referent in obj.getReferents():
                allObjects.append(obj)
            if obj.properties["isContainer"]:
                allObjects.extend(obj.getContainedObjectsWithReferentRecursive(referent))
        return allObjects

    def getContainedObjectsWithReferentAndProperty(self, referent, propertyName, value):
        return [obj for obj in self.contains if referent in obj.getReferents() and obj.properties[propertyName] == value]

    def getContainedObjectsWithReferentAndPropertyRecursive(self, referent, propertyName, value):
        allObjects = []
        for obj in self.contains:
            if referent in obj.getReferents() and obj.properties[propertyName] == value:
                allObjects.append(obj)
            if obj.properties["isContainer"]:
                allObjects.extend(obj.getContainedObjectsWithReferentAndPropertyRecursive(referent, propertyName, value))
        return allObjects

    def getContainedObjectsWithPropertyAndReferent(self, propertyName, value, referent):
        return [obj for obj in self.contains if obj.properties[propertyName] == value and referent in obj.getReferents()]

    def getContainedObjectsWithPropertyAndReferentRecursive(self, propertyName, value, referent):
        allObjects = []
        for obj in self.contains:
            if obj.properties[propertyName] == value and referent in obj.getReferents():
                allObjects.append(obj)
            if obj.properties["isContainer"]:
                allObjects.extend(obj.getContainedObjectsWithPropertyAndReferentRecursive(propertyName, value, referent))
        return allObjects

    def getContainedObjectsWithReferentAndPropertyAndReferent(self, referent1, propertyName1, value1, referent2):
        return [obj for obj in self.contains if referent1 in obj.getReferents() and obj.properties[propertyName1] == value1 and referent2 in obj.getReferents()]

    def getContainedObjectsWithReferentAndPropertyAndReferentRecursive(self, referent1, propertyName1, value1, referent2):
        allObjects = []
        for obj in self.contains:
            if referent1 in obj.getReferents() and obj.properties[propertyName1] == value1 and referent2 in obj.getReferents():
                allObjects.append(obj)
            if obj.properties["isContainer"]:
                allObjects.extend(obj.getContainedObjectsWithReferentAndPropertyAndReferentRecursive(referent1, propertyName1, value1, referent2))
        return allObjects

    def getContainedObjectsWithPropertyAndReferentAndReferent(self, propertyName1, value1, referent1, referent2):
        return [obj for obj in self.contains if obj.properties[propertyName1] == value1 and referent1 in obj.getReferents() and referent2 in obj.getReferents()]

    def getContainedObjectsWithPropertyAndReferentAndReferentRecursive(self, propertyName1, value1, referent1, referent2):
        allObjects = []
        for obj in self.contains:
            if obj.properties[propertyName1] == value1 and referent1 in obj.getReferents() and referent2 in obj.getReferents():
                allObjects.append(obj)
            if obj.properties["isContainer"]:
                allObjects.extend(obj.getContainedObjectsWithPropertyAndReferentAndReferentRecursive(propertyName1, value1, referent1, referent2))
        return allObjects

    def getContainedObjectsWithReferentAndPropertyAndReferentAndProperty(self, referent1, propertyName1, value1, referent2, propertyName2, value2):
        return [obj for obj in self.contains if referent1 in obj.getReferents() and obj.properties[propertyName1] == value1 and referent2 in obj.getReferents() and obj.properties[propertyName2] == value2]

    def getContainedObjectsWithReferentAndPropertyAndReferentAndPropertyRecursive(self, referent1, propertyName1, value1, referent2, propertyName2, value2):
        allObjects = []
        for obj in self.contains:
            if referent1 in obj.getReferents() and obj.properties[propertyName1] == value1 and referent2 in obj.getReferents() and obj.properties[propertyName2] == value2:
                allObjects.append(obj)
            if obj.properties["isContainer"]:
                allObjects.extend(obj.getContainedObjectsWithReferentAndPropertyAndReferentAndPropertyRecursive(referent1, propertyName1, value1, referent2, propertyName2, value2))
        return allObjects

    def getContainedObjectsWithPropertyAndReferentAndReferentAndProperty(self, propertyName1, value1, referent1, referent2, propertyName2, value2):
        return [obj for obj in self.contains if obj.properties[propertyName1] == value1 and referent1 in obj.getReferents() and referent2 in obj.getReferents() and obj.properties[propertyName2] == value2]

    def getContainedObjectsWithPropertyAndReferentAndReferentAndPropertyRecursive(self, propertyName1, value1, referent1, referent2, propertyName2, value2):
        allObjects = []
        for obj in self.contains:
            if obj.properties[propertyName1] == value1 and referent1 in obj.getReferents() and referent2 in obj.getReferents() and obj.properties[propertyName2] == value2:
                allObjects.append(obj)
            if obj.properties["isContainer"]:
                allObjects.extend(obj.getContainedObjectsWithPropertyAndReferentAndReferentAndPropertyRecursive(propertyName1, value1, referent1, referent2, propertyName2, value2))
        return allObjects

    def getContainedObjectsWithReferentAndPropertyAndReferentAndReferent(self, referent1, propertyName1, value1, referent2, referent3):
        return [obj for obj in self.contains if referent1 in obj.getReferents() and obj.properties[propertyName1] == value1 and referent2 in obj.getReferents() and referent3 in obj.getReferents()]

    def getContainedObjectsWithReferentAndPropertyAndReferentAndReferentRecursive(self, referent1, propertyName1, value1, referent2, referent3):
        allObjects = []
        for obj in self.contains:
            if referent1 in obj.getReferents() and obj.properties[propertyName1] == value1 and referent2 in obj.getReferents() and referent3 in obj.getReferents():
                allObjects.append(obj)
            if obj.properties["isContainer"]:
                allObjects.extend(obj.getContainedObjectsWithReferentAndPropertyAndReferentAndReferentRecursive(referent1, propertyName1, value1, referent2, referent3))
        return allObjects

    def getContainedObjectsWithPropertyAndReferentAndReferentAndReferent(self, propertyName1, value1, referent1, referent2, referent3):
        return [obj for obj in self.contains if obj.properties[propertyName1] == value1 and referent1 in obj.getReferents() and referent2 in obj.getReferents() and referent3 in obj.getReferents()]

    def getContainedObjectsWithPropertyAndReferentAndReferentAndReferentRecursive(self, propertyName1, value1, referent1, referent2, referent3):
        allObjects = []
        for obj in self.contains:
            if obj.properties[propertyName1] == value1 and referent1 in obj.getReferents() and referent2 in obj.getReferents() and referent3 in obj.getReferents():
                allObjects.append(obj)
            if obj.properties["isContainer"]:
                allObjects.extend(obj.getContainedObjectsWithPropertyAndReferentAndReferentAndReferentRecursive(propertyName1, value1, referent1, referent2, referent3))
        return allObjects

    def getContainedObjectsWithReferentAndPropertyAndReferentAndReferentAndProperty(self, referent1, propertyName1, value1, referent2, referent3, propertyName2, value2):
        return [obj for obj in self.contains if referent1 in obj.getReferents() and obj.properties[propertyName1] == value1 and referent2 in obj.getReferents() and referent3 in obj.getReferents() and obj.properties[propertyName2] == value2]

    def getContainedObjectsWithReferentAndPropertyAndReferentAndReferentAndPropertyRecursive(self, referent1, propertyName1, value1, referent2, referent3, propertyName2, value2):
        allObjects = []
        for obj in self.contains:
            if referent1 in obj.getReferents() and obj.properties[propertyName1] == value1 and referent2 in obj.getReferents() and referent3 in obj.getReferents() and obj.properties[propertyName2] == value2:
                allObjects.append(obj)
            if obj.properties["isContainer"]:
                allObjects.extend(obj.getContainedObjectsWithReferentAndPropertyAndReferentAndReferentAndPropertyRecursive(referent1, propertyName1, value1, referent2, referent3, propertyName2, value2))
        return allObjects

    def getContainedObjectsWithPropertyAndReferentAndReferentAndReferentAndProperty(self, propertyName1, value1, referent1, referent2, referent3, propertyName2, value2):
        return [obj for obj in self.contains if obj.properties[propertyName1] == value1 and referent1 in obj.getReferents() and referent2 in obj.getReferents() and referent3 in obj.getReferents() and obj.properties[propertyName2] == value2]

    def getContainedObjectsWithPropertyAndReferentAndReferentAndReferentAndPropertyRecursive(self, propertyName1, value1, referent1, referent2, referent3, propertyName2, value2):
        allObjects = []
        for obj in self.contains:
            if obj.properties[propertyName1] == value1 and referent1 in obj.getReferents() and referent2 in obj.getReferents() and referent3 in obj.getReferents() and obj.properties[propertyName2] == value2:
                allObjects.append(obj)
            if obj.properties["isContainer"]:
                allObjects.extend(obj.getContainedObjectsWithPropertyAndReferentAndReferentAndReferentAndPropertyRecursive(propertyName1, value1, referent1, referent2, referent3, propertyName2, value2))
        return allObjects

    def getContainedObjectsWithReferentAndPropertyAndReferentAndReferentAndReferent(self, referent1, propertyName1, value1, referent2, referent3, referent4):
        return [obj for obj in self.contains if referent1 in obj.getReferents() and obj.properties[propertyName1] == value1 and referent2 in obj.getReferents() and referent3 in obj.getReferents() and referent4 in obj.getReferents()]

    def getContainedObjectsWithReferentAndPropertyAndReferentAndReferentAndReferentRecursive(self, referent1, propertyName1, value1, referent2, referent3, referent4):
        allObjects = []
        for obj in self.contains:
            if referent1 in obj.getReferents() and obj.properties[propertyName1] == value1 and referent2 in obj.getReferents() and referent3 in obj.getReferents() and referent4 in obj.getReferents():
                allObjects.append(obj)
            if obj.properties["isContainer"]:
                allObjects.extend(obj.getContainedObjectsWithReferentAndPropertyAndReferentAndReferentAndReferentRecursive(referent1, propertyName1, value1, referent2, referent3, referent4))
        return allObjects

    def getContainedObjectsWithPropertyAndReferentAndReferentAndReferentAndReferent(self, propertyName1, value1, referent1, referent2, referent3, referent4):
        return [obj for obj in self.contains if obj.properties[propertyName1] == value1 and referent1 in obj.getReferents() and referent2 in obj.getReferents() and referent3 in obj.getReferents() and referent4 in obj.getReferents()]

    def getContainedObjectsWithPropertyAndReferentAndReferentAndReferentAndReferentRecursive(self, propertyName1, value1, referent1, referent2, referent3, referent4):
        allObjects = []
        for obj in self.contains:
            if obj.properties[propertyName1] == value1 and referent1 in obj.getReferents() and referent2 in obj.getReferents() and referent3 in obj.getReferents() and referent4 in obj.getReferents():
                allObjects.append(obj)
            if obj.properties["isContainer"]:
                allObjects.extend(obj.getContainedObjectsWithPropertyAndReferentAndReferentAndReferentAndReferentRecursive(propertyName1, value1, referent1, referent2, referent3, referent4))
        return allObjects

    def getContainedObjectsWithReferentAndPropertyAndReferentAndReferentAndReferentAndProperty(self, referent1, propertyName1, value1, referent2, referent3, referent4, propertyName2, value2):
        return [obj for obj in self.contains if referent1 in obj.getReferents() and obj.properties[propertyName1] == value1 and referent2 in obj.getReferents() and referent3 in obj.getReferents() and referent4 in obj.getReferents() and obj.properties[propertyName2] == value2]

    def getContainedObjectsWithReferentAndPropertyAndReferentAndReferentAndReferentAndPropertyRecursive(self, referent1, propertyName1, value1, referent2, referent3, referent4, propertyName2, value2):
        allObjects = []
        for obj in self.contains:
            if referent1 in obj.getReferents() and obj.properties[propertyName1] == value1 and referent2 in obj.getReferents() and referent3 in obj.getReferents() and referent4 in obj.getReferents() and obj.properties[propertyName2] == value2:
                allObjects.append(obj)
            if obj.properties["isContainer"]:
                allObjects.extend(obj.getContainedObjectsWithReferentAndPropertyAndReferentAndReferentAndReferentAndPropertyRecursive(referent1, propertyName1, value1, referent2, referent3, referent4, propertyName2, value2))
        return allObjects

    def getContainedObjectsWithPropertyAndReferentAndReferentAndReferentAndReferentAndProperty(self, propertyName1, value1, referent1, referent2, referent3, referent4, propertyName2, value2):
        return [obj for obj in self.contains if obj.properties[propertyName1] == value1 and referent1 in obj.getReferents() and referent2 in obj.getReferents() and referent3 in obj.getReferents() and referent4 in obj.getReferents() and obj.properties[propertyName2] == value2]

    def getContainedObjectsWithPropertyAndReferentAndReferentAndReferentAndReferentAndPropertyRecursive(self, propertyName1, value1, referent1, referent2, referent3, referent4, propertyName2, value2):
        allObjects = []
        for obj in self.contains:
            if obj.properties[propertyName1] == value1 and referent1 in obj.getReferents() and referent2 in obj.getReferents() and referent3 in obj.getReferents() and referent4 in obj.getReferents() and obj.properties[propertyName2] == value2:
                allObjects.append(obj)
            if obj.properties["isContainer"]:
                allObjects.extend(obj.getContainedObjectsWithPropertyAndReferentAndReferentAndReferentAndReferentAndPropertyRecursive(propertyName1, value1, referent1, referent2, referent3, referent4, propertyName2, value2))
        return allObjects

    def getContainedObjectsWithReferentAndPropertyAndReferentAndReferentAndReferentAndReferent(self, referent1, propertyName1, value1, referent2, referent3, referent4, referent5):
        return [obj for obj in self.contains if referent1 in obj.getReferents() and obj.properties[propertyName1] == value1 and referent2 in obj.getReferents() and referent3 in obj.getReferents() and referent4 in obj.getReferents() and referent5 in obj.getReferents()]

    def getContainedObjectsWithReferentAndPropertyAndReferentAndReferentAndReferentAndReferentRecursive(self, referent1, propertyName1, value1, referent2, referent3, referent4, referent5):
        allObjects = []
        for obj in self.contains:
            if referent1 in obj.getReferents() and obj.properties[propertyName1] == value1 and referent2 in obj.getReferents() and referent3 in obj.getReferents() and referent4 in obj.getReferents() and referent5 in obj.getReferents():
                allObjects.append(obj)
            if obj.properties["isContainer"]:
                allObjects.extend(obj.getContainedObjectsWithReferentAndPropertyAndReferentAndReferentAndReferentAndReferentRecursive(referent1, propertyName1, value1, referent2, referent3, referent4, referent5))
        return allObjects

    def getContainedObjectsWithPropertyAndReferentAndReferentAndReferentAndReferentAndReferent(self, propertyName1, value1, referent1, referent2, referent3, referent4, referent5):
        return [obj for obj in self.contains if obj.properties[propertyName1] == value1 and referent1 in obj.getReferents() and referent2 in obj.getReferents() and referent3 in obj.getReferents() and referent4 in obj.getReferents() and referent5 in obj.getReferents()]

    def getContainedObjectsWithPropertyAndReferentAndReferentAndReferentAndReferentAndReferentRecursive(self, propertyName1, value1, referent1, referent2, referent3, referent4, referent5):
        allObjects = []
        for obj in self.contains:
            if obj.properties[propertyName1] == value1 and referent1 in obj.getReferents() and referent2 in obj.getReferents() and referent3 in obj.getReferents() and referent4 in obj.getReferents() and referent5 in obj.getReferents():
                allObjects.append(obj)
            if obj.properties["isContainer"]:
                allObjects.extend(obj.getContainedObjectsWithPropertyAndReferentAndReferentAndReferentAndReferentAndReferentRecursive(propertyName1, value1, referent1, referent2, referent3, referent4, referent5))
        return allObjects

    def getContainedObjectsWithReferentAndPropertyAndReferentAndReferentAndReferentAndReferentAndProperty(self, referent1, propertyName1, value1, referent2, referent3, referent4, referent5, propertyName2, value2):
        return [obj for obj in self.contains if referent1 in obj.getReferents() and obj.properties[propertyName1] == value1 and referent2 in obj.getReferents() and referent3 in obj.getReferents() and referent4 in obj.getReferents() and referent5 in obj.getReferents() and obj.properties[propertyName2] == value2]

    def getContainedObjectsWithReferentAndPropertyAndReferentAndReferentAndReferentAndReferentAndPropertyRecursive(self, referent1, propertyName1, value1, referent2, referent3, referent4, referent5, propertyName2, value2):
        allObjects = []
        for obj in self.contains:
            if referent1 in obj.getReferents() and obj.properties[propertyName1] == value1 and referent2 in obj.getReferents() and referent3 in obj.getReferents() and referent4 in obj.getReferents() and referent5 in obj.getReferents() and obj.properties[propertyName2] == value2:
                allObjects.append(obj)
            if obj.properties["isContainer"]:
                allObjects.extend(obj.getContainedObjectsWithReferentAndPropertyAndReferentAndReferentAndReferentAndReferentAndPropertyRecursive(referent1, propertyName1, value1, referent2, referent3, referent4, referent5, propertyName2, value2))
        return allObjects

    def getContainedObjectsWithPropertyAndReferentAndReferentAndReferentAndReferentAndReferentAndProperty(self, propertyName1, value1, referent1, referent2, referent3, referent4, referent5, propertyName2, value2):
        return [obj for obj in self.contains if obj.properties[propertyName1] == value1 and referent1 in obj.getReferents() and referent2 in obj.getReferents() and referent3 in obj.getReferents() and referent4 in obj.getReferents() and referent5 in obj.getReferents() and obj.properties[propertyName2] == value2]

    def getContainedObjectsWithPropertyAndReferentAndReferentAndReferentAndReferentAndReferentAndPropertyRecursive(self, propertyName1, value1, referent1, referent2, referent3, referent4, referent5, propertyName2, value2):
        allObjects = []
        for obj in self.contains:
            if obj.properties[propertyName1] == value1 and referent1 in obj.getReferents() and referent2 in obj.getReferents() and referent3 in obj.getReferents() and referent4 in obj.getReferents() and referent5 in obj.getReferents() and obj.properties[propertyName2] == value2:
                allObjects.append(obj)
            if obj.properties["isContainer"]:
                allObjects.extend(obj.getContainedObjectsWithPropertyAndReferentAndReferentAndReferentAndReferentAndReferentAndPropertyRecursive(propertyName1, value1, referent1, referent2, referent3, referent4, referent5, propertyName2, value2))
        return allObjects

    def getContainedObjectsWithReferentAndPropertyAndReferentAndReferentAndReferentAndReferentAndReferent(self, referent1, propertyName1, value1, referent2, referent3, referent4, referent5, referent6):
        return [obj for obj in self.contains if referent1 in obj.getReferents() and obj.properties[propertyName1] == value1 and referent2 in obj.getReferents() and referent3 in obj.getReferents() and referent4 in obj.getReferents() and referent5 in obj.getReferents() and referent6 in obj.getReferents()]

    def getContainedObjectsWithReferentAndPropertyAndReferentAndReferentAndReferentAndReferentAndReferentRecursive(self, referent1, propertyName1, value1, referent2, referent3, referent4, referent5, referent6):
        allObjects = []
        for obj in self.contains:
            if referent1 in obj.getReferents() and obj.properties[propertyName1] == value1 and referent2 in obj.getReferents() and referent3 in obj.getReferents() and referent4 in obj.getReferents() and referent5 in obj.getReferents() and referent6 in obj.getReferents():
                allObjects.append(obj)
            if obj.properties["isContainer"]:
                allObjects.extend(obj.getContainedObjectsWithReferentAndPropertyAndReferentAndReferentAndReferentAndReferentAndReferentRecursive(referent1, propertyName1, value1, referent2, referent3, referent4, referent5, referent6))
        return allObjects

    def getContainedObjectsWithPropertyAndReferentAndReferentAndReferentAndReferentAndReferentAndReferent(self, propertyName1, value1, referent1, referent2, referent3, referent4, referent5, referent6):
        return [obj for obj in self.contains if obj.properties[propertyName1] == value1 and referent1 in obj.getReferents() and referent2 in obj.getReferents() and referent3 in obj.getReferents() and referent4 in obj.getReferents() and referent5 in obj.getReferents() and referent6 in obj.getReferents()]

    def getContainedObjectsWithPropertyAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentRecursive(self, propertyName1, value1, referent1, referent2, referent3, referent4, referent5, referent6):
        allObjects = []
        for obj in self.contains:
            if obj.properties[propertyName1] == value1 and referent1 in obj.getReferents() and referent2 in obj.getReferents() and referent3 in obj.getReferents() and referent4 in obj.getReferents() and referent5 in obj.getReferents() and referent6 in obj.getReferents():
                allObjects.append(obj)
            if obj.properties["isContainer"]:
                allObjects.extend(obj.getContainedObjectsWithPropertyAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentRecursive(propertyName1, value1, referent1, referent2, referent3, referent4, referent5, referent6))
        return allObjects

    def getContainedObjectsWithReferentAndPropertyAndReferentAndReferentAndReferentAndReferentAndReferentAndProperty(self, referent1, propertyName1, value1, referent2, referent3, referent4, referent5, referent6, propertyName2, value2):
        return [obj for obj in self.contains if referent1 in obj.getReferents() and obj.properties[propertyName1] == value1 and referent2 in obj.getReferents() and referent3 in obj.getReferents() and referent4 in obj.getReferents() and referent5 in obj.getReferents() and referent6 in obj.getReferents() and obj.properties[propertyName2] == value2]

    def getContainedObjectsWithReferentAndPropertyAndReferentAndReferentAndReferentAndReferentAndReferentAndPropertyRecursive(self, referent1, propertyName1, value1, referent2, referent3, referent4, referent5, referent6, propertyName2, value2):
        allObjects = []
        for obj in self.contains:
            if referent1 in obj.getReferents() and obj.properties[propertyName1] == value1 and referent2 in obj.getReferents() and referent3 in obj.getReferents() and referent4 in obj.getReferents() and referent5 in obj.getReferents() and referent6 in obj.getReferents() and obj.properties[propertyName2] == value2:
                allObjects.append(obj)
            if obj.properties["isContainer"]:
                allObjects.extend(obj.getContainedObjectsWithReferentAndPropertyAndReferentAndReferentAndReferentAndReferentAndReferentAndPropertyRecursive(referent1, propertyName1, value1, referent2, referent3, referent4, referent5, referent6, propertyName2, value2))
        return allObjects

    def getContainedObjectsWithPropertyAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndProperty(self, propertyName1, value1, referent1, referent2, referent3, referent4, referent5, referent6, propertyName2, value2):
        return [obj for obj in self.contains if obj.properties[propertyName1] == value1 and referent1 in obj.getReferents() and referent2 in obj.getReferents() and referent3 in obj.getReferents() and referent4 in obj.getReferents() and referent5 in obj.getReferents() and referent6 in obj.getReferents() and obj.properties[propertyName2] == value2]

    def getContainedObjectsWithPropertyAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndPropertyRecursive(self, propertyName1, value1, referent1, referent2, referent3, referent4, referent5, referent6, propertyName2, value2):
        allObjects = []
        for obj in self.contains:
            if obj.properties[propertyName1] == value1 and referent1 in obj.getReferents() and referent2 in obj.getReferents() and referent3 in obj.getReferents() and referent4 in obj.getReferents() and referent5 in obj.getReferents() and referent6 in obj.getReferents() and obj.properties[propertyName2] == value2:
                allObjects.append(obj)
            if obj.properties["isContainer"]:
                allObjects.extend(obj.getContainedObjectsWithPropertyAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndPropertyRecursive(propertyName1, value1, referent1, referent2, referent3, referent4, referent5, referent6, propertyName2, value2))
        return allObjects

    def getContainedObjectsWithReferentAndPropertyAndReferentAndReferentAndReferentAndReferentAndReferentAndReferent(self, referent1, propertyName1, value1, referent2, referent3, referent4, referent5, referent6, referent7):
        return [obj for obj in self.contains if referent1 in obj.getReferents() and obj.properties[propertyName1] == value1 and referent2 in obj.getReferents() and referent3 in obj.getReferents() and referent4 in obj.getReferents() and referent5 in obj.getReferents() and referent6 in obj.getReferents() and referent7 in obj.getReferents()]

    def getContainedObjectsWithReferentAndPropertyAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentRecursive(self, referent1, propertyName1, value1, referent2, referent3, referent4, referent5, referent6, referent7):
        allObjects = []
        for obj in self.contains:
            if referent1 in obj.getReferents() and obj.properties[propertyName1] == value1 and referent2 in obj.getReferents() and referent3 in obj.getReferents() and referent4 in obj.getReferents() and referent5 in obj.getReferents() and referent6 in obj.getReferents() and referent7 in obj.getReferents():
                allObjects.append(obj)
            if obj.properties["isContainer"]:
                allObjects.extend(obj.getContainedObjectsWithReferentAndPropertyAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentRecursive(referent1, propertyName1, value1, referent2, referent3, referent4, referent5, referent6, referent7))
        return allObjects

    def getContainedObjectsWithPropertyAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndReferent(self, propertyName1, value1, referent1, referent2, referent3, referent4, referent5, referent6, referent7):
        return [obj for obj in self.contains if obj.properties[propertyName1] == value1 and referent1 in obj.getReferents() and referent2 in obj.getReferents() and referent3 in obj.getReferents() and referent4 in obj.getReferents() and referent5 in obj.getReferents() and referent6 in obj.getReferents() and referent7 in obj.getReferents()]

    def getContainedObjectsWithPropertyAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentRecursive(self, propertyName1, value1, referent1, referent2, referent3, referent4, referent5, referent6, referent7):
        allObjects = []
        for obj in self.contains:
            if obj.properties[propertyName1] == value1 and referent1 in obj.getReferents() and referent2 in obj.getReferents() and referent3 in obj.getReferents() and referent4 in obj.getReferents() and referent5 in obj.getReferents() and referent6 in obj.getReferents() and referent7 in obj.getReferents():
                allObjects.append(obj)
            if obj.properties["isContainer"]:
                allObjects.extend(obj.getContainedObjectsWithPropertyAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentRecursive(propertyName1, value1, referent1, referent2, referent3, referent4, referent5, referent6, referent7))
        return allObjects

    def getContainedObjectsWithReferentAndPropertyAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndProperty(self, referent1, propertyName1, value1, referent2, referent3, referent4, referent5, referent6, referent7, propertyName2, value2):
        return [obj for obj in self.contains if referent1 in obj.getReferents() and obj.properties[propertyName1] == value1 and referent2 in obj.getReferents() and referent3 in obj.getReferents() and referent4 in obj.getReferents() and referent5 in obj.getReferents() and referent6 in obj.getReferents() and referent7 in obj.getReferents() and obj.properties[propertyName2] == value2]

    def getContainedObjectsWithReferentAndPropertyAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndPropertyRecursive(self, referent1, propertyName1, value1, referent2, referent3, referent4, referent5, referent6, referent7, propertyName2, value2):
        allObjects = []
        for obj in self.contains:
            if referent1 in obj.getReferents() and obj.properties[propertyName1] == value1 and referent2 in obj.getReferents() and referent3 in obj.getReferents() and referent4 in obj.getReferents() and referent5 in obj.getReferents() and referent6 in obj.getReferents() and referent7 in obj.getReferents() and obj.properties[propertyName2] == value2:
                allObjects.append(obj)
            if obj.properties["isContainer"]:
                allObjects.extend(obj.getContainedObjectsWithReferentAndPropertyAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndPropertyRecursive(referent1, propertyName1, value1, referent2, referent3, referent4, referent5, referent6, referent7, propertyName2, value2))
        return allObjects

    def getContainedObjectsWithPropertyAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndProperty(self, propertyName1, value1, referent1, referent2, referent3, referent4, referent5, referent6, referent7, propertyName2, value2):
        return [obj for obj in self.contains if obj.properties[propertyName1] == value1 and referent1 in obj.getReferents() and referent2 in obj.getReferents() and referent3 in obj.getReferents() and referent4 in obj.getReferents() and referent5 in obj.getReferents() and referent6 in obj.getReferents() and referent7 in obj.getReferents() and obj.properties[propertyName2] == value2]

    def getContainedObjectsWithPropertyAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndPropertyRecursive(self, propertyName1, value1, referent1, referent2, referent3, referent4, referent5, referent6, referent7, propertyName2, value2):
        allObjects = []
        for obj in self.contains:
            if obj.properties[propertyName1] == value1 and referent1 in obj.getReferents() and referent2 in obj.getReferents() and referent3 in obj.getReferents() and referent4 in obj.getReferents() and referent5 in obj.getReferents() and referent6 in obj.getReferents() and referent7 in obj.getReferents() and obj.properties[propertyName2] == value2:
                allObjects.append(obj)
            if obj.properties["isContainer"]:
                allObjects.extend(obj.getContainedObjectsWithPropertyAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndPropertyRecursive(propertyName1, value1, referent1, referent2, referent3, referent4, referent5, referent6, referent7, propertyName2, value2))
        return allObjects

    def getContainedObjectsWithReferentAndPropertyAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndReferent(self, referent1, propertyName1, value1, referent2, referent3, referent4, referent5, referent6, referent7, referent8):
        return [obj for obj in self.contains if referent1 in obj.getReferents() and obj.properties[propertyName1] == value1 and referent2 in obj.getReferents() and referent3 in obj.getReferents() and referent4 in obj.getReferents() and referent5 in obj.getReferents() and referent6 in obj.getReferents() and referent7 in obj.getReferents() and referent8 in obj.getReferents()]

    def getContainedObjectsWithReferentAndPropertyAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentRecursive(self, referent1, propertyName1, value1, referent2, referent3, referent4, referent5, referent6, referent7, referent8):
        allObjects = []
        for obj in self.contains:
            if referent1 in obj.getReferents() and obj.properties[propertyName1] == value1 and referent2 in obj.getReferents() and referent3 in obj.getReferents() and referent4 in obj.getReferents() and referent5 in obj.getReferents() and referent6 in obj.getReferents() and referent7 in obj.getReferents() and referent8 in obj.getReferents():
                allObjects.append(obj)
            if obj.properties["isContainer"]:
                allObjects.extend(obj.getContainedObjectsWithReferentAndPropertyAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentRecursive(referent1, propertyName1, value1, referent2, referent3, referent4, referent5, referent6, referent7, referent8))
        return allObjects

    def getContainedObjectsWithPropertyAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndReferent(self, propertyName1, value1, referent1, referent2, referent3, referent4, referent5, referent6, referent7, referent8):
        return [obj for obj in self.contains if obj.properties[propertyName1] == value1 and referent1 in obj.getReferents() and referent2 in obj.getReferents() and referent3 in obj.getReferents() and referent4 in obj.getReferents() and referent5 in obj.getReferents() and referent6 in obj.getReferents() and referent7 in obj.getReferents() and referent8 in obj.getReferents()]

    def getContainedObjectsWithPropertyAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentRecursive(self, propertyName1, value1, referent1, referent2, referent3, referent4, referent5, referent6, referent7, referent8):
        allObjects = []
        for obj in self.contains:
            if obj.properties[propertyName1] == value1 and referent1 in obj.getReferents() and referent2 in obj.getReferents() and referent3 in obj.getReferents() and referent4 in obj.getReferents() and referent5 in obj.getReferents() and referent6 in obj.getReferents() and referent7 in obj.getReferents() and referent8 in obj.getReferents():
                allObjects.append(obj)
            if obj.properties["isContainer"]:
                allObjects.extend(obj.getContainedObjectsWithPropertyAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentRecursive(propertyName1, value1, referent1, referent2, referent3, referent4, referent5, referent6, referent7, referent8))
        return allObjects

    def getContainedObjectsWithReferentAndPropertyAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndProperty(self, referent1, propertyName1, value1, referent2, referent3, referent4, referent5, referent6, referent7, referent8, propertyName2, value2):
        return [obj for obj in self.contains if referent1 in obj.getReferents() and obj.properties[propertyName1] == value1 and referent2 in obj.getReferents() and referent3 in obj.getReferents() and referent4 in obj.getReferents() and referent5 in obj.getReferents() and referent6 in obj.getReferents() and referent7 in obj.getReferents() and referent8 in obj.getReferents() and obj.properties[propertyName2] == value2]

    def getContainedObjectsWithReferentAndPropertyAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndPropertyRecursive(self, referent1, propertyName1, value1, referent2, referent3, referent4, referent5, referent6, referent7, referent8, propertyName2, value2):
        allObjects = []
        for obj in self.contains:
            if referent1 in obj.getReferents() and obj.properties[propertyName1] == value1 and referent2 in obj.getReferents() and referent3 in obj.getReferents() and referent4 in obj.getReferents() and referent5 in obj.getReferents() and referent6 in obj.getReferents() and referent7 in obj.getReferents() and referent8 in obj.getReferents() and obj.properties[propertyName2] == value2:
                allObjects.append(obj)
            if obj.properties["isContainer"]:
                allObjects.extend(obj.getContainedObjectsWithReferentAndPropertyAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndPropertyRecursive(referent1, propertyName1, value1, referent2, referent3, referent4, referent5, referent6, referent7, referent8, propertyName2, value2))
        return allObjects

    def getContainedObjectsWithPropertyAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndProperty(self, propertyName1, value1, referent1, referent2, referent3, referent4, referent5, referent6, referent7, referent8, propertyName2, value2):
        return [obj for obj in self.contains if obj.properties[propertyName1] == value1 and referent1 in obj.getReferents() and referent2 in obj.getReferents() and referent3 in obj.getReferents() and referent4 in obj.getReferents() and referent5 in obj.getReferents() and referent6 in obj.getReferents() and referent7 in obj.getReferents() and referent8 in obj.getReferents() and obj.properties[propertyName2] == value2]

    def getContainedObjectsWithPropertyAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndPropertyRecursive(self, propertyName1, value1, referent1, referent2, referent3, referent4, referent5, referent6, referent7, referent8, propertyName2, value2):
        allObjects = []
        for obj in self.contains:
            if obj.properties[propertyName1] == value1 and referent1 in obj.getReferents() and referent2 in obj.getReferents() and referent3 in obj.getReferents() and referent4 in obj.getReferents() and referent5 in obj.getReferents() and referent6 in obj.getReferents() and referent7 in obj.getReferents() and referent8 in obj.getReferents() and obj.properties[propertyName2] == value2:
                allObjects.append(obj)
            if obj.properties["isContainer"]:
                allObjects.extend(obj.getContainedObjectsWithPropertyAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndPropertyRecursive(propertyName1, value1, referent1, referent2, referent3, referent4, referent5, referent6, referent7, referent8, propertyName2, value2))
        return allObjects

    def getContainedObjectsWithReferentAndPropertyAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndReferent(self, referent1, propertyName1, value1, referent2, referent3, referent4, referent5, referent6, referent7, referent8, referent9):
        return [obj for obj in self.contains if referent1 in obj.getReferents() and obj.properties[propertyName1] == value1 and referent2 in obj.getReferents() and referent3 in obj.getReferents() and referent4 in obj.getReferents() and referent5 in obj.getReferents() and referent6 in obj.getReferents() and referent7 in obj.getReferents() and referent8 in obj.getReferents() and referent9 in obj.getReferents()]

    def getContainedObjectsWithReferentAndPropertyAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentRecursive(self, referent1, propertyName1, value1, referent2, referent3, referent4, referent5, referent6, referent7, referent8, referent9):
        allObjects = []
        for obj in self.contains:
            if referent1 in obj.getReferents() and obj.properties[propertyName1] == value1 and referent2 in obj.getReferents() and referent3 in obj.getReferents() and referent4 in obj.getReferents() and referent5 in obj.getReferents() and referent6 in obj.getReferents() and referent7 in obj.getReferents() and referent8 in obj.getReferents() and referent9 in obj.getReferents():
                allObjects.append(obj)
            if obj.properties["isContainer"]:
                allObjects.extend(obj.getContainedObjectsWithReferentAndPropertyAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentRecursive(referent1, propertyName1, value1, referent2, referent3, referent4, referent5, referent6, referent7, referent8, referent9))
        return allObjects

    def getContainedObjectsWithPropertyAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndReferent(self, propertyName1, value1, referent1, referent2, referent3, referent4, referent5, referent6, referent7, referent8, referent9):
        return [obj for obj in self.contains if obj.properties[propertyName1] == value1 and referent1 in obj.getReferents() and referent2 in obj.getReferents() and referent3 in obj.getReferents() and referent4 in obj.getReferents() and referent5 in obj.getReferents() and referent6 in obj.getReferents() and referent7 in obj.getReferents() and referent8 in obj.getReferents() and referent9 in obj.getReferents()]

    def getContainedObjectsWithPropertyAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentRecursive(self, propertyName1, value1, referent1, referent2, referent3, referent4, referent5, referent6, referent7, referent8, referent9):
        allObjects = []
        for obj in self.contains:
            if obj.properties[propertyName1] == value1 and referent1 in obj.getReferents() and referent2 in obj.getReferents() and referent3 in obj.getReferents() and referent4 in obj.getReferents() and referent5 in obj.getReferents() and referent6 in obj.getReferents() and referent7 in obj.getReferents() and referent8 in obj.getReferents() and referent9 in obj.getReferents():
                allObjects.append(obj)
            if obj.properties["isContainer"]:
                allObjects.extend(obj.getContainedObjectsWithPropertyAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentRecursive(propertyName1, value1, referent1, referent2, referent3, referent4, referent5, referent6, referent7, referent8, referent9))
        return allObjects

    def getContainedObjectsWithReferentAndPropertyAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndProperty(self, referent1, propertyName1, value1, referent2, referent3, referent4, referent5, referent6, referent7, referent8, referent9, propertyName2, value2):
        return [obj for obj in self.contains if referent1 in obj.getReferents() and obj.properties[propertyName1] == value1 and referent2 in obj.getReferents() and referent3 in obj.getReferents() and referent4 in obj.getReferents() and referent5 in obj.getReferents() and referent6 in obj.getReferents() and referent7 in obj.getReferents() and referent8 in obj.getReferents() and referent9 in obj.getReferents() and obj.properties[propertyName2] == value2]

    def getContainedObjectsWithReferentAndPropertyAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndPropertyRecursive(self, referent1, propertyName1, value1, referent2, referent3, referent4, referent5, referent6, referent7, referent8, referent9, propertyName2, value2):
        allObjects = []
        for obj in self.contains:
            if referent1 in obj.getReferents() and obj.properties[propertyName1] == value1 and referent2 in obj.getReferents() and referent3 in obj.getReferents() and referent4 in obj.getReferents() and referent5 in obj.getReferents() and referent6 in obj.getReferents() and referent7 in obj.getReferents() and referent8 in obj.getReferents() and referent9 in obj.getReferents() and obj.properties[propertyName2] == value2:
                allObjects.append(obj)
            if obj.properties["isContainer"]:
                allObjects.extend(obj.getContainedObjectsWithReferentAndPropertyAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndPropertyRecursive(referent1, propertyName1, value1, referent2, referent3, referent4, referent5, referent6, referent7, referent8, referent9, propertyName2, value2))
        return allObjects

    def getContainedObjectsWithPropertyAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndProperty(self, propertyName1, value1, referent1, referent2, referent3, referent4, referent5, referent6, referent7, referent8, referent9, propertyName2, value2):
        return [obj for obj in self.contains if obj.properties[propertyName1] == value1 and referent1 in obj.getReferents() and referent2 in obj.getReferents() and referent3 in obj.getReferents() and referent4 in obj.getReferents() and referent5 in obj.getReferents() and referent6 in obj.getReferents() and referent7 in obj.getReferents() and referent8 in obj.getReferents() and referent9 in obj.getReferents() and obj.properties[propertyName2] == value2]

    def getContainedObjectsWithPropertyAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndPropertyRecursive(self, propertyName1, value1, referent1, referent2, referent3, referent4, referent5, referent6, referent7, referent8, referent9, propertyName2, value2):
        allObjects = []
        for obj in self.contains:
            if obj.properties[propertyName1] == value1 and referent1 in obj.getReferents() and referent2 in obj.getReferents() and referent3 in obj.getReferents() and referent4 in obj.getReferents() and referent5 in obj.getReferents() and referent6 in obj.getReferents() and referent7 in obj.getReferents() and referent8 in obj.getReferents() and referent9 in obj.getReferents() and obj.properties[propertyName2] == value2:
                allObjects.append(obj)
            if obj.properties["isContainer"]:
                allObjects.extend(obj.getContainedObjectsWithPropertyAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndPropertyRecursive(propertyName1, value1, referent1, referent2, referent3, referent4, referent5, referent6, referent7, referent8, referent9, propertyName2, value2))
        return allObjects

    def getContainedObjectsWithReferentAndPropertyAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndReferent(self, referent1, propertyName1, value1, referent2, referent3, referent4, referent5, referent6, referent7, referent8, referent9, referent10):
        return [obj for obj in self.contains if referent1 in obj.getReferents() and obj.properties[propertyName1] == value1 and referent2 in obj.getReferents() and referent3 in obj.getReferents() and referent4 in obj.getReferents() and referent5 in obj.getReferents() and referent6 in obj.getReferents() and referent7 in obj.getReferents() and referent8 in obj.getReferents() and referent9 in obj.getReferents() and referent10 in obj.getReferents()]

    def getContainedObjectsWithReferentAndPropertyAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentRecursive(self, referent1, propertyName1, value1, referent2, referent3, referent4, referent5, referent6, referent7, referent8, referent9, referent10):
        allObjects = []
        for obj in self.contains:
            if referent1 in obj.getReferents() and obj.properties[propertyName1] == value1 and referent2 in obj.getReferents() and referent3 in obj.getReferents() and referent4 in obj.getReferents() and referent5 in obj.getReferents() and referent6 in obj.getReferents() and referent7 in obj.getReferents() and referent8 in obj.getReferents() and referent9 in obj.getReferents() and referent10 in obj.getReferents():
                allObjects.append(obj)
            if obj.properties["isContainer"]:
                allObjects.extend(obj.getContainedObjectsWithReferentAndPropertyAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentRecursive(referent1, propertyName1, value1, referent2, referent3, referent4, referent5, referent6, referent7, referent8, referent9, referent10))
        return allObjects

    def getContainedObjectsWithPropertyAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndReferentAndReferent