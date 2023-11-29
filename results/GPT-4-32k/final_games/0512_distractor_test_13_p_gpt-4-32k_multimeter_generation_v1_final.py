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

class Room(Container):
    def __init__(self, name):
        Container.__init__(self, name)

class Door(Container):
    def __init__(self, name, is_locked=True, key=None):
        Container.__init__(self, name)
        self.properties["is_locked"] = is_locked
        self.properties["key"] = key

    def unlock(self, key):
        if self.properties["key"] == key:
            self.properties["is_locked"] = False
            return f"The {self.name} is now unlocked.", True
        else:
            return f"The {key.name} doesn't fit the {self.name}.", False

class Key(GameObject):
    def __init__(self, name):
        GameObject.__init__(self, name)

class Drawer(Container):
    def __init__(self, name):
        Container.__init__(self, name)
        self.properties["isOpenable"] = True
        self.properties["isOpen"] = False

class Coin(GameObject):
    def __init__(self, name):
        GameObject.__init__(self, name)

class TextGame:
    def __init__(self, randomSeed):
        self.random = random.Random(randomSeed)
        self.agent = GameObject("agent")
        self.rootObject = self.initializeWorld()
        self.score = 0
        self.numSteps = 0
        self.gameOver = False
        self.gameWon = False
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.calculateScore()

    def initializeWorld(self):
        world = Room("house")

        world.addObject(self.agent)

        room1 = Room("room1")
        room2 = Room("room2")
        room3 = Room("room3")
        world.addObject(room1)
        world.addObject(room2)
        world.addObject(room3)

        door1 = Door("door1", is_locked=True, key="key1")
        door2 = Door("door2", is_locked=True, key="key2")
        room1.addObject(door1)
        room2.addObject(door2)

        key1 = Key("key1")
        key2 = Key("key2")
        room1.addObject(key1)
        room3.addObject(key2)

        drawer1 = Drawer("drawer1")
        drawer2 = Drawer("drawer2")
        room1.addObject(drawer1)
        room2.addObject(drawer2)

        coin = Coin("coin")
        drawer2.addObject(coin)

        return world

    def getTaskDescription(self):
        return "Your task is to find the keys, use keys to open doors to go to another room and collect a coin."

    def generatePossibleActions(self):
        self.possibleActions = {}

        self.addAction("look", ["look"])
        self.addAction("inventory", ["inventory"])

        allObjects = self.makeNameToObjectDict()

        for objReferent, objs in allObjects.items():
            for obj in objs:
                self.addAction("examine " + objReferent, ["examine", obj])

        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if obj1 != obj2:
                            self.addAction("take " + objReferent1 + " from " + objReferent2, ["take", obj1, obj2])

        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if obj1 != obj2:
                            self.addAction("put " + objReferent1 + " in " + objReferent2, ["put", obj1, obj2])

        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if obj1 != obj2:
                            self.addAction("open " + objReferent1 + " with " + objReferent2, ["open", obj1, obj2])

        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if obj1 != obj2:
                            self.addAction("move to " + objReferent1 + " through " + objReferent2, ["move", obj1, obj2])

        return self.possibleActions

    def addAction(self, actionStr, actionArgs):
        if not (actionStr in self.possibleActions):
            self.possibleActions[actionStr] = []
        self.possibleActions[actionStr].append(actionArgs)

    def makeNameToObjectDict(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        nameToObjectDict = {}
        for obj in allObjects:
            for referent in obj.getReferents():
                if referent not in nameToObjectDict:
                    nameToObjectDict[referent] = []
                nameToObjectDict[referent].append(obj)
        return nameToObjectDict

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

        if (actionVerb == "look"):
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif (actionVerb == "inventory"):
            self.observationStr = self.agent.makeDescriptionStr()
        elif (actionVerb == "examine"):
            obj = action[1]
            self.observationStr = obj.makeDescriptionStr()
        elif (actionVerb == "take"):
            obj1, obj2 = action[1], action[2]
            self.observationStr = self.actionTake(obj1, obj2)
        elif (actionVerb == "put"):
            obj1, obj2 = action[1], action[2]
            self.observationStr = self.actionPut(obj1, obj2)
        elif (actionVerb == "open"):
            obj1, obj2 = action[1], action[2]
            self.observationStr = self.actionOpen(obj1, obj2)
        elif (actionVerb == "move"):
            obj1, obj2 = action[1], action[2]
            self.observationStr = self.actionMove(obj1, obj2)
        else:
            self.observationStr = "ERROR: Unknown action."

        self.doWorldTick()

        lastScore = self.score
        self.calculateScore()
        reward = self.score - lastScore

        return (self.observationStr, self.score, reward, self.gameOver, self.gameWon)

    def actionTake(self, obj1, obj2):
        if obj1.parent != obj2:
            return f"The {obj1.name} is not in the {obj2.name}."
        if not obj1.getProperty("isMoveable"):
            return f"The {obj1.name} is not moveable."
        obj1.removeSelfFromContainer()
        self.agent.addObject(obj1)
        return f"You took the {obj1.name} from the {obj2.name}."

    def actionPut(self, obj1, obj2):
        if obj1.parent != self.agent:
            return f"You don't have the {obj1.name} in your inventory."
        if not obj2.getProperty("isContainer"):
            return f"The {obj2.name} is not a container."
        if not obj2.getProperty("isOpen"):
            return f"The {obj2.name} is closed."
        obj1.removeSelfFromContainer()
        obj2.addObject(obj1)
        return f"You put the {obj1.name} in the {obj2.name}."

    def actionOpen(self, obj1, obj2):
        if obj1.parent != obj2:
            return f"The {obj1.name} is not in the {obj2.name}."
        if not obj1.getProperty("is_locked"):
            return f"The {obj1.name} is already unlocked."
        if obj1.getProperty("key") != obj2.name:
            return f"The {obj2.name} doesn't fit the {obj1.name}."
        obj1.properties["is_locked"] = False
        return f"The {obj1.name} is now unlocked."

    def actionMove(self, obj1, obj2):
        if obj1.parent != obj2:
            return f"The {obj1.name} is not connected to the {obj2.name}."
        if obj1.getProperty("is_locked"):
            return f"The {obj1.name} is locked."
        obj1.removeSelfFromContainer()
        self.agent.addObject(obj1)
        return f"You moved to the {obj1.name} through the {obj2.name}."

    def doWorldTick(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        for obj in allObjects:
            obj.tick()

    def calculateScore(self):
        self.score = 0
        if self.agent.containsItemWithName("coin"):
            self.score += 1
            self.gameOver = True
            self.gameWon = True

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
        while ((len(actionStr) ==0) or (actionStr == "help")):
            actionStr = input("> ")
            if (actionStr == "help"):
                possibleActions = game.generatePossibleActions()
                print("Possible actions: " + str(possibleActions.keys()))
                print("")
                actionStr = ""
            elif (actionStr == "exit") or (actionStr == "quit"):
                return

        observationStr, score, reward, gameOver, gameWon = game.step(actionStr)

        possibleActions = game.generatePossibleActions()

        print("Observation: " + observationStr)
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
