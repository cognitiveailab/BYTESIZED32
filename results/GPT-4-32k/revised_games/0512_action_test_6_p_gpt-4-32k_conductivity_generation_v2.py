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

class ElectricalObject(GameObject):
    def __init__(self, name, conductive=True):
        GameObject.__init__(self, name)
        self.properties["is_electrical_object"] = True
        self.properties["conductive"] = conductive
        self.connects = {"terminal1": (None, None), "terminal2": (None, None)}

    def disconnect(self, terminal):
        if self.connects[terminal][0] is not None:
            obj_connects_to, connected_terminal = self.connects[terminal]
            obj_connects_to.connects[connected_terminal] = (None, None)
        self.connects[terminal] = (None, None)

    def makeDescriptionStr(self, makeDetailed=False):
        terminal1, terminal2 = self.connects.keys()
        if self.connects[terminal1][0] is None and self.connects[terminal2][0] is None:
            return f"a {self.name}"
        elif self.connects[terminal1][0] is None and self.connects[terminal2][0]:
            return f"a {self.name} connecting to {self.connects[terminal2][0].name} {self.connects[terminal2][1]}"
        elif self.connects[terminal1][0] and self.connects[terminal2][0] is None:
            return f"a {self.name} connecting to {self.connects[terminal1][0].name} {self.connects[terminal1][1]}"
        else:
            return f"a {self.name} connecting to {self.connects[terminal1][0].name} {self.connects[terminal1][1]} and {self.connects[terminal2][0].name} {self.connects[terminal2][1]}"

class LED(ElectricalObject):
    def __init__(self, name):
        ElectricalObject.__init__(self, name, True)
        self.properties['on'] = False

    def connectsToBattery(self):
        found_battery = False
        is_good_circuit = True
        current_obj = self
        current_terminal = 'terminal1'
        while True:
            next_obj, next_terminal = current_obj.connects[current_terminal]
            if next_obj is None:
                is_good_circuit = False
                break
            elif not next_obj.getProperty("conductive"):
                is_good_circuit = False
                break
            elif next_obj == self:
                break
            else:
                if type(next_obj) == Battery:
                    found_battery = True
                for key in next_obj.connects:
                    if key != next_terminal:
                        next_terminal = key
                        break
                current_obj = next_obj
                current_terminal = next_terminal

        if found_battery and is_good_circuit:
            return True
        else:
            return False

    def tick(self):
        if self.connectsToBattery():
            self.properties['on'] = True
        else:
            self.properties['on'] = False

    def makeDescriptionStr(self, makeDetailed=False):
        if self.properties["on"]:
            state_desc = f"a {self.name} which is on"
        else:
            state_desc = f"a {self.name} which is off"
        terminal1, terminal2 = self.connects.keys()
        if self.connects[terminal1][0] is None and self.connects[terminal2][0] is None:
            return f"{state_desc}"
        elif self.connects[terminal1][0] is None and self.connects[terminal2][0]:
            return f"{state_desc} and connects to {self.connects[terminal2][0].name} {self.connects[terminal2][1]}"
        elif self.connects[terminal1][0] and self.connects[terminal2][0] is None:
            return f"{state_desc} and connects to {self.connects[terminal1][0].name} {self.connects[terminal1][1]}"
        else:
            return f"{state_desc} and connects to {self.connects[terminal1][0].name} {self.connects[terminal1][1]} and {self.connects[terminal2][0].name} {self.connects[terminal2][1]}"

class Battery(ElectricalObject):
    def __init__(self, name):
        ElectricalObject.__init__(self, name, True)
        self.connects = {"cathode": (None, None), "anode": (None, None)}

class Wire(ElectricalObject):
    def __init__(self, name):
        ElectricalObject.__init__(self, name, True)
        self.properties["is_wire"] = True

class World(Container):
    def __init__(self):
        Container.__init__(self, "workshop")

    def makeDescriptionStr(self, makeDetailed=False):
        outStr = "You find yourself in a workshop. In the workshop, you see: \n"
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

        led = LED("LED")
        world.addObject(led)

        wire1 = Wire("red wire")
        wire2 = Wire("black wire")
        wire3 = Wire("blue wire")
        world.addObject(wire1)
        world.addObject(wire2)
        world.addObject(wire3)

        battery = Battery("battery")
        world.addObject(battery)

        return world

    def getTaskDescription(self):
        return "Your task is to light up an LED. To do this, you need to connect the battery anode to the LED anode with a wire, and connect the battery cathode to the LED cathode with a wire."

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
                            self.addAction("put " + objReferent1 + " " + containerPrefix + " " + objReferent2, ["put",obj1, obj2])

        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("is_electrical_object") and obj2.getProperty("is_electrical_object")):
                            for terminal_1 in obj1.connects:
                                for terminal_2 in obj2.connects:
                                    self.addAction(f"connect {objReferent1} {terminal_1} to {objReferent2} {terminal_2}", ["connect", obj1, terminal_1, obj2, terminal_2])

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

        elif (actionVerb == "take"):
            thingToTake = action[1]
            self.observationStr = self.actionTake(thingToTake)
        elif (actionVerb == "put"):
            thingToMove = action[1]
            newContainer = action[2]
            self.observationStr = self.actionPut(thingToMove, newContainer)
        elif (actionVerb == "connect"):
            obj1, terminal_1, obj2, terminal_2 = action[1:]
            self.observationStr = self.actionConnect(obj1, terminal_1, obj2, terminal_2)
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
            if obj.name == "LED":
                if obj.properties["on"]:
                    self.score += 1
                    self.gameOver = True
                    self.gameWon = True

    def actionConnect(self, obj1, terminal_1, obj2, terminal_2):
        if obj1.connects[terminal_1][0] is not None:
            obj1.disconnect(terminal_1)
        if obj2.connects[terminal_2][0] is not None:
            obj2.disconnect(terminal_2)
        obj1.connects[terminal_1] = (obj2, terminal_2)
        obj2.connects[terminal_2] = (obj1, terminal_1)
        return f"{obj1.name} {terminal_1} is connected to {obj2.name} {terminal_2}."

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
