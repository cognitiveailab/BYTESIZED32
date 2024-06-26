import random

class GameObject():
    def __init__(self, name):
        if hasattr(self, "constructorsRun"):
            return
        self.constructorsRun = ["GameObject"]

        self.name = name
        self.parent = None
        self.contains = []
        self.properties = {}

        self.properties["isContainer"] = False
        self.properties["isMoveable"] = True

    def getProperty(self, propertyName):
        if propertyName in self.properties:
            return self.properties[propertyName]
        else:
            return None

    def addObject(self, obj):
        obj.removeSelfFromContainer()
        self.contains.append(obj)
        obj.parent = self

    def removeObject(self, obj):
        self.contains.remove(obj)
        obj.parent = None

    def removeSelfFromContainer(self):
        if self.parent != None:
            self.parent.removeObject(self)

    def getAllContainedObjectsRecursive(self):
        outList = []
        for obj in self.contains:
            outList.append(obj)
            outList.extend(obj.getAllContainedObjectsRecursive())
        return outList

    def containsItemWithName(self, name):
        foundObjects = []
        for obj in self.contains:
            if obj.name == name:
                foundObjects.append(obj)
        return foundObjects

    def tick(self):
        pass

    def getReferents(self):
        return [self.name]

    def makeDescriptionStr(self, makeDetailed=False):
        return self.name

class Container(GameObject):
    def __init__(self, name):
        if hasattr(self, "constructorsRun"):
            if "Container" in self.constructorsRun:
                return

        GameObject.__init__(self, name)
        self.constructorsRun.append("Container")

        self.properties["isContainer"] = True
        self.properties["isOpenable"] = False
        self.properties["isOpen"] = True
        self.properties["containerPrefix"] = "in"

    def openContainer(self):
        if not self.getProperty("isOpenable"):
            return ("The " + self.name + " can't be opened.", False)

        if self.getProperty("isOpen"):
            return ("The " + self.name + " is already open.", False)

        self.properties["isOpen"] = True
        return ("The " + self.name + " is now open.", True)

    def closeContainer(self):
        if not (self.getProperty("isOpenable") == True):
            return ("The " + self.name + " can't be closed.", False)

        if not (self.getProperty("isOpen") == True):
            return ("The " + self.name + " is already closed.", False)

        self.properties["isOpen"] = False
        return ("The " + self.name + " is now closed.", True)

    def placeObjectInContainer(self, obj):
        if not (self.getProperty("isContainer") == True):
            return ("The " + self.name + " is not a container, so things can't be placed there.", False)

        if not (obj.getProperty("isMoveable") == True):
            return ("The " + obj.name + " is not moveable.", None, False)

        if not (self.getProperty("isOpen") == True):
            return ("The " + self.name + " is closed, so things can't be placed there.", False)

        self.addObject(obj)
        return ("The " + obj.getReferents()[0] + " is placed in the " + self.name + ".", True)

    def takeObjectFromContainer(self, obj):
        if not (self.getProperty("isContainer") == True):
            return ("The " + self.name + " is not a container, so things can't be removed from it.", None, False)

        if not (obj.getProperty("isMoveable") == True):
            return ("The " + obj.name + " is not moveable.", None, False)

        if not (self.getProperty("isOpen") == True):
            return ("The " + self.name + " is closed, so things can't be removed from it.", None, False)

        if obj not in self.contains:
            return ("The " + obj.name + " is not contained in the " + self.name + ".", None, False)

        obj.removeSelfFromContainer()
        return ("The " + obj.getReferents()[0] + " is removed from the " + self.name + ".", obj, True)

    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name

