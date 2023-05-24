Here is the text-based simulation for the task of opening a box whose cover is fixed by screws with a screwdriver:

```python
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

class Screw(GameObject):
    def __init__(self, name):
        GameObject.__init__(self, name)
        self.properties["is_screw"] = True
        self.properties["is_screwed"] = True

    def unscrew(self):
        if self.properties["is_screwed"]:
            self.properties["is_screwed"] = False
            return f"The {self.name} is now unscrewed.", True
        else:
            return f"The {self.name} is already unscrewed.", False

    def screw(self):
        if not self.properties["is_screwed"]:
            self.properties["is_screwed"] = True
            return f"The {self.name} is now screwed.", True
        else:
            return f"The {self.name} is already screwed.", False

class Screwdriver(GameObject):
    def __init__(self, name):
        GameObject.__init__(self, name)
        self.properties["is_screwdriver"] = True

class Box(Container):
    def __init__(self, name):
        Container.__init__(self, name)
        self.properties["isOpenable"] = True
        self.properties["isOpen"] = False

class Coin(GameObject):
    def __init__(self, name):
        GameObject.__init__(self, name)

class Hammer(GameObject):
    def __init__(self, name):
        GameObject.__init__(self, name)

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

        box = Box("box")
        world.addObject(box)

        screw1 = Screw("screw1")
        screw2 = Screw("screw2")
        screw3 = Screw("screw3")
        screw4 = Screw("screw4")
        box.addObject(screw1)
        box.addObject(screw2)
        box.addObject(screw3)
        box.addObject(screw4)

        screwdriver = Screwdriver("screwdriver")
        world.addObject(screwdriver)

        hammer = Hammer("hammer")
        world.addObject(hammer)

        coin = Coin("coin")
        box.addObject(coin)

        return world

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

        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("is_screw") and obj2.getProperty("is_screwdriver")):
                            self.addAction(f"unscrew {objReferent1} with {objReferent2}", ["unscrew", obj1, obj2])
                            self.addAction(f"screw {objReferent1} with {objReferent2}", ["screw", obj1, obj2])

        for objReferent, objs in allObjects.items():
            for obj in objs:
                if obj.getProperty("isOpenable"):
                    self.addAction(f"open {objReferent}", ["open", obj])
                    self.addAction(f"close {objReferent}", ["close", obj])

        return self.possibleActions

    def actionTake(self, obj):
        if (obj.parent == None):
            return "Something has gone wrong -- that object is dangling in the void.  You can't take that."

        obsStr, objRef, success = obj.parent.takeObjectFromContainer(obj)
        if (success == False):
            return obsStr

        self.agent.addObject(obj)
        return obsStr + " You put the " + obj.getReferents()[0] + " in your inventory."

    def actionPut(self, objToMove, newContainer):
        if (newContainer.getProperty("isContainer") == False):
            return "You can't put things in the " + newContainer.getReferents()[0] + "."

        if (objToMove.parent != self.agent):
            return "You don't currently have the " + objToMove.getReferents()[0] + " in your inventory."

        originalContainer = objToMove.parent
        obsStr1, objRef, success = objToMove.parent.takeObjectFromContainer(objToMove)
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

    def actionUnscrew(self, screw, screwdriver):
        if not screw.getProperty("is_screw") or not screwdriver.getProperty("is_screwdriver"):
            return "You can't unscrew the screw with that object."

        obsStr, success = screw.unscrew()
        return obsStr

    def actionScrew(self, screw, screwdriver):
        if not screw.getProperty("is_screw") or not screwdriver.getProperty("is_screwdriver"):
            return "You can't screw the screw with that object."

        obsStr, success = screw.screw()
        return obsStr

    def actionOpen(self, obj):
        if not obj.getProperty("isOpenable"):
            return f"The {obj.name} can't be opened."

        if obj.getProperty("isOpen"):
            return f"The {obj.name} is already open."

        allObjects = obj.getAllContainedObjectsRecursive()
        for o in allObjects:
            if o.getProperty("is_screw") and o.getProperty("is_screwed"):
                return f"You can't open the {obj.name} because there are still screws attached."

        obj.properties["isOpen"] = True
        return f"The {obj.name} is now open."

    def actionClose(self, obj):
        if not obj.getProperty("isOpenable"):
            return f"The {obj.name} can't be closed."

        if not obj.getProperty("isOpen"):
            return f"The {obj.name} is already closed."

        obj.properties["isOpen"] = False
        return f"The {obj.name} is now closed."

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
        elif (actionVerb == "unscrew"):
            screw, screwdriver = action[1:]
            self.observationStr = self.actionUnscrew(screw, screwdriver)
        elif (actionVerb == "screw"):
            screw, screwdriver = action[1:]
            self.observationStr = self.actionScrew(screw, screwdriver)
        elif (actionVerb == "open"):
            obj = action[1]
            self.observationStr = self.actionOpen(obj)
        elif (actionVerb == "close"):
            obj = action[1]
            self.observationStr = self.actionClose(obj)
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

        allObjects = self.rootObject.getAllContainedObjectsRecursive()

        box_open = False
        coin_in_inventory = False

        for obj in allObjects:
            if type(obj) == Box and obj.getProperty("isOpen"):
                box_open = True
            if type(obj) == Coin and obj.parent == self.agent:
                coin_in_inventory = True

        if box_open:
            self.score += 1
        if coin_in_inventory:
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
```

This simulation models the task of opening a box whose cover is fixed by screws with a screwdriver. The user can take objects, put objects, unscrew screws, open and close the box. The goal is to open the box and take the coin inside. There is a distractor object, a hammer, which does not help in completing the task.