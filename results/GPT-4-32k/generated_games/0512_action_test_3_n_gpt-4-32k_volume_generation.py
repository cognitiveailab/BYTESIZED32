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

class Grill(Container):
    def __init__(self):
        Container.__init__(self, "grill")
        self.properties["isOn"] = False

    def turnOn(self):
        if self.properties["isOn"]:
            return "The grill is already on."
        else:
            self.properties["isOn"] = True
            return "You turn on the grill."

    def turnOff(self):
        if not self.properties["isOn"]:
            return "The grill is already off."
        else:
            self.properties["isOn"] = False
            return "You turn off the grill."

    def grillFood(self, food):
        if not self.properties["isOn"]:
            return "The grill is not on. You need to turn it on first."
        if food.getProperty("is_grilled"):
            return f"The {food.name} is already grilled."
        else:
            food.properties["is_grilled"] = True
            return f"You grill the {food.name}."

class Food(GameObject):
    def __init__(self, name):
        GameObject.__init__(self, name)
        self.properties["is_grilled"] = False
        self.properties["has_salt"] = False
        self.properties["has_oil"] = False

    def addSalt(self):
        if self.properties["has_salt"]:
            return f"The {self.name} already has salt."
        else:
            self.properties["has_salt"] = True
            return f"You add salt to the {self.name}."

    def addOil(self):
        if self.properties["has_oil"]:
            return f"The {self.name} already has oil."
        else:
            self.properties["has_oil"] = True
            return f"You add oil to the {self.name}."

    def eat(self):
        if not self.properties["is_grilled"]:
            return f"The {self.name} is not grilled yet. You can't eat it."
        else:
            return f"You eat the {self.name}. Delicious!"

class Salt(GameObject):
    def __init__(self):
        GameObject.__init__(self, "salt")

class Oil(GameObject):
    def __init__(self):
        GameObject.__init__(self, "oil")

class World(Container):
    def __init__(self):
        Container.__init__(self, "backyard")

    def makeDescriptionStr(self, makeDetailed=False):
        outStr = "You find yourself in a backyard. In the backyard, you see: \n"
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

        grill = Grill()
        world.addObject(grill)

        food1 = Food("steak")
        world.addObject(food1)

        food2 = Food("chicken")
        world.addObject(food2)

        salt = Salt()
        world.addObject(salt)

        oil = Oil()
        world.addObject(oil)

        return world

    def getTaskDescription(self):
        return "Your task is to grill the food, adding salt and oil as needed, and then eat it."

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

        for objReferent, objs in allObjects.items():
            for obj in objs:
                if isinstance(obj, Food):
                    self.addAction(f"add salt to {objReferent}", ["add_salt", obj])
                    self.addAction(f"add oil to {objReferent}", ["add_oil", obj])

        self.addAction("turn on grill", ["turn_on_grill"])
        self.addAction("turn off grill", ["turn_off_grill"])

        for objReferent, objs in allObjects.items():
            for obj in objs:
                if isinstance(obj, Food):
                    self.addAction(f"grill {objReferent}", ["grill", obj])

        for objReferent, objs in allObjects.items():
            for obj in objs:
                if isinstance(obj, Food):
                    self.addAction(f"eat {objReferent}", ["eat", obj])

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
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif (actionVerb == "inventory"):
            self.observationStr = self.actionInventory()
        elif (actionVerb == "examine"):
            thingToExamine = action[1]
            self.observationStr = thingToExamine.makeDescriptionStr(makeDetailed=True)
        elif (actionVerb == "take"):
            thingToTake = action[1]
            self.observationStr = self.actionTake(thingToTake)
        elif (actionVerb == "put"):
            thingToMove = action[1]
            newContainer = action[2]
            self.observationStr = self.actionPut(thingToMove, newContainer)
        elif (actionVerb == "add_salt"):
            food = action[1]
            self.observationStr = food.addSalt()
        elif (actionVerb == "add_oil"):
            food = action[1]
            self.observationStr = food.addOil()
        elif (actionVerb == "turn_on_grill"):
            grill = self.rootObject.containsItemWithName("grill")[0]
            self.observationStr = grill.turnOn()
        elif (actionVerb == "turn_off_grill"):
            grill = self.rootObject.containsItemWithName("grill")[0]
            self.observationStr = grill.turnOff()
        elif (actionVerb == "grill"):
            food = action[1]
            grill = self.rootObject.containsItemWithName("grill")[0]
            self.observationStr = grill.grillFood(food)
        elif (actionVerb == "eat"):
            food = action[1]
            self.observationStr = food.eat()
            if "Delicious" in self.observationStr:
                self.gameOver = True
                self.gameWon = True
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
        if self.gameWon:
            self.score += 1

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
