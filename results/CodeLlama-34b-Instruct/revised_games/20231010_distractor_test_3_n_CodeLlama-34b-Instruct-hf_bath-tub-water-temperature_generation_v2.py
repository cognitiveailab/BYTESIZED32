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

    def getContainedObjectsWithReferentAndPropertyAndReferent(self, referent1, propertyName, value, referent2):
        return [obj for obj in self.contains if referent1 in obj.getReferents() and obj.properties[propertyName] == value and referent2 in obj.getReferents()]

    def getContainedObjectsWithReferentAndPropertyAndReferentRecursive(self, referent1, propertyName, value, referent2):
        allObjects = []
        for obj in self.contains:
            if referent1 in obj.getReferents() and obj.properties[propertyName] == value and referent2 in obj.getReferents():
                allObjects.append(obj)
            if obj.properties["isContainer"]:
                allObjects.extend(obj.getContainedObjectsWithReferentAndPropertyAndReferentRecursive(referent1, propertyName, value, referent2))
        return allObjects

    def getContainedObjectsWithPropertyAndReferentAndProperty(self, propertyName1, value1, referent, propertyName2, value2):
        return [obj for obj in self.contains if obj.properties[propertyName1] == value1 and referent in obj.getReferents() and obj.properties[propertyName2] == value2]

    def getContainedObjectsWithPropertyAndReferentAndPropertyRecursive(self, propertyName1, value1, referent, propertyName2, value2):
        allObjects = []
        for obj in self.contains:
            if obj.properties[propertyName1] == value1 and referent in obj.getReferents() and obj.properties[propertyName2] == value2:
                allObjects.append(obj)
            if obj.properties["isContainer"]:
                allObjects.extend(obj.getContainedObjectsWithPropertyAndReferentAndPropertyRecursive(propertyName1, value1, referent, propertyName2, value2))
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

    def getContainedObjectsWithPropertyAndReferentAndPropertyAndReferent(self, propertyName1, value1, referent1, propertyName2, value2, referent2):
        return [obj for obj in self.contains if obj.properties[propertyName1] == value1 and referent1 in obj.getReferents() and obj.properties[propertyName2] == value2 and referent2 in obj.getReferents()]

    def getContainedObjectsWithPropertyAndReferentAndPropertyAndReferentRecursive(self, propertyName1, value1, referent1, propertyName2, value2, referent2):
        allObjects = []
        for obj in self.contains:
            if obj.properties[propertyName1] == value1 and referent1 in obj.getReferents() and obj.properties[propertyName2] == value2 and referent2 in obj.getReferents():
                allObjects.append(obj)
            if obj.properties["isContainer"]:
                allObjects.extend(obj.getContainedObjectsWithPropertyAndReferentAndPropertyAndReferentRecursive(propertyName1, value1, referent1, propertyName2, value2, referent2))
        return allObjects

    def getContainedObjectsWithReferentAndPropertyAndReferentAndPropertyAndReferent(self, referent1, propertyName1, value1, referent2, propertyName2, value2, referent3):
        return [obj for obj in self.contains if referent1 in obj.getReferents() and obj.properties[propertyName1] == value1 and referent2 in obj.getReferents() and obj.properties[propertyName2] == value2 and referent3 in obj.getReferents()]

    def getContainedObjectsWithReferentAndPropertyAndReferentAndPropertyAndReferentRecursive(self, referent1, propertyName1, value1, referent2, propertyName2, value2, referent3):
        allObjects = []
        for obj in self.contains:
            if referent1 in obj.getReferents() and obj.properties[propertyName1] == value1 and referent2 in obj.getReferents() and obj.properties[propertyName2] == value2 and referent3 in obj.getReferents():
                allObjects.append(obj)
            if obj.properties["isContainer"]:
                allObjects.extend(obj.getContainedObjectsWithReferentAndPropertyAndReferentAndPropertyAndReferentRecursive(referent1, propertyName1, value1, referent2, propertyName2, value2, referent3))
        return allObjects

    def getContainedObjectsWithPropertyAndReferentAndPropertyAndReferentAndProperty(self, propertyName1, value1, referent1, propertyName2, value2, referent2, propertyName3, value3):
        return [obj for obj in self.contains if obj.properties[propertyName1] == value1 and referent1 in obj.getReferents() and obj.properties[propertyName2] == value2 and referent2 in obj.getReferents() and obj.properties[propertyName3] == value3]

    def getContainedObjectsWithPropertyAndReferentAndPropertyAndReferentAndPropertyRecursive(self, propertyName1, value1, referent1, propertyName2, value2, referent2, propertyName3, value3):
        allObjects = []
        for obj in self.contains:
            if obj.properties[propertyName1] == value1 and referent1 in obj.getReferents() and obj.properties[propertyName2] == value2 and referent2 in obj.getReferents() and obj.properties[propertyName3] == value3:
                allObjects.append(obj)
            if obj.properties["isContainer"]:
                allObjects.extend(obj.getContainedObjectsWithPropertyAndReferentAndPropertyAndReferentAndPropertyRecursive(propertyName1, value1, referent1, propertyName2, value2, referent2, propertyName3, value3))
        return allObjects

    def getContainedObjectsWithReferentAndPropertyAndReferentAndPropertyAndReferentAndProperty(self, referent1, propertyName1, value1, referent2, propertyName2, value2, referent3, propertyName3, value3):
        return [obj for obj in self.contains if referent1 in obj.getReferents() and obj.properties[propertyName1] == value1 and referent2 in obj.getReferents() and obj.properties[propertyName2] == value2 and referent3 in obj.getReferents() and obj.properties[propertyName3] == value3]

    def getContainedObjectsWithReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyRecursive(self, referent1, propertyName1, value1, referent2, propertyName2, value2, referent3, propertyName3, value3):
        allObjects = []
        for obj in self.contains:
            if referent1 in obj.getReferents() and obj.properties[propertyName1] == value1 and referent2 in obj.getReferents() and obj.properties[propertyName2] == value2 and referent3 in obj.getReferents() and obj.properties[propertyName3] == value3:
                allObjects.append(obj)
            if obj.properties["isContainer"]:
                allObjects.extend(obj.getContainedObjectsWithReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyRecursive(referent1, propertyName1, value1, referent2, propertyName2, value2, referent3, propertyName3, value3))
        return allObjects

    def getContainedObjectsWithPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferent(self, propertyName1, value1, referent1, propertyName2, value2, referent2, propertyName3, value3, referent3):
        return [obj for obj in self.contains if obj.properties[propertyName1] == value1 and referent1 in obj.getReferents() and obj.properties[propertyName2] == value2 and referent2 in obj.getReferents() and obj.properties[propertyName3] == value3 and referent3 in obj.getReferents()]

    def getContainedObjectsWithPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentRecursive(self, propertyName1, value1, referent1, propertyName2, value2, referent2, propertyName3, value3, referent3):
        allObjects = []
        for obj in self.contains:
            if obj.properties[propertyName1] == value1 and referent1 in obj.getReferents() and obj.properties[propertyName2] == value2 and referent2 in obj.getReferents() and obj.properties[propertyName3] == value3 and referent3 in obj.getReferents():
                allObjects.append(obj)
            if obj.properties["isContainer"]:
                allObjects.extend(obj.getContainedObjectsWithPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentRecursive(propertyName1, value1, referent1, propertyName2, value2, referent2, propertyName3, value3, referent3))
        return allObjects

    def getContainedObjectsWithReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferent(self, referent1, propertyName1, value1, referent2, propertyName2, value2, referent3, propertyName3, value3, referent4):
        return [obj for obj in self.contains if referent1 in obj.getReferents() and obj.properties[propertyName1] == value1 and referent2 in obj.getReferents() and obj.properties[propertyName2] == value2 and referent3 in obj.getReferents() and obj.properties[propertyName3] == value3 and referent4 in obj.getReferents()]

    def getContainedObjectsWithReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentRecursive(self, referent1, propertyName1, value1, referent2, propertyName2, value2, referent3, propertyName3, value3, referent4):
        allObjects = []
        for obj in self.contains:
            if referent1 in obj.getReferents() and obj.properties[propertyName1] == value1 and referent2 in obj.getReferents() and obj.properties[propertyName2] == value2 and referent3 in obj.getReferents() and obj.properties[propertyName3] == value3 and referent4 in obj.getReferents():
                allObjects.append(obj)
            if obj.properties["isContainer"]:
                allObjects.extend(obj.getContainedObjectsWithReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentRecursive(referent1, propertyName1, value1, referent2, propertyName2, value2, referent3, propertyName3, value3, referent4))
        return allObjects

    def getContainedObjectsWithPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndProperty(self, propertyName1, value1, referent1, propertyName2, value2, referent2, propertyName3, value3, referent3, propertyName4, value4):
        return [obj for obj in self.contains if obj.properties[propertyName1] == value1 and referent1 in obj.getReferents() and obj.properties[propertyName2] == value2 and referent2 in obj.getReferents() and obj.properties[propertyName3] == value3 and referent3 in obj.getReferents() and obj.properties[propertyName4] == value4]

    def getContainedObjectsWithPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyRecursive(self, propertyName1, value1, referent1, propertyName2, value2, referent2, propertyName3, value3, referent3, propertyName4, value4):
        allObjects = []
        for obj in self.contains:
            if obj.properties[propertyName1] == value1 and referent1 in obj.getReferents() and obj.properties[propertyName2] == value2 and referent2 in obj.getReferents() and obj.properties[propertyName3] == value3 and referent3 in obj.getReferents() and obj.properties[propertyName4] == value4:
                allObjects.append(obj)
            if obj.properties["isContainer"]:
                allObjects.extend(obj.getContainedObjectsWithPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyRecursive(propertyName1, value1, referent1, propertyName2, value2, referent2, propertyName3, value3, referent3, propertyName4, value4))
        return allObjects

    def getContainedObjectsWithReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndProperty(self, referent1, propertyName1, value1, referent2, propertyName2, value2, referent3, propertyName3, value3, referent4, propertyName4, value4):
        return [obj for obj in self.contains if referent1 in obj.getReferents() and obj.properties[propertyName1] == value1 and referent2 in obj.getReferents() and obj.properties[propertyName2] == value2 and referent3 in obj.getReferents() and obj.properties[propertyName3] == value3 and referent4 in obj.getReferents() and obj.properties[propertyName4] == value4]

    def getContainedObjectsWithReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyRecursive(self, referent1, propertyName1, value1, referent2, propertyName2, value2, referent3, propertyName3, value3, referent4, propertyName4, value4):
        allObjects = []
        for obj in self.contains:
            if referent1 in obj.getReferents() and obj.properties[propertyName1] == value1 and referent2 in obj.getReferents() and obj.properties[propertyName2] == value2 and referent3 in obj.getReferents() and obj.properties[propertyName3] == value3 and referent4 in obj.getReferents() and obj.properties[propertyName4] == value4:
                allObjects.append(obj)
            if obj.properties["isContainer"]:
                allObjects.extend(obj.getContainedObjectsWithReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyRecursive(referent1, propertyName1, value1, referent2, propertyName2, value2, referent3, propertyName3, value3, referent4, propertyName4, value4))
        return allObjects

    def getContainedObjectsWithPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferent(self, propertyName1, value1, referent1, propertyName2, value2, referent2, propertyName3, value3, referent3, propertyName4, value4, referent4):
        return [obj for obj in self.contains if obj.properties[propertyName1] == value1 and referent1 in obj.getReferents() and obj.properties[propertyName2] == value2 and referent2 in obj.getReferents() and obj.properties[propertyName3] == value3 and referent3 in obj.getReferents() and obj.properties[propertyName4] == value4 and referent4 in obj.getReferents()]

    def getContainedObjectsWithPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentRecursive(self, propertyName1, value1, referent1, propertyName2, value2, referent2, propertyName3, value3, referent3, propertyName4, value4, referent4):
        allObjects = []
        for obj in self.contains:
            if obj.properties[propertyName1] == value1 and referent1 in obj.getReferents() and obj.properties[propertyName2] == value2 and referent2 in obj.getReferents() and obj.properties[propertyName3] == value3 and referent3 in obj.getReferents() and obj.properties[propertyName4] == value4 and referent4 in obj.getReferents():
                allObjects.append(obj)
            if obj.properties["isContainer"]:
                allObjects.extend(obj.getContainedObjectsWithPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentRecursive(propertyName1, value1, referent1, propertyName2, value2, referent2, propertyName3, value3, referent3, propertyName4, value4, referent4))
        return allObjects

    def getContainedObjectsWithReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferent(self, referent1, propertyName1, value1, referent2, propertyName2, value2, referent3, propertyName3, value3, referent4, propertyName4, value4, referent5):
        return [obj for obj in self.contains if referent1 in obj.getReferents() and obj.properties[propertyName1] == value1 and referent2 in obj.getReferents() and obj.properties[propertyName2] == value2 and referent3 in obj.getReferents() and obj.properties[propertyName3] == value3 and referent4 in obj.getReferents() and obj.properties[propertyName4] == value4 and referent5 in obj.getReferents()]

    def getContainedObjectsWithReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentRecursive(self, referent1, propertyName1, value1, referent2, propertyName2, value2, referent3, propertyName3, value3, referent4, propertyName4, value4, referent5):
        allObjects = []
        for obj in self.contains:
            if referent1 in obj.getReferents() and obj.properties[propertyName1] == value1 and referent2 in obj.getReferents() and obj.properties[propertyName2] == value2 and referent3 in obj.getReferents() and obj.properties[propertyName3] == value3 and referent4 in obj.getReferents() and obj.properties[propertyName4] == value4 and referent5 in obj.getReferents():
                allObjects.append(obj)
            if obj.properties["isContainer"]:
                allObjects.extend(obj.getContainedObjectsWithReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentRecursive(referent1, propertyName1, value1, referent2, propertyName2, value2, referent3, propertyName3, value3, referent4, propertyName4, value4, referent5))
        return allObjects

    def getContainedObjectsWithPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndProperty(self, propertyName1, value1, referent1, propertyName2, value2, referent2, propertyName3, value3, referent3, propertyName4, value4, referent4, propertyName5, value5):
        return [obj for obj in self.contains if obj.properties[propertyName1] == value1 and referent1 in obj.getReferents() and obj.properties[propertyName2] == value2 and referent2 in obj.getReferents() and obj.properties[propertyName3] == value3 and referent3 in obj.getReferents() and obj.properties[propertyName4] == value4 and referent4 in obj.getReferents() and obj.properties[propertyName5] == value5]

    def getContainedObjectsWithPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyRecursive(self, propertyName1, value1, referent1, propertyName2, value2, referent2, propertyName3, value3, referent3, propertyName4, value4, referent4, propertyName5, value5):
        allObjects = []
        for obj in self.contains:
            if obj.properties[propertyName1] == value1 and referent1 in obj.getReferents() and obj.properties[propertyName2] == value2 and referent2 in obj.getReferents() and obj.properties[propertyName3] == value3 and referent3 in obj.getReferents() and obj.properties[propertyName4] == value4 and referent4 in obj.getReferents() and obj.properties[propertyName5] == value5:
                allObjects.append(obj)
            if obj.properties["isContainer"]:
                allObjects.extend(obj.getContainedObjectsWithPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyRecursive(propertyName1, value1, referent1, propertyName2, value2, referent2, propertyName3, value3, referent3, propertyName4, value4, referent4, propertyName5, value5))
        return allObjects

    def getContainedObjectsWithReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndProperty(self, referent1, propertyName1, value1, referent2, propertyName2, value2, referent3, propertyName3, value3, referent4, propertyName4, value4, referent5, propertyName5, value5):
        return [obj for obj in self.contains if referent1 in obj.getReferents() and obj.properties[propertyName1] == value1 and referent2 in obj.getReferents() and obj.properties[propertyName2] == value2 and referent3 in obj.getReferents() and obj.properties[propertyName3] == value3 and referent4 in obj.getReferents() and obj.properties[propertyName4] == value4 and referent5 in obj.getReferents() and obj.properties[propertyName5] == value5]

    def getContainedObjectsWithReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyRecursive(self, referent1, propertyName1, value1, referent2, propertyName2, value2, referent3, propertyName3, value3, referent4, propertyName4, value4, referent5, propertyName5, value5):
        allObjects = []
        for obj in self.contains:
            if referent1 in obj.getReferents() and obj.properties[propertyName1] == value1 and referent2 in obj.getReferents() and obj.properties[propertyName2] == value2 and referent3 in obj.getReferents() and obj.properties[propertyName3] == value3 and referent4 in obj.getReferents() and obj.properties[propertyName4] == value4 and referent5 in obj.getReferents() and obj.properties[propertyName5] == value5:
                allObjects.append(obj)
            if obj.properties["isContainer"]:
                allObjects.extend(obj.getContainedObjectsWithReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyRecursive(referent1, propertyName1, value1, referent2, propertyName2, value2, referent3, propertyName3, value3, referent4, propertyName4, value4, referent5, propertyName5, value5))
        return allObjects

    def getContainedObjectsWithPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferent(self, propertyName1, value1, referent1, propertyName2, value2, referent2, propertyName3, value3, referent3, propertyName4, value4, referent4, propertyName5, value5, referent5):
        return [obj for obj in self.contains if obj.properties[propertyName1] == value1 and referent1 in obj.getReferents() and obj.properties[propertyName2] == value2 and referent2 in obj.getReferents() and obj.properties[propertyName3] == value3 and referent3 in obj.getReferents() and obj.properties[propertyName4] == value4 and referent4 in obj.getReferents() and obj.properties[propertyName5] == value5 and referent5 in obj.getReferents()]

    def getContainedObjectsWithPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentRecursive(self, propertyName1, value1, referent1, propertyName2, value2, referent2, propertyName3, value3, referent3, propertyName4, value4, referent4, propertyName5, value5, referent5):
        allObjects = []
        for obj in self.contains:
            if obj.properties[propertyName1] == value1 and referent1 in obj.getReferents() and obj.properties[propertyName2] == value2 and referent2 in obj.getReferents() and obj.properties[propertyName3] == value3 and referent3 in obj.getReferents() and obj.properties[propertyName4] == value4 and referent4 in obj.getReferents() and obj.properties[propertyName5] == value5 and referent5 in obj.getReferents():
                allObjects.append(obj)
            if obj.properties["isContainer"]:
                allObjects.extend(obj.getContainedObjectsWithPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentRecursive(propertyName1, value1, referent1, propertyName2, value2, referent2, propertyName3, value3, referent3, propertyName4, value4, referent4, propertyName5, value5, referent5))
        return allObjects

    def getContainedObjectsWithReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferent(self, referent1, propertyName1, value1, referent2, propertyName2, value2, referent3, propertyName3, value3, referent4, propertyName4, value4, referent5, propertyName5, value5, referent6):
        return [obj for obj in self.contains if referent1 in obj.getReferents() and obj.properties[propertyName1] == value1 and referent2 in obj.getReferents() and obj.properties[propertyName2] == value2 and referent3 in obj.getReferents() and obj.properties[propertyName3] == value3 and referent4 in obj.getReferents() and obj.properties[propertyName4] == value4 and referent5 in obj.getReferents() and obj.properties[propertyName5] == value5 and referent6 in obj.getReferents()]

    def getContainedObjectsWithReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentRecursive(self, referent1, propertyName1, value1, referent2, propertyName2, value2, referent3, propertyName3, value3, referent4, propertyName4, value4, referent5, propertyName5, value5, referent6):
        allObjects = []
        for obj in self.contains:
            if referent1 in obj.getReferents() and obj.properties[propertyName1] == value1 and referent2 in obj.getReferents() and obj.properties[propertyName2] == value2 and referent3 in obj.getReferents() and obj.properties[propertyName3] == value3 and referent4 in obj.getReferents() and obj.properties[propertyName4] == value4 and referent5 in obj.getReferents() and obj.properties[propertyName5] == value5 and referent6 in obj.getReferents():
                allObjects.append(obj)
            if obj.properties["isContainer"]:
                allObjects.extend(obj.getContainedObjectsWithReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentRecursive(referent1, propertyName1, value1, referent2, propertyName2, value2, referent3, propertyName3, value3, referent4, propertyName4, value4, referent5, propertyName5, value5, referent6))
        return allObjects

    def getContainedObjectsWithPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndProperty(self, propertyName1, value1, referent1, propertyName2, value2, referent2, propertyName3, value3, referent3, propertyName4, value4, referent4, propertyName5, value5, referent5, propertyName6, value6):
        return [obj for obj in self.contains if obj.properties[propertyName1] == value1 and referent1 in obj.getReferents() and obj.properties[propertyName2] == value2 and referent2 in obj.getReferents() and obj.properties[propertyName3] == value3 and referent3 in obj.getReferents() and obj.properties[propertyName4] == value4 and referent4 in obj.getReferents() and obj.properties[propertyName5] == value5 and referent5 in obj.getReferents() and obj.properties[propertyName6] == value6]

    def getContainedObjectsWithPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyRecursive(self, propertyName1, value1, referent1, propertyName2, value2, referent2, propertyName3, value3, referent3, propertyName4, value4, referent4, propertyName5, value5, referent5, propertyName6, value6):
        allObjects = []
        for obj in self.contains:
            if obj.properties[propertyName1] == value1 and referent1 in obj.getReferents() and obj.properties[propertyName2] == value2 and referent2 in obj.getReferents() and obj.properties[propertyName3] == value3 and referent3 in obj.getReferents() and obj.properties[propertyName4] == value4 and referent4 in obj.getReferents() and obj.properties[propertyName5] == value5 and referent5 in obj.getReferents() and obj.properties[propertyName6] == value6:
                allObjects.append(obj)
            if obj.properties["isContainer"]:
                allObjects.extend(obj.getContainedObjectsWithPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyRecursive(propertyName1, value1, referent1, propertyName2, value2, referent2, propertyName3, value3, referent3, propertyName4, value4, referent4, propertyName5, value5, referent5, propertyName6, value6))
        return allObjects

    def getContainedObjectsWithReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndProperty(self, referent1, propertyName1, value1, referent2, propertyName2, value2, referent3, propertyName3, value3, referent4, propertyName4, value4, referent5, propertyName5, value5, referent6, propertyName6, value6):
        return [obj for obj in self.contains if referent1 in obj.getReferents() and obj.properties[propertyName1] == value1 and referent2 in obj.getReferents() and obj.properties[propertyName2] == value2 and referent3 in obj.getReferents() and obj.properties[propertyName3] == value3 and referent4 in obj.getReferents() and obj.properties[propertyName4] == value4 and referent5 in obj.getReferents() and obj.properties[propertyName5] == value5 and referent6 in obj.getReferents() and obj.properties[propertyName6] == value6]

    def getContainedObjectsWithReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyRecursive(self, referent1, propertyName1, value1, referent2, propertyName2, value2, referent3, propertyName3, value3, referent4, propertyName4, value4, referent5, propertyName5, value5, referent6, propertyName6, value6):
        allObjects = []
        for obj in self.contains:
            if referent1 in obj.getReferents() and obj.properties[propertyName1] == value1 and referent2 in obj.getReferents() and obj.properties[propertyName2] == value2 and referent3 in obj.getReferents() and obj.properties[propertyName3] == value3 and referent4 in obj.getReferents() and obj.properties[propertyName4] == value4 and referent5 in obj.getReferents() and obj.properties[propertyName5] == value5 and referent6 in obj.getReferents() and obj.properties[propertyName6] == value6:
                allObjects.append(obj)
            if obj.properties["isContainer"]:
                allObjects.extend(obj.getContainedObjectsWithReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyRecursive(referent1, propertyName1, value1, referent2, propertyName2, value2, referent3, propertyName3, value3, referent4, propertyName4, value4, referent5, propertyName5, value5, referent6, propertyName6, value6))
        return allObjects

    def getContainedObjectsWithPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferent(self, propertyName1, value1, referent1, propertyName2, value2, referent2, propertyName3, value3, referent3, propertyName4, value4, referent4, propertyName5, value5, referent5, propertyName6, value6, referent6):
        return [obj for obj in self.contains if obj.properties[propertyName1] == value1 and referent1 in obj.getReferents() and obj.properties[propertyName2] == value2 and referent2 in obj.getReferents() and obj.properties[propertyName3] == value3 and referent3 in obj.getReferents() and obj.properties[propertyName4] == value4 and referent4 in obj.getReferents() and obj.properties[propertyName5] == value5 and referent5 in obj.getReferents() and obj.properties[propertyName6] == value6 and referent6 in obj.getReferents()]

    def getContainedObjectsWithPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentRecursive(self, propertyName1, value1, referent1, propertyName2, value2, referent2, propertyName3, value3, referent3, propertyName4, value4, referent4, propertyName5, value5, referent5, propertyName6, value6, referent6):
        allObjects = []
        for obj in self.contains:
            if obj.properties[propertyName1] == value1 and referent1 in obj.getReferents() and obj.properties[propertyName2] == value2 and referent2 in obj.getReferents() and obj.properties[propertyName3] == value3 and referent3 in obj.getReferents() and obj.properties[propertyName4] == value4 and referent4 in obj.getReferents() and obj.properties[propertyName5] == value5 and referent5 in obj.getReferents() and obj.properties[propertyName6] == value6 and referent6 in obj.getReferents():
                allObjects.append(obj)
            if obj.properties["isContainer"]:
                allObjects.extend(obj.getContainedObjectsWithPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentRecursive(propertyName1, value1, referent1, propertyName2, value2, referent2, propertyName3, value3, referent3, propertyName4, value4, referent4, propertyName5, value5, referent5, propertyName6, value6, referent6))
        return allObjects

    def getContainedObjectsWithReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferent(self, referent1, propertyName1, value1, referent2, propertyName2, value2, referent3, propertyName3, value3, referent4, propertyName4, value4, referent5, propertyName5, value5, referent6, propertyName6, value6, referent7):
        return [obj for obj in self.contains if referent1 in obj.getReferents() and obj.properties[propertyName1] == value1 and referent2 in obj.getReferents() and obj.properties[propertyName2] == value2 and referent3 in obj.getReferents() and obj.properties[propertyName3] == value3 and referent4 in obj.getReferents() and obj.properties[propertyName4] == value4 and referent5 in obj.getReferents() and obj.properties[propertyName5] == value5 and referent6 in obj.getReferents() and obj.properties[propertyName6] == value6 and referent7 in obj.getReferents()]

    def getContainedObjectsWithReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentRecursive(self, referent1, propertyName1, value1, referent2, propertyName2, value2, referent3, propertyName3, value3, referent4, propertyName4, value4, referent5, propertyName5, value5, referent6, propertyName6, value6, referent7):
        allObjects = []
        for obj in self.contains:
            if referent1 in obj.getReferents() and obj.properties[propertyName1] == value1 and referent2 in obj.getReferents() and obj.properties[propertyName2] == value2 and referent3 in obj.getReferents() and obj.properties[propertyName3] == value3 and referent4 in obj.getReferents() and obj.properties[propertyName4] == value4 and referent5 in obj.getReferents() and obj.properties[propertyName5] == value5 and referent6 in obj.getReferents() and obj.properties[propertyName6] == value6 and referent7 in obj.getReferents():
                allObjects.append(obj)
            if obj.properties["isContainer"]:
                allObjects.extend(obj.getContainedObjectsWithReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentRecursive(referent1, propertyName1, value1, referent2, propertyName2, value2, referent3, propertyName3, value3, referent4, propertyName4, value4, referent5, propertyName5, value5, referent6, propertyName6, value6, referent7))
        return allObjects

    def getContainedObjectsWithPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndProperty(self, propertyName1, value1, referent1, propertyName2, value2, referent2, propertyName3, value3, referent3, propertyName4, value4, referent4, propertyName5, value5, referent5, propertyName6, value6, referent6, propertyName7, value7):
        return [obj for obj in self.contains if obj.properties[propertyName1] == value1 and referent1 in obj.getReferents() and obj.properties[propertyName2] == value2 and referent2 in obj.getReferents() and obj.properties[propertyName3] == value3 and referent3 in obj.getReferents() and obj.properties[propertyName4] == value4 and referent4 in obj.getReferents() and obj.properties[propertyName5] == value5 and referent5 in obj.getReferents() and obj.properties[propertyName6] == value6 and referent6 in obj.getReferents() and obj.properties[propertyName7] == value7]

    def getContainedObjectsWithPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyRecursive(self, propertyName1, value1, referent1, propertyName2, value2, referent2, propertyName3, value3, referent3, propertyName4, value4, referent4, propertyName5, value5, referent5, propertyName6, value6, referent6, propertyName7, value7):
        allObjects = []
        for obj in self.contains:
            if obj.properties[propertyName1] == value1 and referent1 in obj.getReferents() and obj.properties[propertyName2] == value2 and referent2 in obj.getReferents() and obj.properties[propertyName3] == value3 and referent3 in obj.getReferents() and obj.properties[propertyName4] == value4 and referent4 in obj.getReferents() and obj.properties[propertyName5] == value5 and referent5 in obj.getReferents() and obj.properties[propertyName6] == value6 and referent6 in obj.getReferents() and obj.properties[propertyName7] == value7:
                allObjects.append(obj)
            if obj.properties["isContainer"]:
                allObjects.extend(obj.getContainedObjectsWithPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyRecursive(propertyName1, value1, referent1, propertyName2, value2, referent2, propertyName3, value3, referent3, propertyName4, value4, referent4, propertyName5, value5, referent5, propertyName6, value6, referent6, propertyName7, value7))
        return allObjects

    def getContainedObjectsWithReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndProperty(self, referent1, propertyName1, value1, referent2, propertyName2, value2, referent3, propertyName3, value3, referent4, propertyName4, value4, referent5, propertyName5, value5, referent6, propertyName6, value6, referent7, propertyName7, value7):
        return [obj for obj in self.contains if referent1 in obj.getReferents() and obj.properties[propertyName1] == value1 and referent2 in obj.getReferents() and obj.properties[propertyName2] == value2 and referent3 in obj.getReferents() and obj.properties[propertyName3] == value3 and referent4 in obj.getReferents() and obj.properties[propertyName4] == value4 and referent5 in obj.getReferents() and obj.properties[propertyName5] == value5 and referent6 in obj.getReferents() and obj.properties[propertyName6] == value6 and referent7 in obj.getReferents() and obj.properties[propertyName7] == value7]

    def getContainedObjectsWithReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyRecursive(self, referent1, propertyName1, value1, referent2, propertyName2, value2, referent3, propertyName3, value3, referent4, propertyName4, value4, referent5, propertyName5, value5, referent6, propertyName6, value6, referent7, propertyName7, value7):
        allObjects = []
        for obj in self.contains:
            if referent1 in obj.getReferents() and obj.properties[propertyName1] == value1 and referent2 in obj.getReferents() and obj.properties[propertyName2] == value2 and referent3 in obj.getReferents() and obj.properties[propertyName3] == value3 and referent4 in obj.getReferents() and obj.properties[propertyName4] == value4 and referent5 in obj.getReferents() and obj.properties[propertyName5] == value5 and referent6 in obj.getReferents() and obj.properties[propertyName6] == value6 and referent7 in obj.getReferents() and obj.properties[propertyName7] == value7:
                allObjects.append(obj)
            if obj.properties["isContainer"]:
                allObjects.extend(obj.getContainedObjectsWithReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyRecursive(referent1, propertyName1, value1, referent2, propertyName2, value2, referent3, propertyName3, value3, referent4, propertyName4, value4, referent5, propertyName5, value5, referent6, propertyName6, value6, referent7, propertyName7, value7))
        return allObjects

    def getContainedObjectsWithPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferent(self, propertyName1, value1, referent1, propertyName2, value2, referent2, propertyName3, value3, referent3, propertyName4, value4, referent4, propertyName5, value5, referent5, propertyName6, value6, referent6, propertyName7, value7, referent7):
        return [obj for obj in self.contains if obj.properties[propertyName1] == value1 and referent1 in obj.getReferents() and obj.properties[propertyName2] == value2 and referent2 in obj.getReferents() and obj.properties[propertyName3] == value3 and referent3 in obj.getReferents() and obj.properties[propertyName4] == value4 and referent4 in obj.getReferents() and obj.properties[propertyName5] == value5 and referent5 in obj.getReferents() and obj.properties[propertyName6] == value6 and referent6 in obj.getReferents() and obj.properties[propertyName7] == value7 and referent7 in obj.getReferents()]

    def getContainedObjectsWithPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentRecursive(self, propertyName1, value1, referent1, propertyName2, value2, referent2, propertyName3, value3, referent3, propertyName4, value4, referent4, propertyName5, value5, referent5, propertyName6, value6, referent6, propertyName7, value7, referent7):
        allObjects = []
        for obj in self.contains:
            if obj.properties[propertyName1] == value1 and referent1 in obj.getReferents() and obj.properties[propertyName2] == value2 and referent2 in obj.getReferents() and obj.properties[propertyName3] == value3 and referent3 in obj.getReferents() and obj.properties[propertyName4] == value4 and referent4 in obj.getReferents() and obj.properties[propertyName5] == value5 and referent5 in obj.getReferents() and obj.properties[propertyName6] == value6 and referent6 in obj.getReferents() and obj.properties[propertyName7] == value7 and referent7 in obj.getReferents():
                allObjects.append(obj)
            if obj.properties["isContainer"]:
                allObjects.extend(obj.getContainedObjectsWithPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentRecursive(propertyName1, value1, referent1, propertyName2, value2, referent2, propertyName3, value3, referent3, propertyName4, value4, referent4, propertyName5, value5, referent5, propertyName6, value6, referent6, propertyName7, value7, referent7))
        return allObjects

    def getContainedObjectsWithReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferent(self, referent1, propertyName1, value1, referent2, propertyName2, value2, referent3, propertyName3, value3, referent4, propertyName4, value4, referent5, propertyName5, value5, referent6, propertyName6, value6, referent7, propertyName7, value7, referent8):
        return [obj for obj in self.contains if referent1 in obj.getReferents() and obj.properties[propertyName1] == value1 and referent2 in obj.getReferents() and obj.properties[propertyName2] == value2 and referent3 in obj.getReferents() and obj.properties[propertyName3] == value3 and referent4 in obj.getReferents() and obj.properties[propertyName4] == value4 and referent5 in obj.getReferents() and obj.properties[propertyName5] == value5 and referent6 in obj.getReferents() and obj.properties[propertyName6] == value6 and referent7 in obj.getReferents() and obj.properties[propertyName7] == value7 and referent8 in obj.getReferents()]

    def getContainedObjectsWithReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentRecursive(self, referent1, propertyName1, value1, referent2, propertyName2, value2, referent3, propertyName3, value3, referent4, propertyName4, value4, referent5, propertyName5, value5, referent6, propertyName6, value6, referent7, propertyName7, value7, referent8):
        allObjects = []
        for obj in self.contains:
            if referent1 in obj.getReferents() and obj.properties[propertyName1] == value1 and referent2 in obj.getReferents() and obj.properties[propertyName2] == value2 and referent3 in obj.getReferents() and obj.properties[propertyName3] == value3 and referent4 in obj.getReferents() and obj.properties[propertyName4] == value4 and referent5 in obj.getReferents() and obj.properties[propertyName5] == value5 and referent6 in obj.getReferents() and obj.properties[propertyName6] == value6 and referent7 in obj.getReferents() and obj.properties[propertyName7] == value7 and referent8 in obj.getReferents():
                allObjects.append(obj)
            if obj.properties["isContainer"]:
                allObjects.extend(obj.getContainedObjectsWithReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentRecursive(referent1, propertyName1, value1, referent2, propertyName2, value2, referent3, propertyName3, value3, referent4, propertyName4, value4, referent5, propertyName5, value5, referent6, propertyName6, value6, referent7, propertyName7, value7, referent8))
        return allObjects

    def getContainedObjectsWithPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndProperty(self, propertyName1, value1, referent1, propertyName2, value2, referent2, propertyName3, value3, referent3, propertyName4, value4, referent4, propertyName5, value5, referent5, propertyName6, value6, referent6, propertyName7, value7, referent7, propertyName8, value8):
        return [obj for obj in self.contains if obj.properties[propertyName1] == value1 and referent1 in obj.getReferents() and obj.properties[propertyName2] == value2 and referent2 in obj.getReferents() and obj.properties[propertyName3] == value3 and referent3 in obj.getReferents() and obj.properties[propertyName4] == value4 and referent4 in obj.getReferents() and obj.properties[propertyName5] == value5 and referent5 in obj.getReferents() and obj.properties[propertyName6] == value6 and referent6 in obj.getReferents() and obj.properties[propertyName7] == value7 and referent7 in obj.getReferents() and obj.properties[propertyName8] == value8]

    def getContainedObjectsWithPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyRecursive(self, propertyName1, value1, referent1, propertyName2, value2, referent2, propertyName3, value3, referent3, propertyName4, value4, referent4, propertyName5, value5, referent5, propertyName6, value6, referent6, propertyName7, value7, referent7, propertyName8, value8):
        allObjects = []
        for obj in self.contains:
            if obj.properties[propertyName1] == value1 and referent1 in obj.getReferents() and obj.properties[propertyName2] == value2 and referent2 in obj.getReferents() and obj.properties[propertyName3] == value3 and referent3 in obj.getReferents() and obj.properties[propertyName4] == value4 and referent4 in obj.getReferents() and obj.properties[propertyName5] == value5 and referent5 in obj.getReferents() and obj.properties[propertyName6] == value6 and referent6 in obj.getReferents() and obj.properties[propertyName7] == value7 and referent7 in obj.getReferents() and obj.properties[propertyName8] == value8:
                allObjects.append(obj)
            if obj.properties["isContainer"]:
                allObjects.extend(obj.getContainedObjectsWithPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyRecursive(propertyName1, value1, referent1, propertyName2, value2, referent2, propertyName3, value3, referent3, propertyName4, value4, referent4, propertyName5, value5, referent5, propertyName6, value6, referent6, propertyName7, value7, referent7, propertyName8, value8))
        return allObjects

    def getContainedObjectsWithReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndProperty(self, referent1, propertyName1, value1, referent2, propertyName2, value2, referent3, propertyName3, value3, referent4, propertyName4, value4, referent5, propertyName5, value5, referent6, propertyName6, value6, referent7, propertyName7, value7, referent8, propertyName8, value8):
        return [obj for obj in self.contains if referent1 in obj.getReferents() and obj.properties[propertyName1] == value1 and referent2 in obj.getReferents() and obj.properties[propertyName2] == value2 and referent3 in obj.getReferents() and obj.properties[propertyName3] == value3 and referent4 in obj.getReferents() and obj.properties[propertyName4] == value4 and referent5 in obj.getReferents() and obj.properties[propertyName5] == value5 and referent6 in obj.getReferents() and obj.properties[propertyName6] == value6 and referent7 in obj.getReferents() and obj.properties[propertyName7] == value7 and referent8 in obj.getReferents() and obj.properties[propertyName8] == value8]

    def getContainedObjectsWithReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyRecursive(self, referent1, propertyName1, value1, referent2, propertyName2, value2, referent3, propertyName3, value3, referent4, propertyName4, value4, referent5, propertyName5, value5, referent6, propertyName6, value6, referent7, propertyName7, value7, referent8, propertyName8, value8):
        allObjects = []
        for obj in self.contains:
            if referent1 in obj.getReferents() and obj.properties[propertyName1] == value1 and referent2 in obj.getReferents() and obj.properties[propertyName2] == value2 and referent3 in obj.getReferents() and obj.properties[propertyName3] == value3 and referent4 in obj.getReferents() and obj.properties[propertyName4] == value4 and referent5 in obj.getReferents() and obj.properties[propertyName5] == value5 and referent6 in obj.getReferents() and obj.properties[propertyName6] == value6 and referent7 in obj.getReferents() and obj.properties[propertyName7] == value7 and referent8 in obj.getReferents() and obj.properties[propertyName8] == value8:
                allObjects.append(obj)
            if obj.properties["isContainer"]:
                allObjects.extend(obj.getContainedObjectsWithReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndReferentAndPropertyAndRefer