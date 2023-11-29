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

class Stone(GameObject):
    def __init__(self, volume):
        GameObject.__init__(self, "stone")
        self.properties["volume"] = volume

    def makeDescriptionStr(self, makeDetailed=False):
        return "a " + self.name

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
        else:
            super().addObject(obj)

    def removeObject(self, obj):
        if obj.name == "water":
            self.properties["containsLiquid"] = False
            self.properties["containedVolume"] -= obj.getProperty("volume")
            if self.properties["containedVolume"] < 0:
                self.properties["containedVolume"] = 0
        else:
            super().removeObject(obj)

    def makeDescriptionStr(self, makeDetailed=False):
        main_string = f"a {self.name} with a maximum volume of {self.properties['max_volume']} mL."
        if self.properties["containsLiquid"]:
            state_string = f"It currently contains {self.properties['containedVolume']} mL of water."
        else:
            state_string = "It is currently empty."

        return f"{main_string} {state_string}"

class Scale(GameObject):
    def __init__(self, name):
        GameObject.__init__(self, name)
        self.properties["isMoveable"] = False
        self.properties["weight"] = 0

    def addObject(self, obj):
        self.properties["weight"] += obj.getProperty("weight")

    def removeObject(self, obj):
        self.properties["weight"] -= obj.getProperty("weight")

    def makeDescriptionStr(self, makeDetailed=False):
        return f"a {self.name} displaying a weight of {self.properties['weight']} grams"

class Sink(Container):
    def __init__(self, name):
        GameObject.__init__(self, name)
        Container.__init__(self, name)
        self.properties["isMoveable"] = False
        self.properties["water_out_per_tick"] = 100
        self.properties["isOn"] = False

    def tick(self):
        if self.properties["isOn"]:
            water = Water(self.properties["water_out_per_tick"])
            self.addObject(water)

    def turnOn(self):
        self.properties["isOn"] = True
        return f"The {self.name} is now on."

    def turnOff(self):
        self.properties["isOn"] = False
        return f"The {self.name} is now off."

    def makeDescriptionStr(self, makeDetailed=False):
        main_string = f"a {self.name}."
        if self.properties["isOn"]:
            state_string = "It is currently running."
        else:
            state_string = "It is currently off."

        return f"{main_string} {state_string}"

class Water(GameObject):
    def __init__(self, volume):
        GameObject.__init__(self, "water")
        self.properties["volume"] = volume
        self.properties["isMoveable"] = False

    def makeDescriptionStr(self, makeDetailed=False):
        return f"{self.properties['volume']} mL of " + self.name

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

        stone = Stone(volume=self.random.randint(50, 200))
        world.addObject(stone)

        measuring_cup = MeasuringCup("measuring cup", 500)
        world.addObject(measuring_cup)

        scale = Scale("scale")
        world.addObject(scale)

        sink = Sink("sink")
        world.addObject(sink)

        return world

    def getTaskDescription(self):
        return "Your task is to measure the density of the stone. Use the actions to manipulate the objects in the room."

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

        for sink in allObjects["sink"]:
            self.addAction("turn on sink", ["turn on", sink])
            self.addAction("turn off sink", ["turn off", sink])

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

        elif (actionVerb == "take"):
            thingToTake = action[1]
            self.observationStr = self.actionTake(thingToTake)
        elif (actionVerb == "put"):
            thingToMove = action[1]
            newContainer = action[2]
            self.observationStr = self.actionPut(thingToMove, newContainer)
        elif (actionVerb == "turn on"):
            sink = action[1]
            self.observationStr = sink.turnOn()
        elif (actionVerb == "turn off"):
            sink = action[1]
            self.observationStr = sink.turnOff()

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

        stone = self.rootObject.containsItemWithName("stone")[0]
        measuring_cup = self.rootObject.containsItemWithName("measuring cup")[0]
        scale = self.rootObject.containsItemWithName("scale")[0]

        if stone.parent == scale:
            self.score += 1

        if measuring_cup.properties["containsLiquid"]:
            self.score += 1

        if stone.parent == measuring_cup:
            self.score += 1
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
