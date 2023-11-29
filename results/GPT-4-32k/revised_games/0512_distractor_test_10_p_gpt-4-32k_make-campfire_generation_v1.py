import random

class Agent(GameObject):
    def __init__(self):
        GameObject.__init__(self, "agent")

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

    def getCanonicalReferent(self):
        return self.getReferents()[0]

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
        return("You're not sure how to use the " + self.getReferents()[0] + " with the " + patientObject.name + ".", False)

    def makeDescriptionStr(self, makeDetailed=False):
        outStr = "The " + self.name + ", which is currently "
        if self.properties["isOn"]:
            outStr += "on."
        else:
            outStr += "off."
        return outStr

class Stove(Device):
    def __init__(self):
        Device.__init__(self, "stove")
        self.properties["maxTemperature"] = 500
        self.properties["tempIncreasePerTick"] = 50
        self.properties["currentTemperature"] = 0

    def tick(self):
        if self.properties["isOn"]:
            self.properties["currentTemperature"] += self.properties["tempIncreasePerTick"]
            if self.properties["currentTemperature"] > self.properties["maxTemperature"]:
                self.properties["currentTemperature"] = self.properties["maxTemperature"]

    def makeDescriptionStr(self, makeDetailed=False):
        outStr = "a stove"
        if self.properties["isOn"]:
            outStr += " that is turned on and has a temperature of " + str(self.properties["currentTemperature"]) + " degrees."
        else:
            outStr += " that is turned off."
        return outStr

class Pot(Container):
    def __init__(self):
        Container.__init__(self, "pot")
        self.properties["temperature"] = 0

    def tick(self):
        if self.parentContainer != None and isinstance(self.parentContainer, Stove):
            stove = self.parentContainer
            if stove.properties["isOn"]:
                self.properties["temperature"] = stove.properties["currentTemperature"]

    def makeDescriptionStr(self, makeDetailed=False):
        outStr = "a pot"
        if self.properties["temperature"] > 0:
            outStr += " with a temperature of " + str(self.properties["temperature"]) + " degrees."
        else:
            outStr += " that is cold."
        return outStr

class Butter(GameObject):
    def __init__(self):
        GameObject.__init__(self, "butter")
        self.properties["temperature"] = 0
        self.properties["stateOfMatter"] = "solid"
        self.properties["solidName"] = "butter"
        self.properties["liquidName"] = "melted butter"
        self.properties["gasName"] = "vaporized butter"
        self.properties["meltingPoint"] = 90
        self.properties["boilingPoint"] = 250

    def tick(self):
        if self.parentContainer != None and isinstance(self.parentContainer, Pot):
            pot = self.parentContainer
            self.properties["temperature"] = pot.properties["temperature"]
            if self.properties["temperature"] < self.properties["meltingPoint"]:
                self.properties["stateOfMatter"] = "solid"
            elif self.properties["temperature"] < self.properties["boilingPoint"]:
                self.properties["stateOfMatter"] = "liquid"
            else:
                self.properties["stateOfMatter"] = "gas"

    def makeDescriptionStr(self, makeDetailed=False):
        outStr = self.properties[self.properties["stateOfMatter"] + "Name"]
        if self.properties["stateOfMatter"] != "solid":
            outStr += " with a temperature of " + str(self.properties["temperature"]) + " degrees."
        return outStr

class Room(Container):
    def __init__(self):
        Container.__init__(self, "room")

    def makeDescriptionStr(self, makeDetailed=False):
        outStr = "You are in a room. You see:\n"
        for obj in self.contains:
            outStr += "\t" + obj.makeDescriptionStr() + "\n"
        return outStr

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
        world = Room()

        world.addObject(self.agent)

        stove = Stove()
        world.addObject(stove)

        pot = Pot()
        world.addObject(pot)

        butter = Butter()
        world.addObject(butter)

        return world

    def getTaskDescription(self):
        return "Your task is to melt the butter."

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
                self.addAction("take " + objReferent + " from " + obj.parentContainer.getReferents()[0], ["take", obj])

        for objReferent, objs in allObjects.items():
            for obj in objs:
                self.addAction("examine " + objReferent, ["examine", obj])

        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2):
                            containerPrefix = "in"
                            if obj2.properties["isContainer"]:
                                containerPrefix = obj2.properties["containerPrefix"]
                            self.addAction("put " + objReferent1 + " " + containerPrefix + " " + objReferent2, ["put", obj1, obj2])

        return self.possibleActions

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
            self.observationStr = thingToExamine.makeDescriptionStr(makeDetailed = True)
        elif (actionVerb == "take"):
            thingToTake = action[1]
            self.observationStr = self.actionTake(thingToTake)
        elif (actionVerb == "put"):
            thingToMove = action[1]
            newContainer = action[2]
            self.observationStr = self.actionPut(thingToMove, newContainer)

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

        foundObjects = self.rootObject.containsItemWithName("butter")
        if (len(foundObjects) > 0):
            butter = foundObjects[0]
            if butter.properties["stateOfMatter"] == "liquid":
                self.score += 1
                self.gameOver = True
                self.gameWon = True

        foundObjects = self.rootObject.containsItemWithName("pot")
        if (len(foundObjects) > 0):
            pot = foundObjects[0]
            if pot.properties["temperature"] >= pot.properties["boilingPoint"]:
                self.score = -1
                self.gameOver = True
                self.gameWon = False

def main():
    randomSeed = 0

    game = TextGame(randomSeed = randomSeed)

    print("Task Description: " + game.getTaskDescription())
    print("")
    print("Initial Observation: " + game.observationStr)
    print("")
    print("Type 'help' for a list of possible actions.")
    print("")

    while True:
        actionStr = ""
        while ((len(actionStr) == 0) or (actionStr == "help")):
            actionStr = input("> ")
            if (actionStr == "help"):
                print("Possible actions: " + str(game.generatePossibleActions().keys()))
                print("")
                actionStr = ""
            elif (actionStr == "exit") or (actionStr == "quit"):
                return

        observationStr, score, reward, gameOver, gameWon = game.step(actionStr)

        possibleActions = game.generatePossibleActions()

       print("Observaton: " + observationStr)
        print("")
        print("Current step: " + str(game.numSteps))
        print("Score: " + str(score))
        print("Reward: " + str(reward))
        print("Game Over: " + str(gameOver))
        print("Game Won: " + str(gameWon))
        print("")
        print("----------------------------------------")

if __name__ == "__main__":
    main()
