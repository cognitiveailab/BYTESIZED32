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
        if obj in self.contains:
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
        outStr = f"You find yourself in a {self.name}.  In the {self.name}, you see: \n"
        for obj in self.contains:
            outStr += "\t" + obj.makeDescriptionStr() + "\n"

        return outStr

class Stone(GameObject):
    def __init__(self, name, volume, weight):
        GameObject.__init__(self, name)
        self.properties["volume"] = volume
        self.properties["weight"] = weight

class MeasuringCup(Container):
    def __init__(self, name, max_volume):
        GameObject.__init__(self, name)
        Container.__init__(self, name)
        self.properties["max_volume"] = max_volume
        self.properties["contained_volume"] = 0
        self.properties["contains_liquid"] = False

    def addObject(self, obj):
        if obj.name == "Water":
            self.properties["contains_liquid"] = True
            self.properties["contained_volume"] += obj.properties["volume"]
            if self.properties["contained_volume"] > self.properties["max_volume"]:
                self.properties["contained_volume"] = self.properties["max_volume"]
        else:
            super().addObject(obj)

    def removeObject(self, obj):
        if obj.name == "Water":
            self.properties["contains_liquid"] = False
            self.properties["contained_volume"] -= obj.properties["volume"]
            if self.properties["contained_volume"] < 0:
                self.properties["contained_volume"] = 0
        else:
            super().removeObject(obj)

class Scale(GameObject):
    def __init__(self, name):
        GameObject.__init__(self, name)
        self.properties["isMoveable"] = False
        self.properties["measured_weight"] = 0

    def addObject(self, obj):
        self.contains.append(obj)
        obj.parentContainer = self
        self.properties["measured_weight"] += obj.properties["weight"]

    def removeObject(self, obj):
        if obj in self.contains:
            self.contains.remove(obj)
            obj.parentContainer = None
            self.properties["measured_weight"] -= obj.properties["weight"]

class Sink(Container):
    def __init__(self, name, water_out_per_tick):
        GameObject.__init__(self, name)
        Container.__init__(self, name)
        self.properties["isMoveable"] = False
        self.properties["water_out_per_tick"] = water_out_per_tick
        self.properties["is_on"] = False

    def tick(self):
        if self.properties["is_on"]:
            water_volume = self.properties["water_out_per_tick"]
            water = Water("Water", water_volume)
            self.addObject(water)

    def turn_on(self):
        self.properties["is_on"] = True
        return "You turn on the sink."

    def turn_off(self):
        self.properties["is_on"] = False
        return "You turn off the sink."

