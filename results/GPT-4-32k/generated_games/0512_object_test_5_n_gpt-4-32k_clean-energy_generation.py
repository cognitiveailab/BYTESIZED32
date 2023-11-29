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

class Room(Container):
    def __init__(self):
        Container.__init__(self, "room")

    def makeDescriptionStr(self, makeDetailed=False):
        outStr = "You are in a room. "
        if len(self.contains) > 0:
            outStr += "You see "
            for i, obj in enumerate(self.contains):
                if i > 0:
                    outStr += ", "
                outStr += obj.makeDescriptionStr()
            outStr += "."
        else:
            outStr += "The room is empty."
        return outStr

class Screw(GameObject):
    def __init__(self):
        GameObject.__init__(self, "screw")

class Screwdriver(GameObject):
    def __init__(self):
        GameObject.__init__(self, "screwdriver")

class Box(Container):
    def __init__(self):
        Container.__init__(self, "box")
        self.properties["isOpenable"] = True
        self.properties["isOpen"] = False

class Coin(GameObject):
    def __init__(self):
        GameObject.__init__(self, "coin")

class Hammer(GameObject):
    def __init__(self):
        GameObject.__init__(self, "hammer")

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
        room = Room()

        screwdriver = Screwdriver()
        room.addObject(screwdriver)

        box = Box()
        room.addObject(box)

        for _ in range(4):
            screw = Screw()
            box.addObject(screw)

        coin = Coin()
        box.addObject(coin)

        hammer = Hammer()
        room.addObject(hammer)

        return room

    def getTaskDescription(self):
        return "Your task is to open a box whose cover is fixed by screws with a screwdriver."

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

        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        self.addAction("take " + objReferent1, ["take", obj1])
                        self.addAction("put " + objReferent1 + " in " + objReferent2, ["put", obj1, obj2])
                        self.addAction("unscrew " + objReferent1 + " with " + objReferent2, ["unscrew", obj1, obj2])
                        self.addAction("open " + objReferent1, ["open", obj1])
                        self.addAction("close " + objReferent1, ["close", obj1])

        return self.possibleActions

    def addAction(self, actionStr, actionArgs):
        if not (actionStr in self.possibleActions):
            self.possibleActions[actionStr] = []
        self.possibleActions[actionStr].append(actionArgs)

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
        elif (actionVerb == "take"):
            obj = action[1]
            resultStr, obj, success = self.rootObject.takeObjectFromContainer(obj)
            self.observationStr = resultStr
            if success:
                self.rootObject.addObject(obj)
        elif (actionVerb == "put"):
            obj = action[1]
            container = action[2]
            resultStr, success = container.placeObjectInContainer(obj)
            self.observationStr = resultStr
        elif (actionVerb == "unscrew"):
            screw = action[1]
            screwdriver = action[2]
            if screwdriver.name == "screwdriver" and screw.name == "screw":
                box = screw.parentContainer
                if box.getProperty("isOpen") == False:
                    box.removeObject(screw)
                    self.rootObject.addObject(screw)
                    self.observationStr = "You unscrewed the screw with the screwdriver."
                else:
                    self.observationStr = "The box is already open."
            else:
                self.observationStr = "You can't unscrew that with that."
        elif (actionVerb == "open"):
            container = action[1]
            resultStr, success = container.openContainer()
            self.observationStr = resultStr
        elif (actionVerb == "close"):
            container = action[1]
            resultStr, success = container.closeContainer()
            self.observationStr = resultStr
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

        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        box_open = False
        coin_in_room = False
        for obj in allObjects:
            if obj.name == "box" and obj.getProperty("isOpen") == True:
                box_open = True
            if obj.name == "coin" and obj.parentContainer.name == "room":
                coin_in_room = True

        if box_open and coin_in_room:
            self.score += 1
            self.gameOver = True
            self.gameWon = True

def main():
    randomSeed = 0

    game = TextGame(randomSeed = randomSeed)

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
