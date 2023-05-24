Here is the text-based simulation for the given task:

```python
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

class Room(Container):
    def __init__(self, name):
        Container.__init__(self, name)

    def makeDescriptionStr(self, makeDetailed=False):
        outStr = "You are in the " + self.name + ". You see: "
        for obj in self.contains:
            outStr += obj.makeDescriptionStr() + ", "
        outStr = outStr[:-2] + "."
        return outStr

class Door(Container):
    def __init__(self, name):
        Container.__init__(self, name)
        self.properties["isOpenable"] = True
        self.properties["isOpen"] = False

    def makeDescriptionStr(self, makeDetailed=False):
        outStr = "a " + self.name + " that is "
        if self.properties["isOpen"]:
            outStr += "open."
        else:
            outStr += "closed."
        return outStr

class Coin(GameObject):
    def __init__(self):
        GameObject.__init__(self, "coin")

    def makeDescriptionStr(self, makeDetailed=False):
        return "a coin"

class Box(Container):
    def __init__(self, name):
        Container.__init__(self, name)
        self.properties["isOpenable"] = True
        self.properties["isOpen"] = False

    def makeDescriptionStr(self, makeDetailed=False):
        outStr = "a " + self.name + " that is "
        if self.properties["isOpen"]:
            outStr += "open."
        else:
            outStr += "closed."
        return outStr

class Map(GameObject):
    def __init__(self):
        GameObject.__init__(self, "map")

    def makeDescriptionStr(self, makeDetailed=False):
        return "a map"

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
        world = Room("starting room")

        world.addObject(self.agent)

        coin_room = Room("coin room")
        world.addObject(coin_room)

        answer_box_room = Room("answer box room")
        world.addObject(answer_box_room)

        door1 = Door("door1")
        world.addObject(door1)
        door1.addObject(coin_room)

        door2 = Door("door2")
        world.addObject(door2)
        door2.addObject(answer_box_room)

        coin = Coin()
        coin_room.addObject(coin)

        answer_box = Box("answer box")
        answer_box_room.addObject(answer_box)

        map_obj = Map()
        world.addObject(map_obj)

        return world

    def getTaskDescription(self):
        return "Your task is to navigate to another room, collect a coin and put the coin into an answer box."

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

        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2):
                            self.addAction("move to " + objReferent2, ["move to", obj2])

        for objReferent, objs in allObjects.items():
            for obj in objs:
                self.addAction("read " + objReferent, ["read", obj])

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

        obsStr, objRef, success = obj.parentContainer.takeObjectFromContainer(obj)
        if (success == False):
            return obsStr

        self.agent.addObject(obj)
        return obsStr + " You put the " + obj.getReferents()[0] + " in your inventory."

    def actionExamine(self, obj):
        return obj.makeDescriptionStr(makeDetailed=True)

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

    def actionMoveTo(self, obj):
        if obj.name == "coin room":
            if obj.parentContainer.getProperty("isOpen"):
                self.agent.removeSelfFromContainer()
                obj.addObject(self.agent)
                return "You moved to the coin room."
            else:
                return "The door to the coin room is closed. You can't move there."
        elif obj.name == "answer box room":
            if obj.parentContainer.getProperty("isOpen"):
                self.agent.removeSelfFromContainer()
                obj.addObject(self.agent)
                return "You moved to the answer box room."
            else:
                return "The door to the answer box room is closed. You can't move there."
        else:
            return "You can't move there."

    def actionRead(self, obj):
        if obj.name == "map":
            return "The map shows two rooms: a coin room and an answer box room. There are doors connecting the starting room to both of these rooms."
        else:
            return "You can't read that."

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
        elif (actionVerb == "move to"):
            destination = action[1]
            self.observationStr = self.actionMoveTo(destination)
        elif (actionVerb == "read"):
            thingToRead = action[1]
            self.observationStr = self.actionRead(thingToRead)
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

        foundObjects = self.rootObject.containsItemWithName("answer box")
        if (len(foundObjects) > 0):
            answer_box = foundObjects[0]
            containedItems = answer_box.containsItemWithName("coin")
            if (len(containedItems) > 0):
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
                possibleActions = game.generatePossibleActions()
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
```

This code defines a text-based simulation where the player must navigate to another room, collect a coin, and put the coin into an answer box. The game environment consists of a starting room, a coin room, and an answer box room, connected by doors. The player can perform actions such as looking around, examining objects, opening and closing doors, taking and putting objects, moving between rooms, and reading a map. The game is won when the player successfully places the coin in the answer box.