class Device(GameObject):
    def __init__(self, name):
        if hasattr(self, "constructorsRun"):
            if "Device" in self.constructorsRun:
                return

        GameObject.__init__(self, name)
        self.constructorsRun.append("Device")

        self.properties["isDevice"] = True
        self.properties["isOn"] = False

    def turnOn(self):
        if not self.getProperty("isDevice"):
            return ("The " + self.name + " is not a device.", False)

        if self.getProperty("isOn"):
            return ("The " + self.name + " is already on.", False)

        self.properties["isOn"] = True
        return ("The " + self.name + " is now on.", True)

    def turnOff(self):
        if not self.getProperty("isDevice"):
            return ("The " + self.name + " is not a device.", False)

        if not self.getProperty("isOn"):
            return ("The " + self.name + " is already off.", False)

        self.properties["isOn"] = False
        return ("The " + self.name + " is now off.", True)

    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name

class Grill(Device, Container):
    def __init__(self, name):
        Device.__init__(self, name)
        Container.__init__(self, name)
        self.properties["isContainer"] = True
        self.properties["containerPrefix"] = "on"
        self.properties["isMoveable"] = False
        self.properties["isOn"] = False

    def makeDescriptionStr(self, makeDetailed=False):
        return "a " + self.name

class Food(GameObject):
    def __init__(self, name):
        GameObject.__init__(self, name)
        self.properties["isFood"] = True
        self.properties["isSalted"] = False
        self.properties["isOiled"] = False
        self.properties["isGrilled"] = False

    def addSalt(self):
        if not self.getProperty("isFood"):
            return ("The " + self.name + " is not food.", False)

        if self.getProperty("isSalted"):
            return ("The " + self.name + " is already salted.", False)

        self.properties["isSalted"] = True
        return ("The " + self.name + " is now salted.", True)

    def addOil(self):
        if not self.getProperty("isFood"):
            return ("The " + self.name + " is not food.", False)

        if self.getProperty("isOiled"):
            return ("The " + self.name + " is already oiled.", False)

        self.properties["isOiled"] = True
        return ("The " + self.name + " is now oiled.", True)

    def grill(self, grill):
        if not self.getProperty("isFood"):
            return ("The " + self.name + " is not food.", False)

        if not grill.getProperty("isDevice"):
            return ("The " + grill.name + " is not a device.", False)

        if not grill.getProperty("isOn"):
            return ("The " + grill.name + " is not on.", False)

        if self.getProperty("isGrilled"):
            return ("The " + self.name + " is already grilled.", False)

        self.properties["isGrilled"] = True
        return ("The " + self.name + " is now grilled.", True)

    def eat(self):
        if not self.getProperty("isFood"):
            return ("The " + self.name + " is not food.", False)

        if not self.getProperty("isGrilled"):
            return ("The " + self.name + " is not grilled yet.", False)

        return ("You eat the " + self.name + ". Delicious!", True)

    def makeDescriptionStr(self, makeDetailed=False):
        return "a " + self.name

class Salt(GameObject):
    def __init__(self, name):
        GameObject.__init__(self, name)
        self.properties["isSalt"] = True

    def makeDescriptionStr(self, makeDetailed=False):
        return "some " + self.name

class Oil(GameObject):
    def __init__(self, name):
        GameObject.__init__(self, name)
        self.properties["isOil"] = True

    def makeDescriptionStr(self, makeDetailed=False):
        return "some " + self.name

class World(Container):
    def __init__(self):
        Container.__init__(self, "backyard")

    def makeDescriptionStr(self, makeDetailed=False):
        outStr = "You find yourself in a backyard. In the backyard, you see: \n"
        for obj in self.contains:
            outStr += "\t" + obj.makeDescriptionStr() + "\n"

        return outStr

class Agent(Container):
    def __init__(self):
        GameObject.__init__(self, "agent")
        Container.__init__(self, "agent")

    def getReferents(self):
        return ["yourself"]

    def makeDescriptionStr(self, makeDetailed=False):
        return "yourself"

