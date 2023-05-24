import random

class GameObject():
    def __init__(self, name, isContainer=False, isMoveable=True, isUsable=False, isActivatable=False):
        if hasattr(self, "constructorsRun"):
            return
        self.constructorsRun = ["GameObject"]

        self.name = name
        self.parentContainer = None
        self.contains = []
        self.properties = {}

        self.properties["isContainer"] = isContainer
        self.properties["isMoveable"] = isMoveable
        self.properties["isUsable"] = isUsable
        self.properties["isActivatable"] = isActivatable

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
        if not self.getProperty("isContainer"):
            return ("The " + self.name + " is not a container, so things can't be placed there.", False)

        if not obj.getProperty("isMoveable"):
            return ("The " + obj.name + " is not moveable.", None, False)

        if not self.getProperty("isOpen"):
            return ("The " + self.name + " is closed, so things can't be placed there.", False)

        self.addObject(obj)
        return ("The " + obj.getReferents()[0] + " is placed in the " + self.name + ".", True)

    def takeObjectFromContainer(self, obj):
        if not self.getProperty("isContainer"):
            return ("The " + self.name + " is not a container, so things can't be removed from it.", None, False)

        if not obj.getProperty("isMoveable"):
            return ("The " + obj.name + " is not moveable.", None, False)

        if not self.getProperty("isOpen"):
            return ("The " + self.name + " is closed, so things can't be removed from it.", None, False)

        if obj not in self.contains:
            return ("The " + obj.name + " is not contained in the " + self.name + ".", None, False)

        obj.removeSelfFromContainer()
        return ("The " + obj.getReferents()[0] + " is removed from the " + self.name + ".", obj, True)

    def makeDescriptionStr(self, makeDetailed=False):
        return "a(n) " + self.name + "."

class Stone(GameObject):
    def __init__(self, name, volume, weight):
        GameObject.__init__(self, name)
        self.properties["volume"] = volume
        self.properties["weight"] = weight

    def makeDescriptionStr(self, makeDetailed=False):
        return f"a {self.name} with a weight of {self.properties['weight']} grams."

class MeasuringCup(Container):
    def __init__(self, name, max_volume):
        GameObject.__init__(self, name)
        Container.__init__(self, name)
        self.properties["max_volume"] = max_volume
        self.properties["containedVolume"] = 0
        self.properties["containsLiquid"] = False

    def addObject(self, obj):
        if obj.name == "water":
            self.properties["containsLiquid"] = True
            self.properties["containedVolume"] += obj.getProperty("volume")
            if self.properties["containedVolume"] > self.properties["max_volume"]:
                self.properties["containedVolume"] = self.properties["max_volume"]
        super().addObject(obj)

    def removeObject(self, obj):
        if obj.name == "water":
            self.properties["containedVolume"] -= obj.getProperty("volume")
            if self.properties["containedVolume"] <= 0:
                self.properties["containsLiquid"] = False
                self.properties["containedVolume"] = 0
        super().removeObject(obj)

    def makeDescriptionStr(self, makeDetailed=False):
        return f"a {self.name} with a maximum volume of {self.properties['max_volume']} ml."

class Scale(GameObject):
    def __init__(self, name):
        GameObject.__init__(self, name)
        self.properties["isMoveable"] = False
        self.properties["isUsable"] = True

    def useWithObject(self, obj):
        if obj.getProperty("weight") is not None:
            return f"The scale reads {obj.getProperty('weight')} grams.", True
        else:
            return "You cannot weigh that.", False

    def makeDescriptionStr(self, makeDetailed=False):
        return f"a {self.name}."

class Sink(Container):
    def __init__(self, name, water_out_per_tick):
        GameObject.__init__(self, name)
        Container.__init__(self, name)
        self.properties["water_out_per_tick"] = water_out_per_tick
        self.properties["isActivatable"] = True
        self.properties["isOn"] = False

    def addObject(self, obj):
        if obj.name == "measuring cup":
            self.properties["isOn"] = True
        super().addObject(obj)

    def removeObject(self, obj):
        if obj.name == "measuring cup":
            self.properties["isOn"] = False
        super().removeObject(obj)

    def tick(self):
        if self.properties["isOn"]:
            for obj in self.contains:
                if obj.name == "measuring cup":
                    obj.properties["containedVolume"] += self.properties["water_out_per_tick"]
                    if obj.properties["containedVolume"] > obj.properties["max_volume"]:
                        obj.properties["containedVolume"] = obj.properties["max_volume"]

    def makeDescriptionStr(self, makeDetailed=False):
        return f"a {self.name}."

class Water(GameObject):
    def __init__(self, volume):
        GameObject.__init__(self, "water")
        self.properties["volume"] = volume

    def makeDescriptionStr(self, makeDetailed=False):
        return f"water with a volume of {self.properties['volume']} ml."

class Room(Container):
    def __init__(self, name):
        Container.__init__(self, name)

    def makeDescriptionStr(self, makeDetailed=False):
        outStr = f"You find yourself in a {self.name}. In the room, you see: \n"
        for obj in self.contains:
            outStr += '\n'.join(["\t" + desc for desc in obj.makeDescriptionStr().strip().split('\n')]) + '\n'
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
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.gameOver = False
        self.gameWon = False
        self.numSteps = 0
        self.score = 0

    def initializeWorld(self):
        world = Room("room")

        world.addObject(self.agent)

        stone = Stone("stone", 50, 100)
        world.addObject(stone)

        measuring_cup = MeasuringCup("measuring cup", 500)
        world.addObject(measuring_cup)

        scale = Scale("scale")
        world.addObject(scale)

        sink = Sink("sink", 100)
        world.addObject(sink)

        return world

    def getTaskDescription(self):
        return 'Your task is to measure the density of a stone. You have a measuring cup, a scale, and a sink with water.'

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

        self.addAction("answer", ["answer"])

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
        if obj.getProperty("isActivatable"):
            obsStr, success = obj.turnOn()
            return obsStr
        else:
            return "You can't turn on that."

    def actionTurnOff(self, obj):
        if obj.getProperty("isActivatable"):
            obsStr, success = obj.turnOff()
            return obsStr
        else:
            return "You can't turn off that."

    def actionUse(self, deviceObj, patientObject):
        if deviceObj.getProperty("isUsable"):
            obsStr, _ = deviceObj.useWithObject(patientObject)
            return obsStr
        else:
            return "You can't use that."

    def actionAnswer(self):
        stone = None
        measuring_cup = None
        for obj in self.agent.contains:
            if obj.name == "stone":
                stone = obj
            if obj.name == "measuring cup":
                measuring_cup = obj

        if stone is not None and measuring_cup is not None:
            if measuring_cup.properties["containsLiquid"]:
                water_volume = measuring_cup.properties["containedVolume"]
                stone_volume = stone.properties["volume"]
                stone_weight = stone.properties["weight"]
                density = stone_weight / stone_volume
                self.gameOver = True
                self.gameWon = True
                return f"The density of the stone is {density} grams per milliliter."
            else:
                return "You haven't filled the measuring cup with water yet."
        else:
            return "You need to have both the stone and the measuring cup in your inventory to answer."

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
            deviceObj = action[1]
            patientObj = action[2]
            self.observationStr = self.actionUse(deviceObj, patientObj)
        elif (actionVerb == "answer"):
            self.observationStr = self.actionAnswer()
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
            self.score = 1

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
