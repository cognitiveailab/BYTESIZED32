# dens-stone.py
# based on conductivity.py
# ruoyao wang (Mar 05/2023)

# Task Description: Create a micro-simulation that models how to measure the density of a stone
# Environment: room
# Task-critical Objects: Stone, MeasuringCup, Scale, Sink, Water
# High-level object classes: Container (MeasuringCup, Sink)
# Critical properties: water_out_per_tick (Sink), volume (Water, MeasuringCup, Stone), containedVolume (MeasuringCup), containsLiquid (MeasuringCup), weight (Stone, MeasuringCup, Water)
# Actions: look, inventory, examine, take/put object, turn on/off, answer
# Distractor Items: Stone
# Distractor Actions: None
# High-level solution procedure: take stone, put stone on scale, look, take measuring cup, put measuring cup in sink, turn on sink, turn off sink, look, take stone, put stone in measuring cup, look, answer

import random

#
# Abstract class for all game objects
#
class GameObject():
    def __init__(self, name):
        # Prevent this constructor from running if it's already been run during multiple inheritance
        if hasattr(self, "constructorsRun"):
            return
        # Otherwise, keep a list of constructors that have already been run
        self.constructorsRun = ["GameObject"]

        self.name = name
        self.parent = None
        self.contains = []
        self.properties = {}

        # Default properties
        self.properties["isContainer"] = False    # By default, objects are not containers
        self.properties["isMoveable"] = True     # By default, objects are moveable

    # Get a property of the object (safely), returning None if the property doesn't exist
    def getProperty(self, propertyName):
        if propertyName in self.properties:
            return self.properties[propertyName]
        else:
            return None

    # Add an object to this container, removing it from its previous container
    def addObject(self, obj):
        obj.removeSelfFromContainer()
        self.contains.append(obj)
        obj.parent = self

    # Remove an object from this container
    def removeObject(self, obj):
        self.contains.remove(obj)
        obj.parent = None

    # Remove the current object from whatever container it's currently in
    def removeSelfFromContainer(self):
        if self.parent != None:
            self.parent.removeObject(self)

    # Get all contained objects, recursively
    def getAllContainedObjectsRecursive(self):
        outList = []
        for obj in self.contains:
            # Add self
            outList.append(obj)
            # Add all contained objects
            outList.extend(obj.getAllContainedObjectsRecursive())
        return outList

    # Get all contained objects that have a specific name (not recursively)
    def containsItemWithName(self, name):
        foundObjects = []
        for obj in self.contains:
            if obj.name == name:
                foundObjects.append(obj)
        return foundObjects

    # Game tick: Perform any internal updates that need to be performed at each step of the game.
    def tick(self):
        pass

    # Get a list of referents (i.e. names that this object can be called by)
    def getReferents(self):
        return [self.name]

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return self.name


#
#   Abstract Game-object Classes
#


