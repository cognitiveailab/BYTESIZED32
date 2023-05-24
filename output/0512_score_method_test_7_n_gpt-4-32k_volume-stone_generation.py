Here is the text-based simulation for growing a pea:

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
        return ("", obj, True)

    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

class Pea(GameObject):
    def __init__(self, stage, water):
        GameObject.__init__(self, "pea")
        self.properties["stage"] = stage
        self.properties["water"] = water

    def tick(self):
        if self.parentContainer is not None and self.parentContainer.name == "flower pot":
            if self.properties["water"] > 0:
                self.properties["water"] -= 1
                self.properties["stage"] += 1
                if self.properties["stage"] >= 100:
                    self.properties["stage"] = 100
                    return "The pea has grown to the reproducing stage."
            else:
                self.properties["stage"] -= 1
                if self.properties["stage"] <= 0:
                    self.properties["stage"] = 0
                    return "The pea has withered and died due to lack of water."

    def makeDescriptionStr(self, makeDetailed=False):
        stage_str = "seed"
        if self.properties["stage"] >= 100:
            stage_str = "reproducing"
        elif self.properties["stage"] >= 50:
            stage_str = "growing"
        return f"a pea ({stage_str})"

class FlowerPot(Container):
    def __init__(self):
        Container.__init__(self, "flower pot")

    def makeDescriptionStr(self, makeDetailed=False):
        outStr = "a flower pot"
        if len(self.contains) == 0:
            outStr += " that is empty"
        else:
            outStr += " containing a " + self.contains[0].makeDescriptionStr()
        return outStr

class Jug(Container):
    def __init__(self, volume):
        Container.__init__(self, "jug")
        self.properties["volume"] = volume

    def makeDescriptionStr(self, makeDetailed=False):
        return "a jug"

class Sink(Container):
    def __init__(self, water_out_per_tick, isOn=False):
        GameObject.__init__(self, "sink")
        Container.__init__(self, "sink")

        self.properties["containerPrefix"] = "in"
        self.properties["isActivatable"] = True
        self.properties["isMoveable"] = False
        self.properties["isOn"] = isOn
        self.properties["water_out_per_tick"] = water_out_per_tick

    def tick(self):
        containedObjects = self.getAllContainedObjectsRecursive()
        if self.properties["isOn"]:
            for obj in containedObjects:
                if obj.getProperty("isWaterContainer"):
                    foundObjects = obj.containsItemWithName("water")
                    if len(foundObjects) == 0:
                        water = Water(min(obj.getProperty("volume"), self.properties["water_out_per_tick"]))
                        obj.addObject(water)
                    else:
                        foundObjects[0].properties["volume"] = min(obj.getProperty("volume"), foundObjects[0].properties["volume"] + self.properties["water_out_per_tick"])

    def makeDescriptionStr(self, makeDetailed=False):
        outStr = "a sink"

        if self.properties["isOn"]:
            outStr += " that is currently on"
        else:
            outStr += " that is currently off"

        if len(self.contains) == 0:
            outStr += " and that is empty"
        else:
            if not makeDetailed:
                outStr += " and that contains one or more items."
            else:
                outStr += " and that contains the following items: \n"
                for obj in self.contains:
                    outStr += "\t" + obj.makeDescriptionStr() + "\n"

        return outStr

    def turnOn(self):
        if (self.getProperty("isActivatable") == False):
            return ("It's not clear how the " + self.getReferents()[0] + " could be turned on.", False)

        if self.properties["isOn"]:
            return ("The " + self.getReferents()[0] + " is already on.", False)
        else:
            self.properties["isOn"] = True
            return ("The " + self.getReferents()[0] + " is now turned on.", True)

    def turnOff(self):
        if (self.getProperty("isActivatable") == False):
            return ("It's not clear how the " + self.getReferents()[0] + " could be turned off.", False)

        if not self.properties["isOn"]:
            return ("The " + self.getReferents()[0] + " is already off.", False)
        else:
            self.properties["isOn"] = False
            return ("The " + self.getReferents()[0] + " is now turned off.", True)

class Water(GameObject):
    def __init__(self, volume):
        GameObject.__init__(self, "water")
        self.properties["isLiquid"] = True
        self.properties["volume"] = volume

    def getReferents(self):
        return [f"water in {self.parentContainer.name}"]

    def makeDescriptionStr(self, makeDetailed=False):
        return f"water"

class World(Container):
    def __init__(self):
        Container.__init__(self, "garden")

    def makeDescriptionStr(self, makeDetailed=False):
        outStr = "You are in a garden. In the garden, you see: \n"
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

        pea = Pea(stage=0, water=0)
        world.addObject(pea)

        flower_pot = FlowerPot()
        world.addObject(flower_pot)

        jug = Jug(volume=1000)
        world.addObject(jug)

        sink = Sink(water_out_per_tick=500)
        world.addObject(sink)

        return world

    def getTaskDescription(self):
        return "Your task is to grow a pea to the reproducing stage."

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

        self.addAction("examine", ["examine"])

        for objReferent, objs in allObjects.items():
            for obj in objs:
                self.addAction("take " + objReferent, ["take", obj])
                self.addAction("take " + objReferent + " from " + obj.parentContainer.getReferents()[0], ["take", obj])

        for objReferent, objs in allObjects.items():
            for obj in objs:
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

        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2):
                            self.addAction("pour " + objReferent1 + " into " + objReferent2, ["pour", obj1, obj2])

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

    def actionPour(self, water, target):
        if water.name != "water":
            return f"Cannot pour {water.name}."
        elif target.getProperty("isWaterContainer") == False:
            referent = water.getReferents()[0]
            water.removeSelfFromContainer()
            del water
            return f"{referent} is poured."
        else:
            if water.parentContainer.getProperty("volume") > target.getProperty("volume"):
                water.properties["volume"] = water.parentContainer.getProperty("volume") - target.getProperty("volume")
                extra_water = Water(target.getProperty("volume"))
                target.addObject(extra_water)
            else:
                water.removeSelfFromContainer()
                target.addObject(water)

            return f"You pour {water.getReferents()[0]} into {target.name}"

    def actionTurnOn(self, obj):
        if (obj.getProperty("isActivatable") == False):
            return ("It's not clear how the " + obj.getReferents()[0] + " could be turned on.", False)

        if self.properties["isOn"]:
            return ("The " + obj.getReferents()[0] + " is already on.", False)
        else:
            self.properties["isOn"] = True
            return ("The " + obj.getReferents()[0] + " is now turned on.", True)

    def actionTurnOff(self, obj):
        if (obj.getProperty("isActivatable") == False):
            return ("It's not clear how the " + obj.getReferents()[0] + " could be turned off.", False)

        if not self.properties["isOn"]:
            return ("The " + obj.getReferents()[0] + " is already off.", False)
        else:
            self.properties["isOn"] = False
            return ("The " + obj.getReferents()[0] + " is now turned off.", True)

    def doWorldTick(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        output_strs = []
        for obj in allObjects:
            tick_output_str = obj.tick()
            if tick_output_str is not None:
                output_strs.append(tick_output_str)
        return output_strs

    def calculateScore(self):
        self.score = 0

        pea = None
        for obj in self.rootObject.getAllContainedObjectsRecursive():
            if obj.name == "pea":
                pea = obj
                break

        if pea is not None and pea.properties["stage"] == 100:
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
```

This simulation allows the user to grow a pea by taking the pea seed, putting it in a flower pot, and watering it using a jug filled with water from a sink. The user must water the pea on time until it reaches the reproducing stage.