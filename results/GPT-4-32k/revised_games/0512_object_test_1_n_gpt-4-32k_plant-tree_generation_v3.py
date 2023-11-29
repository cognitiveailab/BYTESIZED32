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
        return ("", obj, True)

    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

class Device(GameObject):
    def __init__(self, name):
        if hasattr(self, "constructorsRun"):
            if "Device" in self.constructorsRun:
                return

        GameObject.__init__(self, name)
        self.constructorsRun.append("Device")

        self.properties["isActivatable"] = False
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

    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

class Stove(Device):
    def __init__(self, max_temperature=100, temperature_increase_per_tick=10):
        GameObject.__init__(self, "stove")
        Device.__init__(self, "stove")
        self.properties["isActivatable"] = True
        self.properties["isMoveable"] = False
        self.properties["max_temperature"] = max_temperature
        self.properties["temperature_increase_per_tick"] = temperature_increase_per_tick
        self.properties["current_temperature"] = 0

    def tick(self):
        if self.properties.get("isOn"):
            self.properties["current_temperature"] += self.properties["temperature_increase_per_tick"]
            if self.properties["current_temperature"] > self.properties["max_temperature"]:
                self.properties["current_temperature"] = self.properties["max_temperature"]

    def makeDescriptionStr(self, makeDetailed=False):
        outStr = "a stove"

        if self.properties.get("isOn"):
            outStr += " that is currently on"
        else:
            outStr += " that is currently off"

        return outStr

class Fridge(Device, Container):
    def __init__(self, min_temperature=0, temperature_decrease_per_tick=10):
        GameObject.__init__(self, "fridge")
        Device.__init__(self, "fridge")
        Container.__init__(self, "fridge")
        self.properties["isActivatable"] = True
        self.properties["isMoveable"] = False
        self.properties["min_temperature"] = min_temperature
        self.properties["temperature_decrease_per_tick"] = temperature_decrease_per_tick
        self.properties["current_temperature"] = 0

    def tick(self):
        if self.properties.get("isOn"):
            self.properties["current_temperature"] -= self.properties["temperature_decrease_per_tick"]
            if self.properties["current_temperature"] < self.properties["min_temperature"]:
                self.properties["current_temperature"] = self.properties["min_temperature"]

    def makeDescriptionStr(self, makeDetailed=False):
        outStr = "a fridge"

        if self.properties.get("isOn"):
            outStr += " that is currently on"
        else:
            outStr += " that is currently off"

        if len(self.contains) == 0:
            outStr += " and that is empty"
        else:
            if not makeDetailed:
                outStr += " and that contains one or more items."
            else:
                outStr += " and that contains the following items: \n"
                for obj in self.contains:
                    outStr += "\t" + obj.makeDescriptionStr() + "\n"

        return outStr

class Pot(Container):
    def __init__(self, name):
        GameObject.__init__(self, name)
        Container.__init__(self, name)
        self.properties["isMoveable"] = True

    def makeDescriptionStr(self, makeDetailed=False):
        outStr = f"a {self.name}"

        effectiveContents = []
        for obj in self.contains:
            effectiveContents.append(obj.makeDescriptionStr())

        if (len(effectiveContents) > 0):
            outStr += " containing "
            for i in range(len(effectiveContents)):
                if (i == len(effectiveContents) - 1) and (len(effectiveContents) > 1):
                    outStr += "and "
                outStr += effectiveContents[i] + ", "
            outStr = outStr[:-2]
        else:
            outStr += " that is empty"

        return outStr

class Milk(GameObject):
    def __init__(self, temperature=0):
        GameObject.__init__(self, "milk")
        self.properties["temperature"] = temperature

    def getReferents(self):
        return [f"milk in {self.parentContainer.name}"]

    def makeDescriptionStr(self, makeDetailed=False):
        return f"milk"

class Thermometer(GameObject):
    def __init__(self):
        GameObject.__init__(self, "thermometer")

    def use_on(self, obj):
        if obj.name == "milk":
            return f"The milk's temperature is {obj.properties['temperature']} degrees."
        else:
            return f"The thermometer can't be used on {obj.name}."

class Baby(GameObject):
    def __init__(self):
        GameObject.__init__(self, "baby")

    def feed(self, obj):
        if obj.name == "milk":
            if 35 <= obj.properties["temperature"] <= 40:
                return "You successfully fed the baby with milk at the right temperature!"
            else:
                return "The milk's temperature is not suitable for the baby."
        else:
            return f"You can't feed the baby with {obj.name}."