# Abstract class for things that can be considered 'containers' (e.g. a drawer, a box, a table, a shelf, etc.)
class Container(GameObject):
    def __init__(self, name):
        # Prevent this constructor from running if it's already been run during multiple inheritance
        if hasattr(self, "constructorsRun"):
            if "Container" in self.constructorsRun:
                return

        GameObject.__init__(self, name)
        # Otherwise, mark this constructor as having been run
        self.constructorsRun.append("Container")

        self.properties["isContainer"] = True
        self.properties["isOpenable"] = False  # Can the container be opened (e.g. a drawer, a door, a box, etc.), or is it always 'open' (e.g. a table, a shelf, etc.)
        self.properties["isOpen"] = True      # Is the container open or closed (if it is openable)
        self.properties["containerPrefix"] = "in" # The prefix to use when referring to the container (e.g. "in the drawer", "on the table", etc.)

    # Try to open the container
    # Returns an observation string, and a success flag (boolean)
    def openContainer(self):
        # First, check to see if this object is openable
        if not self.getProperty("isOpenable"):
            # If not, then it can't be opened
            return ("The " + self.name + " can't be opened.", False)

        # If this object is openable, then check to see if it is already open
        if self.getProperty("isOpen"):
            # If so, then it can't be opened
            return ("The " + self.name + " is already open.", False)

        # If this object is openable and it is closed, then open it
        self.properties["isOpen"] = True
        return ("The " + self.name + " is now open.", True)

    # Try to close the container
    # Returns an observation string, and a success flag (boolean)
    def closeContainer(self):
        # First, check to see if this object is openable
        if not (self.getProperty("isOpenable") == True):
            # If not, then it can't be closed
            return ("The " + self.name + " can't be closed.", False)

        # If this object is openable, then check to see if it is already closed
        if not (self.getProperty("isOpen") == True):
            # If so, then it can't be closed
            return ("The " + self.name + " is already closed.", False)

        # If this object is openable and it is open, then close it
        self.properties["isOpen"] = False
        return ("The " + self.name + " is now closed.", True)

    # Try to place the object in a container.
    # Returns an observation string, and a success flag (boolean)
    def placeObjectInContainer(self, obj):
        # First, check to see if this object is a container
        if not (self.getProperty("isContainer") == True):
            # If not, then it can't be placed in a container
            return ("The " + self.name + " is not a container, so things can't be placed there.", False)

        # Check to see if the object is moveable
        if not (obj.getProperty("isMoveable") == True):
            # If not, then it can't be removed from a container
            return ("The " + obj.name + " is not moveable.", None, False)

        # If this object is a container, then check to see if it is open
        if not (self.getProperty("isOpen") == True):
            # If not, then it can't be placed in a container
            return ("The " + self.name + " is closed, so things can't be placed there.", False)

        # If this object is a container and it is open, then place the object in the container
        self.addObject(obj)
        return ("The " + obj.getReferents()[0] + " is placed in the " + self.name + ".", True)

    # Try to remove the object from a container.
    # Returns an observation string, a reference to the object being taken, and a success flag (boolean)
    def takeObjectFromContainer(self, obj):
        # First, check to see if this object is a container
        if not (self.getProperty("isContainer") == True):
            # If not, then it can't be removed from a container
            return ("The " + self.name + " is not a container, so things can't be removed from it.", None, False)

        # Check to see if the object is moveable
        if not (obj.getProperty("isMoveable") == True):
            # If not, then it can't be removed from a container
            return ("The " + obj.name + " is not moveable.", None, False)

        # If this object is a container, then check to see if it is open
        if not (self.getProperty("isOpen") == True):
            # If not, then it can't be removed from a container
            return ("The " + self.name + " is closed, so things can't be removed from it.", None, False)

        # Check to make sure that the object is contained in this container
        if obj not in self.contains:
            return ("The " + obj.name + " is not contained in the " + self.name + ".", None, False)

        # If this object is a container and it is open, then remove the object from the container
        obj.removeSelfFromContainer()
        return ("The " + obj.getReferents()[0] + " is removed from the " + self.name + ".", obj, True)

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name

# A game object with a volume
class VolumeObject(GameObject):
    def __init__(self, name, volume):
        GameObject.__init__(self, name)
        self.properties["volume"] = volume

    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name

# A game object with a weight
class WeightObject(GameObject):
    def __init__(self, name, weight):
        GameObject.__init__(self, name)
        self.properties["weight"] = weight

    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name

# A game object with a volume and a weight
class VolumeWeightObject(VolumeObject, WeightObject):
    def __init__(self, name, volume, weight):
        VolumeObject.__init__(self, name, volume)
        WeightObject.__init__(self, name, weight)

    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name

# A game object with a volume and a weight, and a contained volume
class ContainerVolumeWeightObject(VolumeWeightObject, Container):
    def __init__(self, name, volume, weight, containedVolume):
        VolumeWeightObject.__init__(self, name, volume, weight)
        Container.__init__(self, name)
        self.properties["containedVolume"] = containedVolume

    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name

# A game object with a volume and a weight, and a contained volume, and a contains liquid flag
class ContainerVolumeWeightObject(VolumeWeightObject, Container):
    def __init__(self, name, volume, weight, containedVolume, containsLiquid):
        VolumeWeightObject.__init__(self, name, volume, weight)
        Container.__init__(self, name)
        self.properties["containedVolume"] = containedVolume
        self.properties["containsLiquid"] = containsLiquid

    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name

