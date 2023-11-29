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
    def __init__(self, name):
        Container.__init__(self, name)
        self.properties["isContainer"] = True
        self.properties["isOpenable"] = False
        self.properties["isOpen"] = True
        self.properties["cold"] = False

    def makeDescriptionStr(self, makeDetailed=False):
        outStr = "You are in a "
        if self.properties["cold"]:
            outStr += "cold "
        outStr += self.name + "."
        return outStr

class Clothes(GameObject):
    def __init__(self, name, cold_resistance):
        GameObject.__init__(self, name)
        self.properties["cold_resistance"] = cold_resistance
        self.properties["isWorn"] = False

    def makeDescriptionStr(self, makeDetailed=False):
        outStr = "a " + self.name
        if self.properties["isWorn"]:
            outStr += " (worn)"
        outStr += "."
        return outStr

class Agent(Container):
    def __init__(self):
        GameObject.__init__(self, "agent")
        Container.__init__(self, "agent")
        self.properties["warmth"] = 0

    def getReferents(self):
        return ["yourself"]

    def makeDescriptionStr(self, makeDetailed=False):
        return "yourself"

class World(Container):
    def __init__(self):
        Container.__init__(self, "world")

    def makeDescriptionStr(self, makeDetailed=False):
        outStr = "You find yourself in a world. In the world, you see: \n"
        for obj in self.contains:
            outStr += "\t" + obj.makeDescriptionStr() + "\n"
        return outStr

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

        living_room = Room("living room")
        living_room.properties["cold"] = False
        world.addObject(living_room)

        outside = Room("outside")
        outside.properties["cold"] = True
        world.addObject(outside)

        down_coat = Clothes("down coat", 5)
        living_room.addObject(down_coat)

        sweater = Clothes("sweater", 2)
        living_room.addObject(sweater)

        return world

    def getTaskDescription(self):
        return "Your task is to keep warm, go outside, and navigate to another house in a cold winter day."

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
                self.addAction("examine " + objReferent, ["examine", obj])

        for objReferent, objs in allObjects.items():
            for obj in objs:
                if obj.getProperty("isMoveable"):
                    self.addAction("take " + objReferent, ["take", obj])

        for objReferent, objs in allObjects.items():
            for obj in objs:
                if obj.getProperty("isContainer"):
                    self.addAction("enter " + objReferent, ["enter", obj])

        for objReferent, objs in allObjects.items():
            for obj in objs:
                if obj.name == "clothes":
                    self.addAction("wear " + objReferent, ["wear", obj])

        return self.possibleActions

    def actionExamine(self, obj):
        return obj.makeDescriptionStr(makeDetailed=True)

    def actionTake(self, obj):
        if obj.parentContainer != self.agent:
            return "You don't currently have the " + obj.getReferents()[0] + " in your inventory."

        obsStr, objRef, success = obj.parentContainer.takeObjectFromContainer(obj)
        if success:
            self.agent.addObject(obj)
            return obsStr + " You put the " + obj.getReferents()[0] + " in your inventory."
        else:
            return obsStr

    def actionEnter(self, obj):
        if obj.getProperty("isContainer"):
            obsStr, success = obj.openContainer()
            if success:
                self.agent.removeSelfFromContainer()
                obj.addObject(self.agent)
                return "You enter the " + obj.getReferents()[0] + "."
            else:
                return obsStr
        else:
            return "You can't enter that."

    def actionWear(self, obj):
        if obj.name == "clothes":
            if obj.properties["isWorn"]:
                return "You are already wearing the " + obj.getReferents()[0] + "."
            else:
                obj.properties["isWorn"] = True
                self.agent.properties["warmth"] += obj.properties["cold_resistance"]
                return "You put on the " + obj.getReferents()[0] + "."
        else:
            return "You can't wear that."

    def actionInventory(self):
        inventory = self.agent.contains
        if len(inventory) == 0:
            return "You have nothing in your inventory."
        else:
            inventory_str = "In your inventory, you have:\n"
            for item in inventory:
                inventory_str += "\t" + item.makeDescriptionStr() + "\n"
            return inventory_str

    def step(self, actionStr):
        self.observationStr = ""
        reward = 0

        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return (self.observationStr, self.score, reward, self.gameOver, self.gameWon)

        self.numSteps += 1

        actions = self.possibleActions[actionStr]
        action = None

        if len(actions) > 1:
            action = actions[0]
        else:
            action = actions[0]

        actionVerb = action[0]

        if actionVerb == "look around":
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif actionVerb == "inventory":
            self.observationStr = self.actionInventory()
        elif actionVerb == "examine":
            thingToExamine = action[1]
            self.observationStr = self.actionExamine(thingToExamine)
        elif actionVerb == "take":
            thingToTake = action[1]
            self.observationStr = self.actionTake(thingToTake)
        elif actionVerb == "enter":
            thingToEnter = action[1]
            self.observationStr = self.actionEnter(thingToEnter)
        elif actionVerb == "wear":
            thingToWear = action[1]
            self.observationStr = self.actionWear(thingToWear)
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
        for obj in allObjects:
            if obj.name == "room" and obj.properties["cold"]:
                self.score -= 1

        if self.agent.properties["warmth"] >= 5:
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

    while not game.gameOver:
        actionStr = ""
        while (len(actionStr) == 0) or (actionStr == "help"):
            actionStr = input("> ")
            if actionStr == "help":
                print("Possible actions: " + str(game.generatePossibleActions().keys()))
                print("")
                actionStr = ""
            elif actionStr == "exit" or actionStr == "quit":
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
