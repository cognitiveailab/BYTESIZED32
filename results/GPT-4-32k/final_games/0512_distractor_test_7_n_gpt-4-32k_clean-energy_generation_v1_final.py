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

class Pea(GameObject):
    def __init__(self, name):
        GameObject.__init__(self, name)
        self.properties["stage"] = "seed"
        self.properties["water"] = 0

    def tick(self):
        if self.properties["water"] > 0:
            self.properties["water"] -= 1
            if self.properties["stage"] == "seed":
                self.properties["stage"] = "sprout"
            elif self.properties["stage"] == "sprout":
                self.properties["stage"] = "flowering"
            elif self.properties["stage"] == "flowering":
                self.properties["stage"] = "reproducing"

    def makeDescriptionStr(self, makeDetailed=False):
        return f"a {self.properties['stage']} pea"

class Jug(Container):
    def __init__(self, name):
        GameObject.__init__(self, name)
        Container.__init__(self, name)
        self.properties["isOpenable"] = True
        self.properties["isOpen"] = True
        self.properties["containerPrefix"] = "in"

class Sink(GameObject):
    def __init__(self, name):
        GameObject.__init__(self, name)
        self.properties["isOn"] = False

    def turnOn(self):
        self.properties["isOn"] = True
        return "The sink is now on."

    def turnOff(self):
        self.properties["isOn"] = False
        return "The sink is now off."

class Garden(Container):
    def __init__(self):
        Container.__init__(self, "garden")

    def makeDescriptionStr(self, makeDetailed=False):
        outStr = "You are in a garden. "
        for obj in self.contains:
            outStr += "There is " + obj.makeDescriptionStr() + " here. "
        return outStr

class TextGame:
    def __init__(self, randomSeed):
        self.random = random.Random(randomSeed)
        self.rootObject = self.initializeWorld()
        self.score = 0
        self.numSteps = 0
        self.gameOver = False
        self.gameWon = False
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.calculateScore()

    def initializeWorld(self):
        garden = Garden()

        pea = Pea("pea")
        garden.addObject(pea)

        flower_pot = Container("flower pot")
        garden.addObject(flower_pot)

        jug = Jug("jug")
        garden.addObject(jug)

        sink = Sink("sink")
        garden.addObject(sink)

        return garden

    def getTaskDescription(self):
        return "Your task is to grow a pea. You have a pea seed, a flower pot, a jug, and a sink."

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

        for objReferent1, objs1 in allObjects.items():
            for obj1 in objs1:
                if obj1.getProperty("isContainer"):
                    self.addAction("examine " + objReferent1, ["examine", obj1])
                    self.addAction("look in " + objReferent1, ["examine", obj1])
                    self.addAction("look at " + objReferent1, ["examine", obj1])

                    if obj1.getProperty("isOpenable"):
                        if obj1.getProperty("isOpen"):
                            self.addAction("close " + objReferent1, ["close", obj1])
                        else:
                            self.addAction("open " + objReferent1, ["open", obj1])

                    if obj1.getProperty("isOpen"):
                        for objReferent2, objs2 in allObjects.items():
                            for obj2 in objs2:
                                if obj2.getProperty("isMoveable"):
                                    if obj2.parentContainer == obj1:
                                        self.addAction("take " + objReferent2 + " from " + objReferent1, ["take", obj2, obj1])
                                    else:
                                        self.addAction("put " + objReferent2 + " in " + objReferent1, ["put", obj2, obj1])

                if isinstance(obj1, Sink):
                    if obj1.getProperty("isOn"):
                        self.addAction("turn off " + objReferent1, ["turn off", obj1])
                    else:
                        self.addAction("turn on " + objReferent1, ["turn on", obj1])

                if isinstance(obj1, Jug) and obj1.getProperty("isOpen"):
                    for objReferent2, objs2 in allObjects.items():
                        for obj2 in objs2:
                            if isinstance(obj2, Sink) and obj2.getProperty("isOn"):
                                self.addAction("fill " + objReferent1 + " with water from " + objReferent2, ["fill", obj1, obj2])

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
        elif (actionVerb == "examine"):
            obj = action[1]
            self.observationStr = "You examine " + obj.makeDescriptionStr() + ". "
            if obj.getProperty("isContainer"):
                if obj.getProperty("isOpen"):
                    self.observationStr += "It is open. "
                else:
                    self.observationStr += "It is closed. "
                if len(obj.contains) > 0:
                    self.observationStr += "It contains: "
                    for containedObj in obj.contains:
                        self.observationStr += containedObj.makeDescriptionStr() + ", "
                else:
                    self.observationStr += "It is empty. "
        elif (actionVerb == "open"):
            obj = action[1]
            self.observationStr, success = obj.openContainer()
        elif (actionVerb == "close"):
            obj = action[1]
            self.observationStr, success = obj.closeContainer()
        elif (actionVerb == "take"):
            obj = action[1]
            container = action[2]
            self.observationStr, obj, success = container.takeObjectFromContainer(obj)
            if success:
                self.rootObject.addObject(obj)
        elif (actionVerb == "put"):
            obj = action[1]
            container = action[2]
            self.observationStr, success = container.placeObjectInContainer(obj)
        elif (actionVerb == "turn on"):
            obj = action[1]
            self.observationStr = obj.turnOn()
        elif (actionVerb == "turn off"):
            obj = action[1]
            self.observationStr = obj.turnOff()
        elif (actionVerb == "fill"):
            jug = action[1]
            sink = action[2]
            water = GameObject("water")
            jug.addObject(water)
            self.observationStr = "You fill the jug with water from the sink."
        else:
            self.observationStr = "ERROR: Unknown action."

        self.doWorldTick()

        lastScore = self.score
        self.calculateScore()
        reward = self.score - lastScore

        return (self.observationStr, self.score, reward, self.gameOver, self.gameWon)

    def doWorldTick(self):
        self.rootObject.tick()
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        for obj in allObjects:
            obj.tick()

    def calculateScore(self):
        self.score = 0
        pea = self.rootObject.containsItemWithName("pea")
        if pea:
            pea = pea[0]
            if pea.properties["stage"] == "reproducing":
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
