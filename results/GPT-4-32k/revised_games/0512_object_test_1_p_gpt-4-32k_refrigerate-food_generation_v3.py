import random

class GameObject():
    def __init__(self, name):
        if hasattr(self, "constructorsRun"):
            return
        self.constructorsRun = ["GameObject"]

        self.name = name
        self.parentContainer = None
        self.contains = []
        self.properties = {}

        self.properties["isContainer"] = False
        self.properties["isMoveable"] = True
        self.properties["temperature"] = 20.0

    def getProperty(self, propertyName):
        if propertyName in self.properties:
            return self.properties[propertyName]
        else:
            return None

    def addObject(self, obj):
        obj.removeSelfFromContainer()
        self.contains.append(obj)
        obj.parentContainer = self

    def removeObject(self, obj):
        self.contains.remove(obj)
        obj.parentContainer = None

    def removeSelfFromContainer(self):
        if self.parentContainer != None:
            self.parentContainer.removeObject(self)

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

    def tick(self):
        pass

    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

class Device(GameObject):
    def __init__(self, name):
        if hasattr(self, "constructorsRun"):
            if "Device" in self.constructorsRun:
                return
        GameObject.__init__(self, name)
        self.constructorsRun.append("Device")

        self.properties["isDevice"] = True
        self.properties["isActivatable"] = True
        self.properties["isOn"] = False

    def turnOn(self):
        if (self.getProperty("isActivatable") == False):
            return ("It's not clear how the " + self.getReferents()[0] + " could be turned on.", False)

        if self.properties["isOn"]:
            return ("The " + self.getReferents()[0] + " is already on.", False)
        else:
            self.properties["isOn"] = True
            return ("The " + self.getReferents()[0] + " is now turned on.", True)

    def turnOff(self):
        if (self.getProperty("isActivatable") == False):
            return ("It's not clear how the " + self.getReferents()[0] + " could be turned off.", False)

        if not self.properties["isOn"]:
            return ("The " + self.getReferents()[0] + " is already off.", False)
        else:
            self.properties["isOn"] = False
            return ("The " + self.getReferents()[0] + " is now turned off.", True)

    def useWithObject(self, patientObject):
        return ("You're not sure how to use the " + self.getReferents()[0] + " with the " + patientObject.name + ".", False)

    def makeDescriptionStr(self, makeDetailed=False):
        outStr = "The " + self.name + ", which is currently "
        if self.properties["isOn"]:
            outStr += "on."
        else:
            outStr += "off."
        return outStr

class Stove(Device, Container):
    def __init__(self):
        GameObject.__init__(self, "stove")
        Device.__init__(self, "stove")
        Container.__init__(self, "stove")

        self.properties["containerPrefix"] = "on"
        self.properties["isOpenable"] = False
        self.properties["isMoveable"] = False
        self.properties["isActivatable"] = True
        self.properties["isOn"] = False
        self.properties["max_temperature"] = 100.0
        self.properties["temperature_increase_per_tick"] = 5.0

    def tick(self):
        if (self.properties["isOn"] == True):
            objectsOnStove = self.getAllContainedObjectsRecursive()
            for obj in objectsOnStove:
                newTemperature = obj.properties["temperature"] + self.properties["temperature_increase_per_tick"]
                if (newTemperature > self.properties["max_temperature"]):
                    newTemperature = self.properties["max_temperature"]
                obj.properties["temperature"] = newTemperature

    def makeDescriptionStr(self, makeDetailed=False):
        outStr = "a stove"

        if self.properties["isOn"]:
            outStr += " that is currently on"
        else:
            outStr += " that is currently off"

        effectiveContents = []
        for obj in self.contains:
            effectiveContents.append(obj.makeDescriptionStr())

        if (len(effectiveContents) > 0):
            outStr += " that looks to have "
            for i in range(len(effectiveContents)):
                if (i == len(effectiveContents) - 1) and (len(effectiveContents) > 1):
                    outStr += "and "
                outStr += effectiveContents[i] + ", "
            outStr = outStr[:-2] + " " + self.properties["containerPrefix"] + " it"
        else:
            outStr += " that is empty"

        return outStr

