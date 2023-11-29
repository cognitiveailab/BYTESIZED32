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

class Stove(Container):
    def __init__(self):
        Container.__init__(self, "stove")
        self.properties["isOpenable"] = False
        self.properties["isOn"] = False
        self.properties["temperature_increase_per_tick"] = 5
        self.properties["max_temperature"] = 100

    def turnOn(self):
        if self.getProperty("isOn"):
            return "The stove is already on."
        self.properties["isOn"] = True
        return "The stove is now on."

    def turnOff(self):
        if not self.getProperty("isOn"):
            return "The stove is already off."
        self.properties["isOn"] = False
        return "The stove is now off."

    def tick(self):
        super().tick()
        if self.getProperty("isOn"):
            for obj in self.contains:
                if obj.name == "pot":
                    obj.properties["temperature"] += self.properties["temperature_increase_per_tick"]
                    if obj.properties["temperature"] > self.properties["max_temperature"]:
                        obj.properties["temperature"] = self.properties["max_temperature"]

    def makeDescriptionStr(self, makeDetailed=False):
        if self.getProperty("isOn"):
            return "a stove that is on."
        else:
            return "a stove that is off."

class Fridge(Container):
    def __init__(self):
        Container.__init__(self, "fridge")
        self.properties["isOpenable"] = True
        self.properties["isOpen"] = False
        self.properties["temperature_decrease_per_tick"] = 5
        self.properties["min_temperature"] = 0

    def tick(self):
        super().tick()
        if self.getProperty("isOpen"):
            for obj in self.contains:
                if obj.name == "pot":
                    obj.properties["temperature"] -= self.properties["temperature_decrease_per_tick"]
                    if obj.properties["temperature"] < self.properties["min_temperature"]:
                        obj.properties["temperature"] = self.properties["min_temperature"]

    def makeDescriptionStr(self, makeDetailed=False):
        if self.getProperty("isOpen"):
            return "a fridge that is open."
        else:
            return "a fridge that is closed."

class Pot(Container):
    def __init__(self):
        Container.__init__(self, "pot")
        self.properties["isOpenable"] = False
        self.properties["temperature"] = 0

    def makeDescriptionStr(self, makeDetailed=False):
        return "a pot with milk at " + str(self.properties["temperature"]) + " degrees."

class Milk(GameObject):
    def __init__(self):
        GameObject.__init__(self, "milk")

    def makeDescriptionStr(self, makeDetailed=False):
        return "milk"

class Thermometer(GameObject):
    def __init__(self):
        GameObject.__init__(self, "thermometer")

    def useOn(self, obj):
        if obj.name == "pot":
            return "The milk temperature is " + str(obj.properties["temperature"]) + " degrees."
        else:
            return "You can't use the thermometer on that."

    def makeDescriptionStr(self, makeDetailed=False):
        return "a thermometer"

class Baby(GameObject):
    def __init__(self):
        GameObject.__init__(self, "baby")

    def feed(self, obj):
        if obj.name == "pot":
            if 35 <= obj.properties["temperature"] <= 40:
                return "You successfully fed the baby with milk at the right temperature!", True
            else:
                return "The milk temperature is not suitable for the baby.", False
        else:
            return "You can't feed the baby with that."

    def makeDescriptionStr(self, makeDetailed=False):
        return "a baby"

class World(Container):
    def __init__(self):
        Container.__init__(self, "kitchen")

    def makeDescriptionStr(self, makeDetailed=False):
        outStr = "You find yourself in a kitchen. Around you, you see:\n"
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
        fridge.addObject(pot)

        milk = Milk()
        pot.addObject(milk)

        thermometer = Thermometer()
        world.addObject(thermometer)

        baby = Baby()
        world.addObject(baby)

        self.random.shuffle(world.contains)

        return world

    def getTaskDescription(self):
        return "Your task is to heat milk to a temperature that is suitable for a baby using a stove."

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
                self.addAction("open " + objReferent, ["open", obj])
                self.addAction("close " + objReferent, ["close", obj])

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

        for objReferent, objs in allObjects.items():
            for obj in objs:
                self.addAction("use thermometer on " + objReferent, ["use thermometer on", obj])

        for objReferent, objs in allObjects.items():
            for obj in objs:
                self.addAction("feed baby with " + objReferent, ["feed baby with", obj])

        return self.possibleActions

    def actionOpen(self, obj):
        if (obj.getProperty("isContainer") == True):
            obsStr, success = obj.openContainer()
            return obsStr
        else:
            return "You can't open that."

    def actionClose(self, obj):
        if (obj.getProperty("isContainer") == True):
            obsStr, success = obj.closeContainer()
            return obsStr
        else:
            return "You can't close that."

    def actionTake(self, obj):
        if (obj.parentContainer == None):
            return "Something has gone wrong -- that object is dangling in the void.  You can't take that."

        if (obj.getProperty("isCombusting") == True):
            return "You can't pick up the " + obj.getReferents()[0] + " because it's on fire!"

        obsStr, objRef, success = obj.parentContainer.takeObjectFromContainer(obj)
        if (success == False):
            return obsStr

        self.agent.addObject(obj)
        return obsStr + " You put the " + obj.getReferents()[0] + " in your inventory."

    def actionPut(self, objToMove, newContainer):
        if (newContainer.getProperty("isContainer") == False):
            return "You can't put things in the " + newContainer.getReferents()[0] + "."

        if (objToMove.parentContainer != self.agent):
            return "You don't currently have the " + objToMove.getReferents()[0] + " in your inventory."

        originalContainer = objToMove.parentContainer
        obsStr1, objRef, success = objToMove.parentContainer.takeObjectFromContainer(objToMove)
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

    def actionExamine(self, obj):
        return obj.makeDescriptionStr(makeDetailed=True)

    def actionUseThermometerOn(self, thermometer, obj):
        return thermometer.useOn(obj)

    def actionFeedBabyWith(self, baby, obj):
        obsStr, success = baby.feed(obj)
        if success:
            self.gameOver = True
            self.gameWon = True
        return obsStr

    def doWorldTick(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        for obj in allObjects:
            obj.tick()

    def calculateScore(self):
        self.score = 0

        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        for obj in allObjects:
            if isinstance(obj, Pot):
                if 35 <= obj.properties["temperature"] <= 40:
                    self.score += 1

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
        elif (actionVerb == "open"):
            thingToOpen = action[1]
            self.observationStr = self.actionOpen(thingToOpen)
        elif (actionVerb == "close"):
            thingToClose = action[1]
            self.observationStr = self.actionClose(thingToClose)
        elif (actionVerb == "take"):
            thingToTake = action[1]
            self.observationStr = self.actionTake(thingToTake)
        elif (actionVerb == "put"):
            thingToMove = action[1]
            newContainer = action[2]
            self.observationStr = self.actionPut(thingToMove, newContainer)
        elif (actionVerb == "use thermometer on"):
            thermometer = action[1]
            obj = action[2]
            self.observationStr = self.actionUseThermometerOn(thermometer, obj)
        elif (actionVerb == "feed baby with"):
            baby = action[1]
            obj = action[2]
            self.observationStr = self.actionFeedBabyWith(baby, obj)
        else:
            self.observationStr = "ERROR: Unknown action."

        self.doWorldTick()

        lastScore = self.score
        self.calculateScore()
        reward = self.score - lastScore

        return (self.observationStr, self.score, reward, self.gameOver, self.gameWon)

def main():
    randomSeed = 1
    game = TextGame(randomSeed=randomSeed)

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
