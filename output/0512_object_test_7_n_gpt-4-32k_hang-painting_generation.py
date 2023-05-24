Here is the text-based simulation for growing a pea:

```python
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

        self.properties["temperature"] = 20.0

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
    def __init__(self, name, isOpenable=False, isOpen=True, containerPrefix="in"):
        if hasattr(self, "constructorsRun"):
            if "Container" in self.constructorsRun:
                return

        GameObject.__init__(self, name)
        self.constructorsRun.append("Container")

        self.properties["isContainer"] = True
        self.properties["isOpenable"] = isOpenable
        self.properties["isOpen"] = isOpen
        self.properties["containerPrefix"] = containerPrefix

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
        if len(self.contains) == 0:
            return f"an empty {self.name}"
        else:
            outStr = f"a(n) {self.name}, which contains: \n"
            for obj in self.contains:
                outStr += '\n'.join(["\t\t" + desc for desc in obj.makeDescriptionStr().strip().split('\n')]) + '\n'

            return outStr

class Pea(GameObject):
    def __init__(self):
        GameObject.__init__(self, "pea")
        self.properties["stage"] = "seed"
        self.properties["water"] = 0

    def water(self, amount):
        self.properties["water"] += amount
        if self.properties["water"] >= 5 and self.properties["stage"] == "seed":
            self.properties["stage"] = "sprout"
            return "The pea has grown into a sprout."
        elif self.properties["water"] >= 10 and self.properties["stage"] == "sprout":
            self.properties["stage"] = "reproducing"
            return "The pea has grown into its reproducing stage."
        else:
            return "You watered the pea."

    def makeDescriptionStr(self, makeDetailed=False):
        return f"a {self.properties['stage']} {self.name}"

class FlowerPot(Container):
    def __init__(self):
        GameObject.__init__(self, "flower pot")
        Container.__init__(self, "flower pot")

    def makeDescriptionStr(self, makeDetailed=False):
        if len(self.contains) == 0:
            return "an empty flower pot"
        else:
            return f"a flower pot with a {self.contains[0].properties['stage']} {self.contains[0].name}"

class Jug(Container):
    def __init__(self):
        GameObject.__init__(self, "jug")
        Container.__init__(self, "jug")

    def makeDescriptionStr(self, makeDetailed=False):
        return "a jug"

class Sink(GameObject):
    def __init__(self):
        GameObject.__init__(self, "sink", isActivatable=True)
        self.properties["isOn"] = False

    def turn_on(self):
        self.properties["isOn"] = True
        return "The sink is turned on."

    def turn_off(self):
        self.properties["isOn"] = False
        return "The sink is turned off."

    def makeDescriptionStr(self, makeDetailed=False):
        if self.properties["isOn"]:
            return "a sink that is turned on"
        else:
            return "a sink that is turned off"

class Garden(Container):
    def __init__(self):
        Container.__init__(self, "garden")

    def makeDescriptionStr(self, makeDetailed=False):
        outStr = "You find yourself in a garden. In the garden, you see: \n"
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

        self.score = 0
        self.numSteps = 0
        self.gameOver = False
        self.gameWon = False
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.calculateScore()

    def initializeWorld(self):
        world = Garden()

        world.addObject(self.agent)

        pea = Pea()
        world.addObject(pea)

        flower_pot = FlowerPot()
        world.addObject(flower_pot)

        jug = Jug()
        world.addObject(jug)

        sink = Sink()
        world.addObject(sink)

        return world

    def getTaskDescription(self):
        return 'Your task is to grow a pea to its reproducing stage.'

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

        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if obj1 != obj2:
                            containerPrefix = "in"
                            if obj2.properties["isContainer"]:
                                containerPrefix = obj2.properties["containerPrefix"]
                            self.addAction("put " + objReferent1 + " " + containerPrefix + " " + objReferent2, ["put", obj1, obj2])

        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if obj1 != obj2:
                            self.addAction("use " + objReferent1 + " on " + objReferent2, ["use", obj1, obj2])

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

    def actionUse(self, obj1, obj2):
        if type(obj1) == Jug and type(obj2) == Sink:
            if obj2.getProperty("isOn"):
                return "You filled the jug with water."
            else:
                return "The sink is turned off. Turn it on first."
        elif type(obj1) == Jug and type(obj2) == Pea:
            if obj2.parentContainer != None and type(obj2.parentContainer) == FlowerPot:
                return obj2.water(5)
            else:
                return "The pea is not in a flower pot. Put it in a flower pot first."
        elif type(obj1) == Sink:
            if obj1.getProperty("isOn"):
                return obj1.turn_off()
            else:
                return obj1.turn_on()
        else:
            return f"Using {obj1.name} on {obj2.name} has no effect."

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

        if actionVerb == "look around":
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif actionVerb == "inventory":
            self.observationStr = self.actionInventory()
        elif actionVerb == "take":
            thingToTake = action[1]
            self.observationStr = self.actionTake(thingToTake)
        elif actionVerb == "put":
            thingToMove = action[1]
            newContainer = action[2]
            self.observationStr = self.actionPut(thingToMove, newContainer)
        elif actionVerb == "use":
            obj1 = action[1]
            obj2 = action[2]
            self.observationStr = self.actionUse(obj1, obj2)

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
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        for obj in allObjects:
            if type(obj) == Pea:
                if obj.properties["stage"] == "reproducing":
                    self.gameOver = True
                    self.gameWon = True
                    self.score = 1
                elif obj.properties["water"] >= 15:
                    self.gameOver = True
                    self.gameWon = False
                    self.score = 0

def main():
    randomSeed = 0

    game = TextGame(randomSeed=randomSeed)

    print("Task Description: " + game.getTaskDescription())
    print()
    print("Initial Observation: " + game.observationStr)
    print()
    print("Type 'help' for a list of possible actions.")
    print()

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

This simulation allows the user to grow a pea by placing it in a flower pot, filling a jug with water from a sink, and watering the pea until it reaches the reproducing stage. The user can also turn the sink on and off. The game ends when the pea reaches the reproducing stage or if it is overwatered.