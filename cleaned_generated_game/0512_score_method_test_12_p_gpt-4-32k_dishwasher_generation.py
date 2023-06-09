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

class Device(GameObject):
    def __init__(self, name):
        if hasattr(self, "constructorsRun"):
            if "Device" in self.constructorsRun:
                return
        GameObject.__init__(self, name)
        self.constructorsRun.append("Device")

        self.properties["isDevice"] = True
        self.properties["isActivatable"] = True
        self.properties["isOn"] = False

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

    def useWithObject(self, patientObject):
        return ("You're not sure how to use the " + self.getReferents()[0] + " with the " + patientObject.name + ".", False)

    def makeDescriptionStr(self, makeDetailed=False):
        outStr = "The " + self.name + ", which is currently "
        if self.properties["isOn"]:
            outStr += "on."
        else:
            outStr += "off."
        return outStr

class VendingMachine(Container, Device):
    def __init__(self):
        GameObject.__init__(self, "vending machine")
        Container.__init__(self, "vending machine")
        Device.__init__(self, "vending machine")

        self.properties["isOpenable"] = False
        self.properties["isMoveable"] = False
        self.properties["total_money_received"] = 0

    def addObject(self, obj):
        if obj.name == "coin":
            self.properties["total_money_received"] += obj.value
            return "You inserted a " + obj.getReferents()[0] + " into the vending machine."
        else:
            return "You can't insert that into the vending machine."

    def select_snack(self, snack):
        if snack.price <= self.properties["total_money_received"]:
            self.properties["total_money_received"] -= snack.price
            return "You selected the " + snack.getReferents()[0] + " and it is now dispensed.", True
        else:
            return "You don't have enough money to buy the " + snack.getReferents()[0] + ".", False

    def makeDescriptionStr(self, makeDetailed=False):
        return "a vending machine."

class Coin(GameObject):
    def __init__(self, name, value):
        GameObject.__init__(self, name)
        self.value = value

    def makeDescriptionStr(self, makeDetailed=False):
        return "a " + self.name

class Snack(GameObject):
    def __init__(self, name, price):
        GameObject.__init__(self, name)
        self.price = price

    def makeDescriptionStr(self, makeDetailed=False):
        return "a " + self.name + " (price: " + str(self.price) + ")"

class Room(Container):
    def __init__(self):
        Container.__init__(self, "room")

    def makeDescriptionStr(self, makeDetailed=False):
        outStr = "You find yourself in a room. In the room, you see: \n"
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
        world = Room()

        world.addObject(self.agent)

        vending_machine = VendingMachine()
        world.addObject(vending_machine)

        coin1 = Coin("quarter", 25)
        world.addObject(coin1)

        coin2 = Coin("dime", 10)
        world.addObject(coin2)

        snack1 = Snack("chocolate bar", 35)
        vending_machine.addObject(snack1)

        snack2 = Snack("bag of chips", 50)
        vending_machine.addObject(snack2)

        return world

    def getTaskDescription(self):
        return "Your task is to buy a snack from the vending machine."

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

    def generatePossibleActions(self):
        allObjects = self.makeNameToObjectDict()

        self.possibleActions = {}

        self.addAction("look around", ["look around"])
        self.addAction("look", ["look around"])

        self.addAction("inventory", ["inventory"])

        for objReferent, objs in allObjects.items():
            for obj in objs:
                self.addAction("examine " + objReferent, ["examine", obj])

        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2):
                            self.addAction("insert " + objReferent1 + " into " + objReferent2, ["insert", obj1, obj2])
                            self.addAction("select " + objReferent1 + " from " + objReferent2, ["select", obj1, obj2])

        return self.possibleActions

    def actionExamine(self, obj):
        return obj.makeDescriptionStr(makeDetailed=True)

    def actionInsert(self, obj1, obj2):
        if obj1.name == "coin" and obj2.name == "vending machine":
            return obj2.addObject(obj1)
        else:
            return "You can't insert that into the vending machine."

    def actionSelect(self, snack, vending_machine):
        if snack.name in ["chocolate bar", "bag of chips"] and vending_machine.name == "vending machine":
            obsStr, success = vending_machine.select_snack(snack)
            if success:
                self.gameOver = True
                self.gameWon = True
            return obsStr
        else:
            return "You can't select that from the vending machine."

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
        elif (actionVerb == "insert"):
            thingToInsert = action[1]
            target = action[2]
            self.observationStr = self.actionInsert(thingToInsert, target)
        elif (actionVerb == "select"):
            snack = action[1]
            vending_machine = action[2]
            self.observationStr = self.actionSelect(snack, vending_machine)
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
        self.score = -self.numSteps
        if self.gameWon:
            self.score += 100

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
