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
        self.properties["capacity"] = 3
        self.properties["water"] = 0

    def fill(self, source):
        if source.name == "sink":
            self.properties["water"] = self.properties["capacity"]
            return f"The {self.name} is now full."
        else:
            return f"You can't fill the {self.name} from the {source.name}."

    def pour(self, target):
        if isinstance(target, Pea):
            if self.properties["water"] > 0:
                target.properties["water"] += 1
                self.properties["water"] -= 1
                return f"You watered the {target.name}."
            else:
                return f"The {self.name} is empty."
        else:
            return f"You can't pour water into the {target.name}."

class Sink(GameObject):
    def __init__(self, name):
        GameObject.__init__(self, name)

class FlowerPot(Container):
    def __init__(self, name):
        GameObject.__init__(self, name)
        Container.__init__(self, name)

class Garden(Container):
    def __init__(self):
        Container.__init__(self, "garden")

    def makeDescriptionStr(self, makeDetailed=False):
        description = "You are in a garden. "
        for obj in self.contains:
            description += f"There is {obj.makeDescriptionStr()} {obj.properties['containerPrefix']} the garden. "
        return description

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

        flower_pot = FlowerPot("flower pot")
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
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        self.addAction(f"take {objReferent1}", ["take", obj1])
                        self.addAction(f"put {objReferent1} in {objReferent2}", ["put", obj1, obj2])
                        self.addAction(f"fill {objReferent1} from {objReferent2}", ["fill", obj1, obj2])
                        self.addAction(f"pour {objReferent1} into {objReferent2}", ["pour", obj1, obj2])

        return self.possibleActions

    def actionTake(self, obj):
        if obj.getProperty("isMoveable"):
            obj.removeSelfFromContainer()
            return f"You took the {obj.name}."
        else:
            return f"You can't take the {obj.name}."

    def actionPut(self, obj, target):
        if isinstance(target, Container):
            target.addObject(obj)
            return f"You put the {obj.name} in the {target.name}."
        else:
            return f"You can't put the {obj.name} in the {target.name}."

    def actionFill(self, obj, source):
        if isinstance(obj, Jug):
            return obj.fill(source)
        else:
            return f"You can't fill the {obj.name}."

    def actionPour(self, obj, target):
        if isinstance(obj, Jug):
            return obj.pour(target)
        else:
            return f"You can't pour the {obj.name}."

    def step(self, actionStr):
        self.observationStr = ""

        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return (self.observationStr, self.score, self.gameOver, self.gameWon)

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
        elif (actionVerb == "take"):
            obj = action[1]
            self.observationStr = self.actionTake(obj)
        elif (actionVerb == "put"):
            obj = action[1]
            target = action[2]
            self.observationStr = self.actionPut(obj, target)
        elif (actionVerb == "fill"):
            obj = action[1]
            source = action[2]
            self.observationStr = self.actionFill(obj, source)
        elif (actionVerb == "pour"):
            obj = action[1]
            target = action[2]
            self.observationStr = self.actionPour(obj, target)
        else:
            self.observationStr = "ERROR: Unknown action."

        self.doWorldTick()

        lastScore = self.score
        self.calculateScore()

        return (self.observationStr, self.score, self.gameOver, self.gameWon)

    def doWorldTick(self):
        self.rootObject.tick()
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        for obj in allObjects:
            obj.tick()

    def calculateScore(self):
        self.score = 0
        pea = self.rootObject.containsItemWithName("pea")[0]
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

        observationStr, score, gameOver, gameWon = game.step(actionStr)
        possibleActions = game.generatePossibleActions()

        print("Observation: " + observationStr)
        print("")
        print("Current step: " + str(game.numSteps))
        print("Score: " + str(score))
        print("Game Over: " + str(gameOver))
        print("Game Won: " + str(gameWon))
        print("")
        print("----------------------------------------")

if __name__ == "__main__":
    main()