# A game object with a volume and a weight, and a contained volume, and a contains liquid flag, and a water out per tick
class ContainerVolumeWeightObject(VolumeWeightObject, Container):
    def __init__(self, name, volume, weight, containedVolume, containsLiquid, waterOutPerTick):
        VolumeWeightObject.__init__(self, name, volume, weight)
        Container.__init__(self, name)
        self.properties["containedVolume"] = containedVolume
        self.properties["containsLiquid"] = containsLiquid
        self.properties["waterOutPerTick"] = waterOutPerTick

    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name

# A game object with a volume and a weight, and a contained volume, and a contains liquid flag, and a water out per tick, and a is on flag
class ContainerVolumeWeightObject(VolumeWeightObject, Container):
    def __init__(self, name, volume, weight, containedVolume, containsLiquid, waterOutPerTick, isOn):
        VolumeWeightObject.__init__(self, name, volume, weight)
        Container.__init__(self, name)
        self.properties["containedVolume"] = containedVolume
        self.properties["containsLiquid"] = containsLiquid
        self.properties["waterOutPerTick"] = waterOutPerTick
        self.properties["isOn"] = isOn

    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name

# A game object with a volume and a weight, and a contained volume, and a contains liquid flag, and a water out per tick, and a is on flag, and a is answerable flag
class ContainerVolumeWeightObject(VolumeWeightObject, Container):
    def __init__(self, name, volume, weight, containedVolume, containsLiquid, waterOutPerTick, isOn, isAnswerable):
        VolumeWeightObject.__init__(self, name, volume, weight)
        Container.__init__(self, name)
        self.properties["containedVolume"] = containedVolume
        self.properties["containsLiquid"] = containsLiquid
        self.properties["waterOutPerTick"] = waterOutPerTick
        self.properties["isOn"] = isOn
        self.properties["isAnswerable"] = isAnswerable

    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name

# The world is the root object of the game object tree.  In single room environments, it's where all the objects are located.
class World(Container):
    def __init__(self):
        Container.__init__(self, "room")

    def makeDescriptionStr(self, makeDetailed=False):
        outStr = "You find yourself in a room.  In the room, you see: \n"
        for obj in self.contains:
            outStr += "\t" + obj.makeDescriptionStr() + "\n"

        return outStr