class Fridge(Container):
    def __init__(self):
        GameObject.__init__(self, "fridge")
        Container.__init__(self, "fridge")

        self.properties["containerPrefix"] = "in"
        self.properties["isOpenable"] = True
        self.properties["isOpen"] = False
        self.properties["isMoveable"] = False
        self.properties["min_temperature"] = 4.0
        self.properties["temperature_decrease_per_tick"] = 5.0

    def tick(self):
        if (self.properties["isOpen"] == False):
            objectsInFridge = self.getAllContainedObjectsRecursive()
            for obj in objectsInFridge:
                newTemperature = obj.properties["temperature"] - self.properties["temperature_decrease_per_tick"]
                if (newTemperature < self.properties["min_temperature"]):
                    newTemperature = self.properties["min_temperature"]
                obj.properties["temperature"] = newTemperature

    def makeDescriptionStr(self, makeDetailed=False):
        outStr = "a fridge"

        if self.properties["isOpen"]:
            outStr += " that is currently open"
        else:
            outStr += " that is currently closed"

        effectiveContents = []
        for obj in self.contains:
            effectiveContents.append(obj.makeDescriptionStr())

        if (len(effectiveContents) > 0):
            outStr += " that looks to have "
            for i in range(len(effectiveContents)):
                if (i == len(effectiveContents) - 1) and (len(effectiveContents) > 1):
                    outStr += "and "
                outStr += effectiveContents[i] + ", "
            outStr = outStr[:-2] + " " + self.properties["containerPrefix"] + " it"
        else:
            outStr += " that is empty"

        return outStr

class Pot(Container):
    def __init__(self):
        GameObject.__init__(self, "pot")
        Container.__init__(self, "pot")

        self.properties["containerPrefix"] = "in"
        self.properties["isOpenable"] = False
        self.properties["isMoveable"] = True

    def makeDescriptionStr(self, makeDetailed=False):
        outStr = "a pot"

        effectiveContents = []
        for obj in self.contains:
            effectiveContents.append(obj.makeDescriptionStr())

        if (len(effectiveContents) > 0):
            outStr += " that looks to have "
            for i in range(len(effectiveContents)):
                if (i == len(effectiveContents) - 1) and (len(effectiveContents) > 1):
                    outStr += "and "
                outStr += effectiveContents[i] + ", "
            outStr = outStr[:-2] + " " + self.properties["containerPrefix"] + " it"
        else:
            outStr += " that is empty"

        return outStr

class Milk(GameObject):
    def __init__(self):
        GameObject.__init__(self, "milk")
        self.properties["isMoveable"] = True

    def makeDescriptionStr(self, makeDetailed=False):
        return "a bottle of milk"

class Thermometer(GameObject):
    def __init__(self):
        GameObject.__init__(self, "thermometer")
        self.properties["isMoveable"] = True

    def makeDescriptionStr(self, makeDetailed=False):
        return "a thermometer"

class Baby(GameObject):
    def __init__(self):
        GameObject.__init__(self, "baby")
        self.properties["isMoveable"] = False

    def makeDescriptionStr(self, makeDetailed=False):
        return "a baby"

