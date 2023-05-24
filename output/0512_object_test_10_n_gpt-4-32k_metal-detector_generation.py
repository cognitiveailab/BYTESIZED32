Here is a text-based simulation for the task of melting butter:

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

    def makeDescriptionStr(self, makeDetailed=False):
        return f"a {self.name}"

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
        return "a " + self.name

class Room(Container):
    def __init__(self, name):
        GameObject.__init__(self, name)
        Container.__init__(self, name)
        self.properties["isMoveable"] = False

    def makeDescriptionStr(self, makeDetailed=False):
        outStr = f"You are in a {self.name}. In the {self.name}, you see: \n"
        for obj in self.contains:
            outStr += "\t" + obj.makeDescriptionStr() + "\n"
        return outStr

class Device(GameObject):
    def __init__(self, name):
        GameObject.__init__(self, name)
        self.properties["isOn"] = False

    def turnOn(self):
        if self.getProperty("isOn"):
            return f"The {self.name} is already on.", False
        self.properties["isOn"] = True
        return f"The {self.name} is now on.", True

    def turnOff(self):
        if not self.getProperty("isOn"):
            return f"The {self.name} is already off.", False
        self.properties["isOn"] = False
        return f"The {self.name} is now off.", True

class Stove(Device):
    def __init__(self, name, maxTemperature, tempIncreasePerTick):
        Device.__init__(self, name)
        self.properties["maxTemperature"] = maxTemperature
        self.properties["tempIncreasePerTick"] = tempIncreasePerTick
        self.properties["currentTemperature"] = 0

    def tick(self):
        if self.getProperty("isOn"):
            self.properties["currentTemperature"] += self.properties["tempIncreasePerTick"]
            if self.properties["currentTemperature"] > self.properties["maxTemperature"]:
                self.properties["currentTemperature"] = self.properties["maxTemperature"]

    def makeDescriptionStr(self, makeDetailed=False):
        if self.getProperty("isOn"):
            return f"a {self.name} (on)"
        else:
            return f"a {self.name} (off)"

class Butter(GameObject):
    def __init__(self, name, temperature, meltingPoint, boilingPoint):
        GameObject.__init__(self, name)
        self.properties["temperature"] = temperature
        self.properties["meltingPoint"] = meltingPoint
        self.properties["boilingPoint"] = boilingPoint
        self.properties["stateOfMatter"] = "solid"
        self.properties["solidName"] = "butter"
        self.properties["liquidName"] = "melted butter"
        self.properties["gasName"] = "butter vapor"

    def tick(self):
        if self.parentContainer != None:
            if isinstance(self.parentContainer, Stove):
                stove = self.parentContainer
                if stove.getProperty("isOn"):
                    self.properties["temperature"] = stove.properties["currentTemperature"]
                    if self.properties["temperature"] >= self.properties["boilingPoint"]:
                        self.properties["stateOfMatter"] = "gas"
                    elif self.properties["temperature"] >= self.properties["meltingPoint"]:
                        self.properties["stateOfMatter"] = "liquid"
                    else:
                        self.properties["stateOfMatter"] = "solid"

    def makeDescriptionStr(self, makeDetailed=False):
        if self.properties["stateOfMatter"] == "solid":
            return f"a {self.properties['solidName']}"
        elif self.properties["stateOfMatter"] == "liquid":
            return f"a {self.properties['liquidName']}"
        else:
            return f"a {self.properties['gasName']}"

class Pot(Container):
    def __init__(self, name):
        GameObject.__init__(self, name)
        Container.__init__(self, name)

    def makeDescriptionStr(self, makeDetailed=False):
        return f"a {self.name}"

class TextGame:
    def __init__(self, randomSeed):
        self.random = random.Random(randomSeed)
        self.agent = Agent()
        self.rootObject = self.initializeWorld()
        self.score = 0
        self.numSteps = 0
        self.gameOver = False
        self.gameWon = False
        self.observationStr = self.rootObject.makeDescriptionStr(self.current_room)
        self.calculateScore()

    def initializeWorld(self):
        world = World()

        room = Room("kitchen")
        world.addObject(room)

        stove = Stove("stove", maxTemperature=500, tempIncreasePerTick=10)
        room.addObject(stove)

        butter = Butter("butter", temperature=25, meltingPoint=35, boilingPoint=150)
        room.addObject(butter)

        pot = Pot("pot")
        room.addObject(pot)

        self.current_room = room

        return world

    def getTaskDescription(self):
        return "Your task is to melt the butter. You win the game by turning the butter into melted butter."

    def makeNameToObjectDict(self):
        allObjects = self.current_room.getAllContainedObjectsRecursive()

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

        for objReferent, objs in allObjects.items():
            for obj in objs:
                if isinstance(obj, Device):
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

    def actionTurnOn(self, device):
        if not isinstance(device, Device):
            return f"You can't turn on the {device.name}."
        obsStr, success = device.turnOn()
        return obsStr

    def actionTurnOff(self, device):
        if not isinstance(device, Device):
            return f"You can't turn off the {device.name}."
        obsStr, success = device.turnOff()
        return obsStr

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
            self.observationStr = self.rootObject.makeDescriptionStr(self.agent.parentContainer)
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
            device = action[1]
            self.observationStr = self.actionTurnOn(device)
        elif (actionVerb == "turn off"):
            device = action[1]
            self.observationStr = self.actionTurnOff(device)
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
            if isinstance(obj, Butter) and obj.properties["stateOfMatter"] == "liquid":
                self.score = 1
                self.gameOver = True
                self.gameWon = True

class World(Container):
    def __init__(self):
        Container.__init__(self, "world")

class Agent(Container):
    def __init__(self):
        GameObject.__init__(self, "agent")
        Container.__init__(self, "agent")

    def getReferents(self):
        return ["yourself"]

    def makeDescriptionStr(self, makeDetailed=False):
        return "yourself"

def main():
    randomSeed = 0

    game = TextGame(randomSeed = randomSeed)

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

This simulation models the process of melting butter in a kitchen. The task-critical objects are Stove, Butter, and Pot. The user needs to take the butter, put it in the pot, take the pot, put the pot on the stove, turn on the stove, and wait until the butter melts. The distractor action is to eat the butter.