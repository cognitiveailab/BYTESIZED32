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


class VendingMachine(Container):
    def __init__(self, name):
        GameObject.__init__(self, name)
        Container.__init__(self, name)
        self.properties["isMoveable"] = False
        self.properties["total_money_received"] = 0

    def insertCoin(self, coin):
        if not isinstance(coin, Coin):
            return "You can't insert that into the vending machine."

        self.properties["total_money_received"] += coin.value
        return f"You inserted a {coin.name} into the vending machine."

    def selectSnack(self, snack):
        if not isinstance(snack, Snack):
            return "That's not a snack you can select."

        if self.properties["total_money_received"] < snack.price:
            return "You don't have enough money to buy that snack."

        self.properties["total_money_received"] -= snack.price
        return f"You bought a {snack.name} from the vending machine."


class Coin(GameObject):
    def __init__(self, name, value):
        GameObject.__init__(self, name)
        self.value = value

    def makeDescriptionStr(self, makeDetailed=False):
        return f"a {self.name} worth {self.value}"


class Snack(GameObject):
    def __init__(self, name, price):
        GameObject.__init__(self, name)
        self.price = price

    def makeDescriptionStr(self, makeDetailed=False):
        return f"a {self.name} with a price of {self.price}"


class Room(Container):
    def __init__(self, name):
        GameObject.__init__(self, name)
        Container.__init__(self, name)
        self.properties["isMoveable"] = False

    def makeDescriptionStr(self, makeDetailed=False):
        outStr = f"You find yourself in a {self.name}. In the {self.name}, you see: \n"
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
        self.observationStr = self.rootObject.makeDescriptionStr(self.current_room)
        self.calculateScore()

    def initializeWorld(self):
        world = World()

        room = Room("room")
        world.addObject(room)

        vending_machine = VendingMachine("vending machine")
        room.addObject(vending_machine)

        coin1 = Coin("coin1", 1)
        coin2 = Coin("coin2", 2)
        coin5 = Coin("coin5", 5)
        room.addObject(coin1)
        room.addObject(coin2)
        room.addObject(coin5)

        snack1 = Snack("snack1", 3)
        snack2 = Snack("snack2", 6)
        vending_machine.addObject(snack1)
        vending_machine.addObject(snack2)

        room.addObject(self.agent)
        self.current_room = room

        return world

    def getTaskDescription(self):
        return "Your task is to buy a snack from a vending machine with some coins."

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
                self.addAction("insert " + objReferent + " into vending machine", ["insert", obj])

        for objReferent, objs in allObjects.items():
            for obj in objs:
                self.addAction("select " + objReferent, ["select", obj])

        return self.possibleActions

    def addAction(self, actionStr, actionArgs):
        if not (actionStr in self.possibleActions):
            self.possibleActions[actionStr] = []
        self.possibleActions[actionStr].append(actionArgs)

    def actionTake(self, obj):
        if (obj.parentContainer == None):
            return "Something has gone wrong -- that object is dangling in the void.  You can't take that."

        obsStr, objRef, success = obj.parentContainer.takeObjectFromContainer(obj)
        if (success == False):
            return obsStr

        self.agent.addObject(obj)
        return obsStr + " You put the " + obj.getReferents()[0] + " in your inventory."

    def actionInsert(self, obj):
        if not isinstance(obj, Coin):
            return "You can't insert that into the vending machine."

        vending_machine = None
        for item in self.current_room.contains:
            if isinstance(item, VendingMachine):
                vending_machine = item
                break

        if vending_machine is None:
            return "There is no vending machine to insert the coin into."

        obsStr, objRef, success = obj.parentContainer.takeObjectFromContainer(obj)
        if (success == False):
            return obsStr

        return vending_machine.insertCoin(obj)

    def actionSelect(self, obj):
        if not isinstance(obj, Snack):
            return "You can't select that."

        vending_machine = None
        for item in self.current_room.contains:
            if isinstance(item, VendingMachine):
                vending_machine = item
                break

        if vending_machine is None:
            return "There is no vending machine to select the snack from."

        return vending_machine.selectSnack(obj)

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
        elif (actionVerb == "insert"):
            thingToInsert = action[1]
            self.observationStr = self.actionInsert(thingToInsert)
        elif (actionVerb == "select"):
            thingToSelect = action[1]
            self.observationStr = self.actionSelect(thingToSelect)
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
        if self.gameOver:
            self.score = 0
            return

        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        for obj in allObjects:
            if isinstance(obj, Snack) and obj.parentContainer == self.agent:
                self.score = 1
                self.gameOver = True
                self.gameWon = True
                return

        self.score = 0

def main():
    randomSeed = 0

    game = TextGame(randomSeed=randomSeed)

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