# The agent (just a placeholder for a container for the inventory)
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
        # Random number generator, initialized with a seed passed as an argument
        self.random = random.Random(randomSeed)
        # The agent/player
        self.agent = Agent()
        # Game Object Tree
        self.rootObject = self.initializeWorld()
        # Game score
        self.score = 0
        self.numSteps = 0
        # Game over flag
        self.gameOver = False
        self.gameWon = False
        # Last game observation
        self.observationStr = self.rootObject.makeDescriptionStr()
        # Do calculate initial scoring
        self.calculateScore()

    # Create/initialize the world/environment for this game
    def initializeWorld(self):
        world = World()

        # Add the agent
        world.addObject(self.agent)

        # Add a stone
        stone = VolumeWeightObject("stone", 10, 10)
        world.addObject(stone)

        # Add a measuring cup
        measuringCup = ContainerVolumeWeightObject("measuring cup", 10, 10, 0, False)
        world.addObject(measuringCup)

        # Add a scale
        scale = ContainerVolumeWeightObject("scale", 10, 10, 0, False)
        world.addObject(scale)

        # Add a sink
        sink = ContainerVolumeWeightObject("sink", 10, 10, 0, False, 1)
        world.addObject(sink)

        # Add water
        water = VolumeWeightObject("water", 10, 10)
        world.addObject(water)

        # Return the world
        return world

    # Get the task description for this game
    def getTaskDescription(self):
        return "Your task is to measure the density of the stone."

    # Make a dictionary whose keys are object names (strings), and whose values are lists of object references with those names.
    # This is useful for generating valid actions, and parsing user input.
    def makeNameToObjectDict(self):
        # Get a list of all game objects that could serve as arguments to actions
        allObjects = self.rootObject.getAllContainedObjectsRecursive()

        # Make a dictionary whose keys are object names (strings), and whose values are lists that contain the arguments.
        nameToObjectDict = {}
        for obj in allObjects:
            for name in obj.getReferents():
                #print("Object referent: " + name)
                if name in nameToObjectDict:
                    nameToObjectDict[name].append(obj)
                else:
                    nameToObjectDict[name] = [obj]

        return nameToObjectDict

    #
    #   Action generation
    #

    def addAction(self, actionStr, actionArgs):
        # Check whether the action string key already exists -- if not, add a blank list
        if not (actionStr in self.possibleActions):
            self.possibleActions[actionStr] = []
        # Add the action arguments to the list
        self.possibleActions[actionStr].append(actionArgs)

    # Returns a list of valid actions at the current time step
    def generatePossibleActions(self):
        # Get a list of all game objects that could serve as arguments to actions
        allObjects = self.makeNameToObjectDict()

        # Make a dictionary whose keys are possible action strings, and whose values are lists that contain the arguments.
        self.possibleActions = {}

        # Actions with zero arguments
        # (0-arg) Look around the environment
        self.addAction("look around", ["look around"])
        self.addAction("look", ["look around"])

        # (0-arg) Look at the agent's current inventory
        self.addAction("inventory", ["inventory"])

        # Actions with one object argument

        # (1-arg) Take
        for objReferent, objs in allObjects.items():
            for obj in objs:
                self.addAction("take " + objReferent, ["take", obj])
                self.addAction("take " + objReferent + " from " + obj.parent.getReferents()[0], ["take", obj])

        # (1-arg) Examine
        for objReferent, objs in allObjects.items():
            for obj in objs:
                self.addAction("examine " + objReferent, ["examine", obj])
                self.addAction("examine " + objReferent + " in " + obj.parent.getReferents()[0], ["examine", obj])

        # Actions with two object arguments

        # (2-arg) Put
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2):
                            containerPrefix = "in"
                            if obj2.properties["isContainer"]:
                                containerPrefix = obj2.properties["containerPrefix"]
                            self.addAction("put " + objReferent1 + " " + containerPrefix + " " + objReferent2, ["put", obj1, obj2])

        # (2-arg) Turn on/off
        for objReferent, objs in allObjects.items():
            for obj in objs:
                if obj.getProperty("isOn"):
                    self.addAction("turn off " + objReferent, ["turn off", obj])
                else:
                    self.addAction("turn on " + objReferent, ["turn on", obj])

        # Actions with three object arguments

        # (3-arg) Answer
        for objReferent, objs in allObjects.items():
            for obj in objs:
                if obj.getProperty("isAnswerable"):
                    self.addAction("answer " + objReferent, ["answer", obj])

        # Actions with four object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for objReferent3, objs3 in allObjects.items():
                    for obj1 in objs1:
                        for obj2 in objs2:
                            for obj3 in objs3:
                                if (obj1 != obj2 and obj1.getProperty("is_electrical_object") and obj2.getProperty("is_electrical_object")):
                                    for terminal_1 in obj1.connects:
                                        for terminal_2 in obj2.connects:
                                            self.addAction(f"connect {objReferent1} {terminal_1} to {objReferent2} {terminal_2}", ["connect", obj1, terminal_1, obj2, terminal_2])

        return self.possibleActions

    #
    #   Interpret actions
    #

    # Take an object from a container
    def actionTake(self, obj):
        # If the object doesn't have a parent container, then it's dangling and something has gone wrong
        if (obj.parent == None):
            return "Something has gone wrong -- that object is dangling in the void.  You can't take that."

        # Take the object from the parent container, and put it in the inventory
        obsStr, objRef, success = obj.parent.takeObjectFromContainer(obj)
        if (success == False):
            return obsStr

        # if an electrical object is taken, remove all its connections
        if obj.getProperty("is_electrical_object"):
            for key in obj.connects:
                obj.disconnect(key)

        # Add the object to the inventory
        self.agent.addObject(obj)
        return obsStr + " You put the " + obj.getReferents()[0] + " in your inventory."

    # Examine an object
    def actionExamine(self, obj):
        # If the object doesn't have a parent container, then it's dangling and something has gone wrong
        if (obj.parent == None):
            return "Something has gone wrong -- that object is dangling in the void.  You can't examine that."

        # Examine the object
        obsStr = "You examine the " + obj.getReferents()[0] + "."
        if (obj.getProperty("isContainer") == True):
            obsStr += " It is a container."
        if (obj.getProperty("isOpenable") == True):
            obsStr += " It is openable."
        if (obj.getProperty("isOpen") == True):
            obsStr += " It is open."
        if (obj.getProperty("isAnswerable") == True):
            obsStr += " It is answerable."
        if (obj.getProperty("isOn") == True):
            obsStr += " It is on."
        if (obj.getProperty("is_electrical_object") == True):
            obsStr += " It is an electrical object."
        if (obj.getProperty("is_wire") == True):
            obsStr += " It is a wire."
        if (obj.getProperty("is_battery") == True):
            obsStr += " It is a battery."
        if (obj.getProperty("is_light_bulb") == True):
            obsStr += " It is a light bulb."
        if (obj.getProperty("is_stone") == True):
            obsStr += " It is a stone."
        if (obj.getProperty("is_measuring_cup") == True):
            obsStr += " It is a measuring cup."
        if (obj.getProperty("is_scale") == True):
            obsStr += " It is a scale."
        if (obj.getProperty("is_sink") == True):
            obsStr += " It is a sink."
        if (obj.getProperty("is_water") == True):
            obsStr += " It is water."
        return obsStr

    # Put an object in a container
    def actionPut(self, objToMove, newContainer):
        # Check that the destination container is a container
        if (newContainer.getProperty("isContainer") == False):
            return "You can't put things in the " + newContainer.getReferents()[0] + "."

        # Enforce that the object must be in the inventory to do anything with it
        if (objToMove.parent != self.agent):
            return "You don't currently have the " + objToMove.getReferents()[0] + " in your inventory."

        # Take the object from it's current container, and put it in the new container.
        # Deep copy the reference to the original parent container, because the object's parent container will be changed when it's taken from the original container
        originalContainer = objToMove.parent
        obsStr1, objRef, success = objToMove.parent.takeObjectFromContainer(objToMove)
        if (success == False):
            return obsStr1

        # Put the object in the new container
        obsStr2, success = newContainer.placeObjectInContainer(objToMove)
        if (success == False):
            # For whatever reason, the object can't be moved into the new container. Put the object back into the original container
            originalContainer.addObject(objToMove)
            return obsStr2

        # Success -- show both take and put observations
        return obsStr1 + "\n" + obsStr2

    # Turn on/off an object
    def actionTurnOnOff(self, obj):
        # Check that the object is a container
        if (obj.getProperty("isContainer") == False):
            return "You can't turn the " + obj.getReferents()[0] + " on or off."

        # Enforce that the object must be in the inventory to do anything with it
        if (obj.parent != self.agent):
            return "You don't currently have the " + obj.getReferents()[0] + " in your inventory."

        # Turn the object on or off
        if (obj.getProperty("isOn") == True):
            obj.properties["isOn"] = False
            return "You turn the " + obj.getReferents()[0] + " off."
        else:
            obj.properties["isOn"] = True
            return "You turn the " + obj.getReferents()[0] + " on."

    # Answer an object
    def actionAnswer(self, obj):
        # Check that the object is answerable
        if (obj.getProperty("isAnswerable") == False):
            return "You can't answer the " + obj.getReferents()[0] + "."

        # Enforce that the object must be in the inventory to do anything with it
        if (obj.parent != self.agent):
            return "You don't currently have the " + obj.getReferents()[0] + " in your inventory."

        # Answer the object
        obsStr = "You answer the " + obj.getReferents()[0] + "."
        self.gameOver = True
        self.gameWon = True
        return obsStr

    # Connects two electrical objects
    def actionConnect(self, obj1, terminal_1, obj2, terminal_2):
        # at least one of the two objects should be a wire
        if not (obj1.getProperty("is_wire") or (obj2.getProperty("is_wire"))):
            return "You cannot connect to devices directly without a wire."
        # disconnect the terminal if the terminal is already connected to other objects
        if obj1.connects[terminal_1]:
            obj1.disconnect(terminal_1)
        if obj2.connects[terminal_2]:
            obj2.disconnect(terminal_2)
        obj1.connects[terminal_1] = (obj2, terminal_2)
        obj2.connects[terminal_2] = (obj1, terminal_1)
        return f"Successfully connect {obj1.name} {terminal_1} to {obj2.name} {terminal_2}"

    # Performs an action in the environment, returns the result (a string observation, the reward, and whether the game is completed).
    def step(self, actionStr):
        self.observationStr = ""
        reward = 0

        # Check to make sure the action is in the possible actions dictionary
        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return (self.observationStr, self.score, reward, self.gameOver, self.gameWon)

        self.numSteps += 1

        # Find the action in the possible actions dictionary
        actions = self.possibleActions[actionStr]
        action = None

        # Check for an ambiguous action (i.e. one that has multiple possible arguments)
        if (len(actions) > 1):
            # If there are multiple possible arguments, for now just choose the first one
            action = actions[0]
        else:
            # Otherwise, also just take the first action in the list of possible actions
            action = actions[0]

        # Interpret the action
        actionVerb = action[0]


        if (actionVerb == "look around"):
            # Look around the environment -- i.e. show the description of the world.
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif (actionVerb == "inventory"):
            # Display the agent's inventory
            self.observationStr = self.actionInventory()

        elif (actionVerb == "take"):
            # Take an object from a container
            thingToTake = action[1]
            self.observationStr = self.actionTake(thingToTake)
        elif (actionVerb == "examine"):
            # Examine an object
            thingToExamine = action[1]
            self.observationStr = self.actionExamine(thingToExamine)
        elif (actionVerb == "put"):
            # Put an object in a container
            thingToMove = action[1]
            newContainer = action[2]
            self.observationStr = self.actionPut(thingToMove, newContainer)
        elif (actionVerb == "turn on"):
            # Turn on an object
            thingToTurnOn = action[1]
            self.observationStr = self.actionTurnOnOff(thingToTurnOn)
        elif (actionVerb == "turn off"):
            # Turn off an object
            thingToTurnOff = action[1]
            self.observationStr = self.actionTurnOnOff(thingToTurnOff)
        elif (actionVerb == "answer"):
            # Answer an object
            thingToAnswer = action[1]
            self.observationStr = self.actionAnswer(thingToAnswer)
        elif (actionVerb == "connect"):
            obj1, terminal_1, obj2, terminal_2 = action[1:]
            self.observationStr = self.actionConnect(obj1, terminal_1, obj2, terminal_2)
        # Catch-all
        else:
            self.observationStr = "ERROR: Unknown action."

        # Do one tick of the environment
        self.doWorldTick()

        # Calculate the score
        lastScore = self.score
        self.calculateScore()
        reward = self.score - lastScore

        return (self.observationStr, self.score, reward, self.gameOver, self.gameWon)

    # Call the object update for each object in the environment
    def doWorldTick(self):
        # Get a list of all objects in the environment
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        # Loop through all objects, and call their tick()
        for obj in allObjects:
            obj.tick()

    # Calculate the game score
    def calculateScore(self):
        # Baseline score
        self.score = 0

        # Check if the stone is put into the correct box.
        allObjects = self.rootObject.getAllContainedObjectsRecursive()

        for obj in allObjects:
            if type(obj) == Stone:
                if obj.getProperty("isOn"):
                    self.score += 1
                    self.gameOver = True
                    self.gameWon = True