class World(Container):
    def __init__(self):
        Container.__init__(self, "kitchen")

    def makeDescriptionStr(self, makeDetailed=False):
        outStr = "You find yourself in a kitchen. In the kitchen, you see: \n"
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

        stove = Stove()
        world.addObject(stove)

        fridge = Fridge()
        world.addObject(fridge)

        pot = Pot()
        world.addObject(pot)

        milk = Milk()
        pot.addObject(milk)

        thermometer = Thermometer()
        world.addObject(thermometer)

        baby = Baby()
        world.addObject(baby)

        return world

    def getTaskDescription(self):
        return "Your task is to heat the milk to a suitable temperature for the baby using the stove."

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
                self.addAction("examine " + objReferent, ["examine", obj])

        for objReferent, objs in allObjects.items():
            for obj in objs:
                self.addAction("take " + objReferent, ["take", obj])

        for objReferent, objs in allObjects.items():
            for obj in objs:
                self.addAction("put " + objReferent + " on stove", ["put", obj, "stove"])
                self.addAction("put " + objReferent + " in fridge", ["put", obj, "fridge"])

        for objReferent, objs in allObjects.items():
            for obj in objs:
                self.addAction("turn on " + objReferent, ["turn on", obj])
                self.addAction("turn off " + objReferent, ["turn off", obj])

        self.addAction("use thermometer on milk", ["use thermometer", "milk"])
        self.addAction("feed baby with milk", ["feed baby", "milk"])

        return self.possibleActions

    def actionExamine(self, obj):
        return obj.makeDescriptionStr(makeDetailed=True)

    def actionTake(self, obj):
        if (obj.parentContainer != self.agent):
            return "You don't currently have the " + obj.getReferents()[0] + " in your inventory."

        obsStr, objRef, success = obj.parentContainer.takeObjectFromContainer(obj)
        if (success == False):
            return obsStr

        self.agent.addObject(obj)
        return obsStr + " You put the " + obj.getReferents()[0] + " in your inventory."

    def actionPut(self, obj, container_name):
        if (obj.parentContainer != self.agent):
            return "You don't currently have the " + obj.getReferents()[0] + " in your inventory."

        container = None
        for obj in self.rootObject.contains:
            if obj.name == container_name:
                container = obj
                break

        if container is None:
            return "There is no " + container_name + " in the kitchen."

        obsStr, objRef, success = obj.parentContainer.takeObjectFromContainer(obj)
        if (success == False):
            return obsStr

        container.addObject(obj)
        return obsStr + " You put the " + obj.getReferents()[0] + " on the " + container_name + "."

    def actionTurnOn(self, obj):
        if (obj.getProperty("isDevice") == True):
            obsStr, success = obj.turnOn()
            return obsStr
        else:
            return "You can't turn on that."

    def actionTurnOff(self, obj):
        if (obj.getProperty("isDevice") == True):
            obsStr, success = obj.turnOff()
            return obsStr
        else:
            return "You can't turn off that."

    def actionUseThermometer(self, obj):
        if obj.name != "milk":
            return "You can only use the thermometer on the milk."

        if obj.parentContainer.name != "stove":
            return "The milk must be on the stove to use the thermometer."

        return "The current temperature of the milk is " + str(obj.getProperty("temperature")) + " degrees Celsius."

    def actionFeedBaby(self, obj):
        if obj.name != "milk":
            return "You can only feed the baby with milk."

        if obj.getProperty("temperature") < 35 or obj.getProperty("temperature") > 40:
            return "The milk is not at a suitable temperature for the baby."

        self.gameOver = True
        self.gameWon = True
        return "You have successfully heated the milk to a suitable temperature and fed the baby. Congratulations!"

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
        elif (actionVerb == "examine"):
            thingToExamine = action[1]
            self.observationStr = self.actionExamine(thingToExamine)
        elif (actionVerb == "take"):
            thingToTake = action[1]
            self.observationStr = self.actionTake(thingToTake)
        elif (actionVerb == "put"):
            thingToMove = action[1]
            container_name = action[2]
            self.observationStr = self.actionPut(thingToMove, container_name)
        elif (actionVerb == "turn on"):
            thingToTurnOn = action[1]
            self.observationStr= self.actionTurnOn(thingToTurnOn)
        elif (actionVerb == "turn off"):
            thingToTurnOff = action[1]
            self.observationStr = self.actionTurnOff(thingToTurnOff)
        elif (actionVerb == "use thermometer"):
            thingToMeasure = action[1]
            self.observationStr = self.actionUseThermometer(thingToMeasure)
        elif (actionVerb == "feed baby"):
            thingToFeed = action[1]
            self.observationStr = self.actionFeedBaby(thingToFeed)
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

        if self.gameWon:
            self.score = 100 - self.numSteps

        return self.score

if __name__ == "__main__":
    game = TextGame(randomSeed=0)
    print(game.getTaskDescription())
    print(game.rootObject.makeDescriptionStr())

    while not game.gameOver:
        action = input("Enter action: ")
        observation, score, reward, game_over, game_won = game.step(action)
        print(observation)
        print("Score:", score)
        print("Reward:", reward)
        print("Game Over:", game_over)
        print("Game Won:", game_won)
        print("-----------------------------")
