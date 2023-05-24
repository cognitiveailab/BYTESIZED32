Here is the text-based simulation for the task of heating milk to a suitable temperature for a baby using a stove:

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

class Device(GameObject):
    def __init__(self, name):
        if hasattr(self, "constructorsRun"):
            if "Device" in self.constructorsRun:
                return

        GameObject.__init__(self, name)
        self.constructorsRun.append("Device")

        self.properties["isDevice"] = True
        self.properties["isOn"] = False

    def turnOn(self):
        if not self.getProperty("isDevice"):
            return ("The " + self.name + " is not a device.", False)

        if self.getProperty("isOn"):
            return ("The " + self.name + " is already on.", False)

        self.properties["isOn"] = True
        return ("The " + self.name + " is now on.", True)

    def turnOff(self):
        if not self.getProperty("isDevice"):
            return ("The " + self.name + " is not a device.", False)

        if not self.getProperty("isOn"):
            return ("The " + self.name + " is already off.", False)

        self.properties["isOn"] = False
        return ("The " + self.name + " is now off.", True)

    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name

class Stove(Device):
    def __init__(self):
        Device.__init__(self, "stove")
        self.properties["temperature_increase_per_tick"] = 5
        self.properties["max_temperature"] = 100

class Fridge(Device):
    def __init__(self):
        Device.__init__(self, "fridge")
        self.properties["temperature_decrease_per_tick"] = 2
        self.properties["min_temperature"] = 0

class Milk(GameObject):
    def __init__(self):
        GameObject.__init__(self, "milk")
        self.properties["temperature"] = 5

    def tick(self):
        if self.parent:
            if isinstance(self.parent, Stove) and self.parent.getProperty("isOn"):
                self.properties["temperature"] += self.parent.getProperty("temperature_increase_per_tick")
                if self.properties["temperature"] > self.parent.getProperty("max_temperature"):
                    self.properties["temperature"] = self.parent.getProperty("max_temperature")
            elif isinstance(self.parent, Fridge) and self.parent.getProperty("isOn"):
                self.properties["temperature"] -= self.parent.getProperty("temperature_decrease_per_tick")
                if self.properties["temperature"] < self.parent.getProperty("min_temperature"):
                    self.properties["temperature"] = self.parent.getProperty("min_temperature")

    def makeDescriptionStr(self, makeDetailed=False):
        return f"the milk (temperature: {self.properties['temperature']}°C)"

class Pot(Container):
    def __init__(self):
        Container.__init__(self, "pot")
        self.properties["containerPrefix"] = "on"

class Thermometer(GameObject):
    def __init__(self):
        GameObject.__init__(self, "thermometer")

    def use_on(self, obj):
        if isinstance(obj, Milk):
            return f"The milk's temperature is {obj.properties['temperature']}°C."
        else:
            return "You can only use the thermometer on the milk."

class Baby(GameObject):
    def __init__(self):
        GameObject.__init__(self, "baby")

    def feed(self, obj):
        if isinstance(obj, Milk):
            if 35 <= obj.properties["temperature"] <= 40:
                return "You successfully fed the baby with the milk at the right temperature!"
            else:
                return "The milk's temperature is not suitable for the baby."
        else:
            return "You can only feed the baby with milk."

class World(Container):
    def __init__(self):
        Container.__init__(self, "kitchen")

    def makeDescriptionStr(self, makeDetailed=False):
        outStr = "You find yourself in a kitchen. In the kitchen, you see: \n"
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

        stove = Stove()
        world.addObject(stove)

        fridge = Fridge()
        world.addObject(fridge)

        pot = Pot()
        world.addObject(pot)

        milk = Milk()
        pot.addObject(milk)

        thermometer = Thermometer()
        world.addObject(thermometer)

        baby = Baby()
        world.addObject(baby)

        return world

    def getTaskDescription(self):
        return "Your task is to heat the milk to a suitable temperature for a baby using a stove."

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
                        if (obj1 != obj2):
                            self.addAction("use " + objReferent1 + " on " + objReferent2, ["use", obj1, obj2])

        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2):
                            self.addAction("feed " + objReferent1 + " to " + objReferent2, ["feed", obj1, obj2])

        for objReferent1, objs1 in allObjects.items():
            for obj1 in objs1:
                self.addAction("turn on " + objReferent1, ["turn on", obj1])
                self.addAction("turn off " + objReferent1, ["turn off", obj1])

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

    def actionUse(self, obj1, obj2):
        if isinstance(obj1, Thermometer) and isinstance(obj2, Milk):
            return obj1.use_on(obj2)
        else:
            return "You can't use those objects together."

    def actionFeed(self, obj1, obj2):
        if isinstance(obj1, Milk) and isinstance(obj2, Baby):
            return obj2.feed(obj1)
        else:
            return "You can't feed that to the baby."

    def actionTurnOn(self, obj):
        if not obj.getProperty("isDevice"):
            return "You can't turn that on."

        if obj.getProperty("isOn"):
            return "That is already on."

        obj.properties["isOn"] = True
        return f"The {obj.name} is now on."

    def actionTurnOff(self, obj):
        if not obj.getProperty("isDevice"):
            return "You can't turn that off."

        if not obj.getProperty("isOn"):
            return "That is already off."

        obj.properties["isOn"] = False
        return f"The {obj.name} is now off."

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
        elif (actionVerb == "use"):
            obj1 = action[1]
            obj2 = action[2]
            self.observationStr = self.actionUse(obj1, obj2)
        elif (actionVerb == "feed"):
            obj1 = action[1]
            obj2 = action[2]
            self.observationStr = self.actionFeed(obj1, obj2)
        elif (actionVerb == "turn on"):
            obj = action[1]
            self.observationStr = self.actionTurnOn(obj)
        elif (actionVerb == "turn off"):
            obj = action[1]
            self.observationStr = self.actionTurnOff(obj)
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

        milk = self.agent.containsItemWithName("milk")
        if milk:
            milk = milk[0]
            if 35 <= milk.properties["temperature"] <= 40:
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

This simulation allows the user to heat milk to a suitable temperature for a baby using a stove. The user can perform actions such as taking objects, putting objects in containers, turning devices on and off, using a thermometer to check the milk's temperature, and feeding the baby with the milk. The game ends when the user feeds the baby with milk at the correct temperature.