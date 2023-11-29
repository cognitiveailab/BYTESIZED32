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
        return "the " + self.name + "."

class Stove(Device, Container):
    def __init__(self, name="stove"):
        Device.__init__(self, name)
        Container.__init__(self, name)
        self.properties["temperature_increase_per_tick"] = 5
        self.properties["max_temperature"] = 100

class Fridge(Device, Container):
    def __init__(self, name="fridge"):
        Device.__init__(self, name)
        Container.__init__(self, name)
        self.properties["temperature_decrease_per_tick"] = 5
        self.properties["min_temperature"] = 0

class Pot(Container):
    def __init__(self, name="pot"):
        Container.__init__(self, name)

class Milk(GameObject):
    def __init__(self, name="milk", temperature=5):
        GameObject.__init__(self, name)
        self.properties["temperature"] = temperature

class Thermometer(GameObject):
    def __init__(self, name="thermometer"):
        GameObject.__init__(self, name)

class Baby(GameObject):
    def __init__(self, name="baby"):
        GameObject.__init__(self, name)

class Kitchen(Container):
    def __init__(self):
        Container.__init__(self, "kitchen")

    def makeDescriptionStr(self, makeDetailed=False):
        outStr = "You are in a kitchen. You see: \n"
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
        world = Kitchen()

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
        return "Your task is to heat the milk to a suitable temperature for the baby."

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
                if obj.getProperty("isDevice"):
                    self.addAction("turn on " + objReferent, ["turn on", obj])
                    self.addAction("turn off " + objReferent, ["turn off", obj])

                if obj.getProperty("isContainer"):
                    self.addAction("open " + objReferent, ["open", obj])
                    self.addAction("close " + objReferent, ["close", obj])

                if obj.getProperty("isMoveable"):
                    self.addAction("take " + objReferent, ["take", obj])
                    self.addAction("put " + objReferent, ["put", obj])

                if obj.name == "thermometer":
                    self.addAction("use " + objReferent + " on milk", ["use thermometer", obj])

                if obj.name == "milk":
                    self.addAction("feed baby with " + objReferent, ["feed baby", obj])

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
        elif (actionVerb == "turn on"):
            device = action[1]
            obs, success = device.turnOn()
            self.observationStr = obs
        elif (actionVerb == "turn off"):
            device = action[1]
            obs, success = device.turnOff()
            self.observationStr = obs
        elif (actionVerb == "open"):
            container = action[1]
            obs, success = container.openContainer()
            self.observationStr = obs
        elif (actionVerb == "close"):
            container = action[1]
            obs, success = container.closeContainer()
            self.observationStr = obs
        elif (actionVerb == "take"):
            obj = action[1]
            obs, objRef, success = obj.parentContainer.takeObjectFromContainer(obj)
            if success:
                self.agent.addObject(obj)
            self.observationStr = obs
        elif (actionVerb == "put"):
            obj = action[1]
            obs, success = self.rootObject.placeObjectInContainer(obj)
            if success:
                self.agent.removeObject(obj)
            self.observationStr = obs        elif (actionVerb == "use thermometer"):
            thermometer = action[1]
            milk = self.rootObject.containsItemWithName("milk")[0]
            milk_temp = milk.getProperty("temperature")
            self.observationStr = f"The milk temperature is {milk_temp} degrees."
        elif (actionVerb == "feed baby"):
            milk = action[1]
            milk_temp = milk.getProperty("temperature")
            if 35 <= milk_temp <= 40:
                self.observationStr = "You successfully fed the baby with the milk."
                self.gameOver = True
                self.gameWon = True
            else:
                self.observationStr = "The milk temperature is not suitable for the baby."

        tick_output_strs = self.doWorldTick()
        if len(tick_output_strs) > 0:
            self.observationStr = '\n'.join([self.observationStr] + tick_output_strs)
        lastScore = self.score
        self.calculateScore()
        reward = self.score - lastScore

        return (self.observationStr, self.score, reward, self.gameOver, self.gameWon)

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

        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        for obj in allObjects:
            if obj.name == "baby" and self.gameWon:
                self.score += 1

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