class TextGame:
    def __init__(self, randomSeed):
        self.random = random.Random(randomSeed)
        self.agent = Agent()
        self.rootObject = self.initializeWorld()
        self.score = 0
        self.numSteps = 0
        self.gameOver = False
        self.gameWon = False
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.calculateScore()

    def initializeWorld(self):
        world = World()

        world.addObject(self.agent)

        grill = Grill("grill")
        world.addObject(grill)

        food = Food("food")
        world.addObject(food)

        salt = Salt("salt")
        world.addObject(salt)

        oil = Oil("oil")
        world.addObject(oil)

        return world

    def getTaskDescription(self):
        return "Your task is to grill the food. First, take the food and add salt and oil to it. Then, turn on the grill, put the food on the grill, and wait until it's cooked. Finally, eat the food."

    def makeNameToObjectDict(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()

        nameToObjectDict = {}
        for obj in allObjects:
            for name in obj.getReferents():
                if name in nameToObjectDict:
                    nameToObjectDict[name].append(obj)
                else:
                    nameToObjectDict[name] = [obj]

        return nameToObjectDict

    def addAction(self, actionStr, actionArgs):
        if not (actionStr in self.possibleActions):
            self.possibleActions[actionStr] = []
        self.possibleActions[actionStr].append(actionArgs)

    def generatePossibleActions(self):
        allObjects = self.makeNameToObjectDict()

        self.possibleActions = {}

        self.addAction("look around", ["look around"])
        self.addAction("look", ["look around"])

        self.addAction("inventory", ["inventory"])

        for objReferent, objs in allObjects.items():
            for obj in objs:
                self.addAction("take " + objReferent, ["take", obj])
                self.addAction("take " + objReferent + " from " + obj.parent.getReferents()[0], ["take", obj])

        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2):
                            containerPrefix = "in"
                            if obj2.properties["isContainer"]:
                                containerPrefix = obj2.properties["containerPrefix"]
                            self.addAction("put " + objReferent1 + " " + containerPrefix + " " + objReferent2, ["put", obj1, obj2])

        for objReferent, objs in allObjects.items():
            for obj in objs:
                if obj.getProperty("isFood"):
                    self.addAction("add salt to " + objReferent, ["add salt", obj])
                    self.addAction("add oil to " + objReferent, ["add oil", obj])
                    self.addAction("eat " + objReferent, ["eat", obj])

        for objReferent, objs in allObjects.items():
            for obj in objs:
                if obj.getProperty("isDevice"):
                    self.addAction("turn on " + objReferent, ["turn on", obj])
                    self.addAction("turn off " + objReferent, ["turn off", obj])

        return self.possibleActions

    def actionTake(self, obj):
        if (obj.parent == None):
            return "Something has gone wrong -- that object is dangling in the void.  You can't take that."

        obsStr, objRef, success = obj.parent.takeObjectFromContainer(obj)
        if (success == False):
            return obsStr

        self.agent.addObject(obj)
        return obsStr + " You put the " + obj.getReferents()[0] + " in your inventory."

    def actionPut(self, objToMove, newContainer):
        if (newContainer.getProperty("isContainer") == False):
            return "You can't put things in the " + newContainer.getReferents()[0] + "."

        if (objToMove.parent != self.agent):
            return "You don't currently have the " + objToMove.getReferents()[0] + " in your inventory."

        originalContainer = objToMove.parent
        obsStr1, objRef, success = objToMove.parent.takeObjectFromContainer(objToMove)
        if (success == False):
            return obsStr1

        obsStr2, success = newContainer.placeObjectInContainer(objToMove)
        if (success == False):
            originalContainer.addObject(objToMove)
            return obsStr2

        return obsStr1 + "\n" + obsStr2

    def actionInventory(self):
        inventory = self.agent.contains
        if (len(inventory) == 0):
            return "Your inventory is empty."
        else:
            obsStr = "You have the following items in your inventory:\n"
            for obj in inventory:
                obsStr += "\t" + obj.makeDescriptionStr() + "\n"
            return obsStr

    def actionAddSalt(self, food):
        if not food.getProperty("isFood"):
            return "The " + food.name + " is not food.", False

        if food.getProperty("isSalted"):
            return "The " + food.name + " is already salted.", False

        food.properties["isSalted"] = True
        return "The " + food.name + " is now salted.", True

    def actionAddOil(self, food):
        if not food.getProperty("isFood"):
            return "The " + food.name + " is not food.", False

        if food.getProperty("isOiled"):
            return "The " + food.name + " is already oiled.", False

        food.properties["isOiled"] = True
        return "The " + food.name + " is now oiled.", True

    def actionTurnOn(self, device):
        if not device.getProperty("isDevice"):
            return "The " + device.name + " is not a device.", False

        if device.getProperty("isOn"):
            return "The " + device.name + " is already on.", False

        device.properties["isOn"] = True
        return "The " + device.name + " is now on.", True

    def actionTurnOff(self, device):
        if not device.getProperty("isDevice"):
            return "The " + device.name + " is not a device.", False

        if not device.getProperty("isOn"):
            return "The " + device.name + " is already off.", False

        device.properties["isOn"] = False
        return "The " + device.name + " is now off.", True

    def actionGrill(self, food, grill):
        if not food.getProperty("isFood"):
            return "The " + food.name + " is not food.", False

        if not grill.getProperty("isDevice"):
            return "The " + grill.name + " is not a device.", False

        if not grill.getProperty("isOn"):
            return "The " + grill.name + " is not on.", False

        if food.getProperty("isGrilled"):
            return "The " + food.name + " is already grilled.", False

        food.properties["isGrilled"] = True
        return "The " + food.name + " is now grilled.", True

    def actionEat(self, food):
        if not food.getProperty("isFood"):
            return "The " + food.name + " is not food.", False

        if not food.getProperty("isGrilled"):
            return "The " + food.name + " is not grilled yet.", False

        return "You eat the " + food.name + ". Delicious!", True

    def step(self, actionStr):
        self.observationStr = ""
        reward = 0

        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return (self.observationStr, self.score, reward, self.gameOver, self.gameWon)

        self.numSteps += 1

        actions = self.possibleActions[actionStr]
        action = None

        if (len(actions) > 1):
            action = actions[0]
        else:
            action = actions[0]

        actionVerb = action[0]

        if (actionVerb == "look around"):
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif (actionVerb == "inventory"):
            self.observationStr = self.actionInventory()
        elif (actionVerb == "take"):
            thingToTake = action[1]
            self.observationStr = self.actionTake(thingToTake)
        elif (actionVerb == "put"):
            thingToMove = action[1]
            newContainer = action[2]
            self.observationStr = self.actionPut(thingToMove, newContainer)
        elif (actionVerb == "add salt"):
            food = action[1]
            self.observationStr, success = self.actionAddSalt(food)
        elif (actionVerb == "add oil"):
            food = action[1]
            self.observationStr, success = self.actionAddOil(food)
        elif (actionVerb == "turn on"):
            device = action[1]
            self.observationStr, success = self.actionTurnOn(device)
        elif (actionVerb == "turn off"):
            device = action[1]
            self.observationStr, success = self.actionTurnOff(device)
        elif (actionVerb == "grill"):
            food = action[1]
            grill = action[2]
            self.observationStr, success = self.actionGrill(food, grill)
        elif (actionVerb == "eat"):
            food = action[1]
            self.observationStr, success = self.actionEat(food)
        else:
            self.observationStr = "ERROR: Unknown action."

        self.doWorldTick()

        lastScore = self.score
        self.calculateScore()
        reward = self.score - lastScore

        return (self.observationStr, self.score, reward, self.gameOver, self.gameWon)

    def doWorldTick(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        for obj in allObjects:
            obj.tick()

    def calculateScore(self):
        self.score = 0

        food = None
        for obj in self.rootObject.getAllContainedObjectsRecursive():
            if obj.getProperty("isFood"):
                food = obj
                break

        if food is not None:
            if food.getProperty("isGrilled") and food.parent == self.agent:
                self.score += 1
                self.gameOver = True
                self.gameWon = True

if __name__ == "__main__":
    main()
