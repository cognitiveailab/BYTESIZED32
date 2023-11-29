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
        return ("The " + obj.getReferents()[0] + " is removed from the " + self.name + ".", obj, True)

    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

class Stone(GameObject):
    def __init__(self, name, volume, weight):
        GameObject.__init__(self, name)
        self.properties["volume"] = volume
        self.properties["weight"] = weight

    def makeDescriptionStr(self, makeDetailed=False):
        return f"a {self.name}"

class MeasuringCup(Container):
    def __init__(self, name, max_volume):
        GameObject.__init__(self, name)
        Container.__init__(self, name)
        self.properties["max_volume"] = max_volume
        self.properties["containedVolume"] = 0
        self.properties["containsLiquid"] = False
        self.properties["containerPrefix"] = "in"

    def addObject(self, obj):
        if obj.name == "Water":
            self.properties["containsLiquid"] = True
            self.properties["containedVolume"] += obj.getProperty("volume")
            if self.properties["containedVolume"] > self.properties["max_volume"]:
                self.properties["containedVolume"] = self.properties["max_volume"]
        else:
            super().addObject(obj)

    def removeObject(self, obj):
        if obj.name == "Water":
            self.properties["containsLiquid"] = False
            self.properties["containedVolume"] -= obj.getProperty("volume")
            if self.properties["containedVolume"] < 0:
                self.properties["containedVolume"] = 0
        else:
            super().removeObject(obj)

    def makeDescriptionStr(self, makeDetailed=False):
        if self.properties["containsLiquid"]:
            return f"a {self.name} containing {self.properties['containedVolume']}ml of water"
        else:
            return f"an empty {self.name}"

class Scale(Container):
    def __init__(self):
        GameObject.__init__(self, "scale")
        Container.__init__(self, "scale")
        self.properties['isMoveable'] = False
        self.properties["containerPrefix"] = "on"

    def makeDescriptionStr(self, makeDetailed=False):
        if len(self.contains) == 0:
            return "a scale which reads 0g"
        else:
            total_weights = 0
            outStr = "contains "
            for i in range(len(self.contains)):
                if (i == len(self.contains) - 1) and (len(self.contains) > 1):
                    outStr += "and "
                outStr += self.contains[i].makeDescriptionStr() + ", "
                total_weights += self.contains[i].getProperty("weight")

            outStr = outStr[:-2]
            return f"a scale which reads {total_weights}g and {outStr}"

class Sink(Container):
    def __init__(self):
        GameObject.__init__(self, "sink")
        Container.__init__(self, "sink")
        self.properties["isMoveable"] = False
        self.properties["isOpenable"] = False
        self.properties["isOpen"] = True
        self.properties["containerPrefix"] = "in"
        self.properties["water_out_per_tick"] = 100
        self.properties["isOn"] = False

    def tick(self):
        if self.properties["isOn"]:
            water_volume = self.properties["water_out_per_tick"]
            water = Water("Water", water_volume)
            self.addObject(water)

    def makeDescriptionStr(self, makeDetailed=False):
        if self.properties["isOn"]:
            return "a sink with water running"
        else:
            return "a sink"

class Water(GameObject):
    def __init__(self, name, volume):
        GameObject.__init__(self, name)
        self.properties["volume"] = volume

    def makeDescriptionStr(self, makeDetailed=False):
        return f"{self.properties['volume']}ml of water"

class World(Container):
    def __init__(self):
        Container.__init__(self, "room")

    def makeDescriptionStr(self, makeDetailed=False):
        outStr = "You find yourself in a room. In the room, you see: \n"
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
        self.answer_density = None
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

        stone_volume = self.random.randint(50, 150)
        stone_weight = self.random.randint(100, 300)
        stone = Stone("Stone", stone_volume, stone_weight)
        world.addObject(stone)

        measuring_cup = MeasuringCup("measuring cup", 500)
        world.addObject(measuring_cup)

        scale = Scale()
        world.addObject(scale)

        sink = Sink()
        world.addObject(sink)

        self.target_density = stone_weight / stone_volume

        return world

    def getTaskDescription(self):
        return "Your task is to figure out the density of the stone."

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

        for i in range(1, 10):
            self.addAction(f"answer {i}", ["answer", i])

        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2):
                            containerPrefix = "in"
                            if obj2.properties["isContainer"]:
                                containerPrefix = obj2.properties["containerPrefix"]
                            self.addAction("put " + objReferent1 + " " + containerPrefix + " " + objReferent2, ["put", obj1, obj2])

        self.addAction("turn on sink", ["turn on", "sink"])
        self.addAction("turn off sink", ["turn off", "sink"])

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
        obsStr1, objRef,success = objToMove.parentContainer.takeObjectFromContainer(objToMove)
        if (success == False):
            return obsStr1

        obsStr2, success = newContainer.placeObjectInContainer(objToMove)
        if (success == False):
            originalContainer.addObject(objToMove)
            return obsStr2

        return obsStr1 + "\n" + obsStr2

    def actionAnswer(self, density):
        self.answer_density = density
        return f"You believe the density of the stone is {density}g/ml."

    def actionInventory(self):
        inventory = self.agent.contains
        if (len(inventory) == 0):
            return "Your inventory is empty."
        else:
            obsStr = "You have the following items in your inventory:\n"
            for obj in inventory:
                obsStr += "\t" + obj.makeDescriptionStr() + "\n"
            return obsStr

    def actionTurnOn(self, obj_name):
        if obj_name == "sink":
            self.rootObject.containsItemWithName("sink")[0].properties["isOn"] = True
            return "You turn on the sink."
        else:
            return "You can't turn that on."

    def actionTurnOff(self, obj_name):
        if obj_name == "sink":
            self.rootObject.containsItemWithName("sink")[0].properties["isOn"] = False
            return "You turn off the sink."
        else:
            return "You can't turn that off."

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
            self.observationStr = thingToExamine.makeDescriptionStr(makeDetailed=True)
        elif (actionVerb == "take"):
            thingToTake = action[1]
            self.observationStr = self.actionTake(thingToTake)
        elif (actionVerb == "put"):
            thingToMove = action[1]
            newContainer = action[2]
            self.observationStr = self.actionPut(thingToMove, newContainer)
        elif (actionVerb == "answer"):
            answer = action[1]
            self.observationStr = self.actionAnswer(answer)
        elif (actionVerb == "turn on"):
            obj_name = action[1]
            self.observationStr = self.actionTurnOn(obj_name)
        elif (actionVerb == "turn off"):
            obj_name = action[1]
            self.observationStr = self.actionTurnOff(obj_name)
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

        if self.answer_density is not None:
            if round(self.target_density, 1) == round(self.answer_density, 1):
                self.score += 1
                self.gameOver = True
                self.gameWon = True
            else:
                self.score = 0
                self.gameOver = True
                self.gameWon = False

def main():
    randomSeed = 1

    game = TextGame(randomSeed=randomSeed)

    possibleActions = game.generatePossibleActions()
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
                print("Possible actions: " + str(possibleActions.keys()))
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