class Water(GameObject):
    def __init__(self, name, volume):
        GameObject.__init__(self, name)
        self.properties["volume"] = volume
        self.properties["isMoveable"] = False

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

        stone = Stone("stone", 100, 500)
        room.addObject(stone)

        measuring_cup = MeasuringCup("measuring cup", 1000)
        room.addObject(measuring_cup)

        scale = Scale("scale")
        room.addObject(scale)

        sink = Sink("sink", 100)
        room.addObject(sink)

        self.agent.parentContainer = room
        self.current_room = room

        return world

    def getTaskDescription(self):
        return "Your task is to measure the density of a stone."

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
                self.addAction("put " + objReferent + " on scale", ["put_on_scale", obj])

        for objReferent, objs in allObjects.items():
            for obj in objs:
                self.addAction("put " + objReferent + " in measuring cup", ["put_in_measuring_cup", obj])

        self.addAction("turn on sink", ["turn_on_sink"])
        self.addAction("turn off sink", ["turn_off_sink"])

        self.addAction("answer", ["answer"])

        return self.possibleActions

    def actionTake(self, obj):
        if (obj.parentContainer == None):
            return "Something has gone wrong -- that object is dangling in the void.  You can't take that."

        obsStr, objRef, success = obj.parentContainer.takeObjectFromContainer(obj)
        if (success == False):
            return obsStr

        self.agent.addObject(obj)
        return obsStr + " You put the " + obj.getReferents()[0] + " in your inventory."

    def actionPutOnScale(self, obj):
        if obj.name != "stone":
            return "You can only put the stone on the scale."

        scale = None
        for obj in self.current_room.contains:
            if obj.name == "scale":
                scale = obj
                break

        if scale is None:
            return "There is no scale in the room."

        scale.addObject(obj)
        self.agent.removeObject(obj)
        return f"You put the {obj.name} on the scale."

    def actionPutInMeasuringCup(self, obj):
        if obj.name != "stone":
            return "You can only put the stone in the measuring cup."

        measuring_cup = None
        for obj in self.current_room.contains:
            if obj.name == "measuring cup":
                measuring_cup = obj
                break

        if measuring_cup is None:
            return "There is no measuring cup in the room."

        measuring_cup.addObject(obj)
        self.agent.removeObject(obj)
        return f"You put the {obj.name} in the measuring cup."

    def actionTurnOnSink(self):
        sink = None
        for obj in self.current_room.contains:
            if obj.name == "sink":
                sink = obj
                break

        if sink is None:
            return "There is no sink in the room."

        return sink.turn_on()

    def actionTurnOffSink(self):
        sink = None
        for obj in self.current_room.contains:
            if obj.name == "sink":
                sink = obj
                break

        if sink is None:
            return "There is no sink in the room."

        return sink.turn_off()

    def actionAnswer(self):
        stone = None
        for obj in self.current_room.contains:
            if obj.name == "stone":
                stone = obj
                break

        if stone is None:
            return "There is no stone in the room."

        measuring_cup = None
        for obj in self.current_room.contains:
            if obj.name == "measuring cup":
                measuring_cup = obj
                break

        if measuring_cup is None:
            return "There is no measuring cup in the room."

        scale = None
        for obj in self.current_room.contains:
            if obj.name == "scale":
                scale = obj
                break

        if scale is None:
            return "There is no scale in the room."

        if stone.parentContainer != measuring_cup:
            return "The stone is not in the measuring cup."

        if not measuring_cup.properties["contains_liquid"]:
            return "The measuring cup does not contain water."

        if stone.parentContainer != scale:
            return "The stone is not on the scale."

        stone_weight = stone.properties["weight"]
        stone_volume = stone.properties["volume"]
        water_volume = measuring_cup.properties["contained_volume"]

        displaced_water_volume = water_volume - stone_volume
        density = stone_weight / displaced_water_volume

        self.gameOver = True
        self.gameWon = True
        return f"The density of the stone is {density}."

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
        elif (actionVerb == "put_on_scale"):
            thingToPut = action[1]
            self.observationStr = self.actionPutOnScale(thingToPut)
        elif (actionVerb == "put_in_measuring_cup"):
            thingToPut = action[1]
            self.observationStr = self.actionPutInMeasuringCup(thingToPut)
        elif (actionVerb == "turn_on_sink"):
            self.observationStr = self.actionTurnOnSink()
        elif (actionVerb == "turn_off_sink"):
            self.observationStr = self.actionTurnOffSink()
        elif (actionVerb == "answer"):
            self.observationStr = self.actionAnswer()
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
            if self.gameWon:
                self.score = 1
            else:
                self.score = 0

class Agent(Container):
    def __init__(self):
        GameObject.__init__(self, "agent")
        Container.__init__(self, "agent")

    def getReferents(self):
        return ["yourself"]

    def makeDescriptionStr(self, makeDetailed=False):
        return "yourself"

class World(Container):
    def __init__(self):
        Container.__init__(self, "world")

    def makeDescriptionStr(self, room, makeDetailed=False):
        outStr = f"You find yourself in a {room.name}.  In the {room.name}, you see: \n"
        for obj in room.contains:
            outStr += "\t" + obj.makeDescriptionStr() + "\n"

        return outStr

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