# Main Program
def main():
    # Random seed
    randomSeed = 1

    # Create a new game
    game = TextGame(randomSeed = randomSeed)

    # Get a list of valid actions
    possibleActions = game.generatePossibleActions()
    #print("Possible actions: " + str(possibleActions.keys()))
    print("Task Description: " + game.getTaskDescription())
    print("")
    print("Initial Observation: " + game.observationStr)
    print("")
    print("Type 'help' for a list of possible actions.")
    print("")


    # Main game loop
    #while not game.gameOver:
    while True:

        # Get the player's action
        actionStr = ""
        while ((len(actionStr) == 0) or (actionStr == "help")):
            actionStr = input("> ")
            if (actionStr == "help"):
                print("Possible actions: " + str(possibleActions.keys()))
                print("")
                actionStr = ""
            elif (actionStr == "exit") or (actionStr == "quit"):
                return

        # Perform the action
        observationStr, score, reward, gameOver, gameWon = game.step(actionStr)

        # Get a list of valid actions
        possibleActions = game.generatePossibleActions()

        # Print the current game state
        print("Observation: " + observationStr)
        print("")
        print("Current step: " + str(game.numSteps))
        print("Score: " + str(score))
        print("Reward: " + str(reward))
        print("Game Over: " + str(gameOver))
        print("Game Won: " + str(gameWon))
        print("")
        print("----------------------------------------")


# Run the main program
if __name__ == "__main__":
    main()
