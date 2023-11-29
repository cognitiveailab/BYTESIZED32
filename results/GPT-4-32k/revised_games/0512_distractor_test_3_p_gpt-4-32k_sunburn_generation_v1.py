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
        self.connects = []

    def makeDescriptionStr(self, makeDetailed=False):
        outStr = f"You find yourself in a {self.name}.  In the {self.name}, you see: \n"
        for obj in self.contains:
            outStr += "\t" + obj.makeDescriptionStr() + "\n"

        return outStr

    def connectsTo(self, room):
        connected = False
        for r in self.connects:
            if r.name == room.name:
                connected = True
                break
        return connected

class World(Container):
    def __init__(self):
        Container.__init__(self, "world")

    def makeDescriptionStr(self, room, makeDetailed=False):
        outStr = f"You find yourself in a {room.name}.  In the {room.name}, you see: \n"
        for obj in room.contains:
            outStr += "\t" + obj.makeDescriptionStr() + "\n"
        outStr += "You also see:\n"
        for connected_room in room.connects:
            outStr += f"\t a way to the {connected_room.name}\n"

        return outStr

class Device(GameObject):
    def __init__(self, name):
        GameObject.__init__(self, name)
        self.properties["isDevice"] = True
        self.properties["isOn"] = False

    def turnOn(self):
        if not self.getProperty("isDevice"):
            return f"The {self.name} is not a device.", False

        if self.getProperty("isOn"):
            return f"The {self.name} is already on.", False

        self.properties["isOn"] = True
        return f"The {self.name} is now on.", True

    def turnOff(self):
        if not self.getProperty("isDevice"):
            return f"The {self.name} is not a device.", False

        if not self.getProperty("isOn"):
            return f"The {self.name} is already off.", False

        self.properties["isOn"] = False
        return f"The {self.name} is now off.", True

class Food(GameObject):
    def __init__(self, name):
        GameObject.__init__(self, name)
        self.properties["isFood"] = True
        self.properties["is_grilled"] = False
        self.properties["has_salt"] = False
        self.properties["has_oil"] = False

    def add_salt(self):
        if not self.getProperty("isFood"):
            return f"The {self.name} is not food.", False

        if self.getProperty("has_salt"):
            return f"The {self.name} already has salt.", False

        self.properties["has_salt"] = True
        return f"Salt has been added to the {self.name}.", True

    def add_oil(self):
        if not self.getProperty("isFood"):
            return f"The {self.name} is not food.", False

        if self.getProperty("has_oil"):
            return f"The {self.name} already has oil.", False

        self.properties["has_oil"] = True
        return f"Oil has been added to the {self.name}.", True

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
        self.observationStr = self.rootObject.makeDescriptionStr(self.agent.parentContainer)
        self.calculateScore()

    def initializeWorld(self):
        world = World()

        backyard = Room("backyard")
        world.addObject(backyard)

        grill = Device("grill")
        backyard.addObject(grill)

        food = Food("food")
        backyard.addObject(food)

        salt = GameObject("salt")
        backyard.addObject(salt)

        oil = GameObject("oil")
        backyard.addObject(oil)

        backyard.addObject(self.agent)

        return world

    def getTaskDescription(self):
        return "Your task is to grill food. You need to add salt and oil to the food, turn on the grill, grill the food, and eat it."

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
                if obj.getProperty("isDevice"):
                    self.addAction("turn on " + objReferent, ["turn on", obj])
                    self.addAction("turn off " + objReferent, ["turn off", obj])

        for objReferent, objs in allObjects.items():
            for obj in objs:
                if obj.getProperty("isFood"):
                    self.addAction("add salt to " + objReferent, ["add salt", obj])
                    self.addAction("add oil to " + objReferent, ["add oil", obj])

        self.addAction("grill food", ["grill food"])
        self.addAction("eat food", ["eat food"])

        return self.possibleActions

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
        elif (actionVerb == "turn on"):
            device = action[1]
            obsStr, success = device.turnOn()
            self.observationStr = obsStr
        elif (actionVerb == "turn off"):
            device = action[1]
            obsStr, success = device.turnOff()
            self.observationStr = obsStr
        elif (actionVerb == "add salt"):
            food = action[1]
            obsStr, success = food.add_salt()
            self.observationStr = obsStr
        elif (actionVerb == "add oil"):
            food = action[1]
            obsStr, success = food.add_oil()
            self.observationStr = obsStr
        elif (actionVerb == "grill food"):
            food = self.agent.containsItemWithName("food")
            grill = self.agent.parentContainer.containsItemWithName("grill")
            if not food or not grill:
                self.observationStr = "You need to have food and be near the grill to grill food."
            elif not grill[0].getProperty("isOn"):
                self.observationStr = "The grill is not on. Turn it on before grilling food."
            else:
                food[0].properties["is_grilled"] = True
                self.observationStr = "You have successfully grilled the food."
        elif (actionVerb == "eat food"):
            food = self.agent.containsItemWithName("food")
            if not food:
                self.observationStr = "You need to have food in your inventory to eat it."
            elif not food[0].getProperty("is_grilled"):
                self.observationStr = "The food is not grilled yet. Grill it before eating."
            else:
                self.observationStr = "You have successfully eaten the grilled food."
                self.gameOver = True
                self.gameWon = True
        else:
            self.observationStr = "ERROR: Unknown action."

        self.doWorldTick()

        lastScore = self.score
        self.calculateScore()
        reward = self.score - lastScore

        return (self.observationStr, self.score, reward, self.gameOver, self.gameWon)

    def actionTake(self, obj):
        if (obj.parentContainer == None):
            return "Something has gone wrong -- that object is dangling in the void.  You can't take that."

        obsStr, objRef, success = obj.parentContainer.takeObjectFromContainer(obj)
        if (success == False):
            return obsStr

        self.agent.addObject(obj)
        return obsStr + " You put the " + obj.getReferents()[0] + " in your inventory."

    def actionInventory(self):
        inventory = self.agent.contains
        if (len(inventory) == 0):
            return"Your inventory is empty."
        else:
            obsStr = "You have the following items in your inventory:\n"
            for obj in inventory:
                obsStr += "\t" + obj.makeDescriptionStr() + "\n"
            return obsStr

    def doWorldTick(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        for obj in allObjects:
            obj.tick()

    def calculateScore(self):
        self.score = 0

        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        for obj in allObjects:
            if (obj.name == "food"):
                if obj.getProperty("is_grilled"):
                    self.score = 1
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