class Kitchen(Container):
    def __init__(self):
        Container.__init__(self, "kitchen")

    def makeDescriptionStr(self, makeDetailed=False):
        outStr = "You are in the kitchen. In the kitchen, you see: \n"
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
        world = Kitchen()

        world.addObject(self.agent)
        stove = Stove()
        world.addObject(stove)
        fridge = Fridge()
        world.addObject(fridge)
        pot = Pot("pot")
        world.addObject(pot)
        milk = Milk()
        fridge.addObject(milk)
        thermometer = Thermometer()
        world.addObject(thermometer)
        baby = Baby()
        world.addObject(baby)

        return world

    def getTaskDescription(self):
        return f"Your task is to heat the milk to a suitable temperature for a baby and feed the baby."

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
                self.addAction("turn on " + objReferent, ["turn on", obj])
                self.addAction("turn off " + objReferent, ["turn off", obj])

        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2):
                            containerPrefix = "in"
                            if obj2.properties["isContainer"]:
                                containerPrefix = obj2.properties["containerPrefix"]
                            self.addAction("put " + objReferent1 + " " + containerPrefix + " " + objReferent2, ["put", obj1, obj2])

        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2):
                            self.addAction("use " + objReferent1 + " on " + objReferent2, ["use", obj1, obj2])

        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2):
                            self.addAction("feed " + objReferent2 + " with " + objReferent1, ["feed", obj2, obj1])

        return self.possibleActions

    def actionTake(self, obj):
        if (obj.parentContainer == None):
            return "Something has gone wrong -- that object is dangling in the void.  You can't take that."

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

    def actionTurnOn(self, obj):
        if (obj.getProperty("isActivatable") == False):
            return ("It's not clear how the " + obj.getReferents()[0] + " could be turned on.", False)

        if obj.properties.get("isOn"):
            return ("The " + obj.getReferents()[0] + " is already on.", False)
        else:
            obj.properties["isOn"] = True
            return ("The " + obj.getReferents()[0] + " is now turned on.", True)

    def actionTurnOff(self, obj):
        if (obj.getProperty("isActivatable") == False):
            return ("It's not clear how the " + obj.getReferents()[0] + " could be turned off.", False)

        if not obj.properties.get("isOn"):
            return ("The " + obj.getReferents()[0] + " is already off.", False)
        else:
            obj.properties["isOn"] = False
            return ("The " + obj.getReferents()[0] + " is now turned off.", True)

    def actionUse(self, obj1, obj2):
        if obj1.name == "thermometer" and obj2.name == "milk":
            return obj1.use_on(obj2)
        else:
            return f"You can't use {obj1.name} on {obj2.name}."

    def actionFeed(self, obj1, obj2):
        if obj1.name == "baby" and obj2.name == "milk":
            return obj1.feed(obj2)
        else:
            return f"You can't feed {obj1.name} with {obj2.name}."

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
        elif (actionVerb == "turn on"):
            thingToTurnOn = action[1]
            self.observationStr = self.actionTurnOn(thingToTurnOn)
        elif (actionVerb == "turn off"):
            thingToTurnOff = action[1]
            self.observationStr = self.actionTurnOff(thingToTurnOff)
        elif (actionVerb == "put"):
            thingToMove = action[1]
            newContainer = action[2]
            self.observationStr = self.actionPut(thingToMove, newContainer)
        elif (actionVerb == "use"):
            obj1 = action[1]
            obj2 = action[2]
            self.observationStr = self.actionUse(obj1, obj2)
        elif (actionVerb == "feed"):
            obj1 = action[1]
            obj2 = action[2]
            self.observationStr = self.actionFeed(obj1, obj2)
        else:
            self.observationStr = "ERROR: Unknown action."

        tick_output_strs = self.doWorldTick()
        if len(tick_output_strs) > 0:
            self.observationStr = '\n'.join([self.observationStr] + tick_output_strs)
        lastScore = self.score
        self.calculateScore()
        reward = self.score - lastScore

        return (self.observationStr, self.score, reward, self.gameOver, self.gameWon)

    def doWorldTick(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        output_strs = []
        for obj in allObjects:
            tick_output_str = obj.tick()
            if tick_output_str is not None:
                output_strs.append(tick_output_str)
        return output_strs

    def calculateScore(self):
        self.score = 0

        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        for obj in allObjects:
            if (obj.name == "baby"):
                for obj_baby in obj.contains:
                    if obj_baby.name == "milk" and 35 <= obj_baby.properties["temperature"] <= 40:
                        self.score = 1
                        self.gameOver = True
                        self.gameWon = True

def main():
    randomSeed = 0

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
