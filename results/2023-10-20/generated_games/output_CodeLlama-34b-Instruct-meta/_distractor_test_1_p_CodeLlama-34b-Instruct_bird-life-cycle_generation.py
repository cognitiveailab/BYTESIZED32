# heating_milk.py
# based on make-ice-cubes.py
# ruoyao wang (feb 7/2023)

# Task: Create a micro-simulation that models how to heat milk to a temperature that is suitable for a baby using a stove.
# Environment: kitchen
# Task-critical Objects: Stove, Pot, Milk, Fridge, Thermometer
# High-level object classes: Device (Stove, Fridge), Container (Stove, Pot, Fridge) 
# Critical properties: temperature (Milk), temperature_increase_per_tick (Stove), temperature_decrease_per_tick (fridge), max_temperature (Stove), min_temperature (fridge)
# Actions: look, inventory, examine, take/put object, open/close container, turn on/off device, use thermometer on object, feed baby with milk
# Distractor Items: None
# Distractor Actions: drink milk
# High-level solution procedure: open fridge, take pot containing milk, put the pot on the stove, turn on the stove, use the thermometer to moniter the milk temperature till the temperature is suitable for a baby to drink, feed baby

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
        self.parentContainer = None
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
        obj.parentContainer = self

    # Remove an object from this container
    def removeObject(self, obj):
        self.contains.remove(obj)
        obj.parentContainer = None

    # Remove the current object from whatever container it's currently in
    def removeSelfFromContainer(self):
        if self.parentContainer != None:
            self.parentContainer.removeObject(self)

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
        return "the " + self.name + "."


# A device with a temperature that can be increased or decreased
class Device(GameObject):
    def __init__(self, name, temperature, temperature_increase_per_tick, temperature_decrease_per_tick, max_temperature, min_temperature):
        GameObject.__init__(self, name)
        self.properties["temperature"] = temperature
        self.properties["temperature_increase_per_tick"] = temperature_increase_per_tick
        self.properties["temperature_decrease_per_tick"] = temperature_decrease_per_tick
        self.properties["max_temperature"] = max_temperature
        self.properties["min_temperature"] = min_temperature

    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

    def getReferents(self):
        return [self.getProperty("temperature")]

    def tick(self):
        output_str = None
        # increase the temperature of the device
        self.properties["temperature"] += self.properties["temperature_increase_per_tick"]
        # decrease the temperature of the device
        self.properties["temperature"] -= self.properties["temperature_decrease_per_tick"]
        # if the temperature is higher than the max temperature, set it to the max temperature
        if self.properties["temperature"] > self.properties["max_temperature"]:
            self.properties["temperature"] = self.properties["max_temperature"]
        # if the temperature is lower than the min temperature, set it to the min temperature
        if self.properties["temperature"] < self.properties["min_temperature"]:
            self.properties["temperature"] = self.properties["min_temperature"]
        return output_str


# A container with a temperature that can be increased or decreased
class ContainerWithTemperature(Container, Device):
    def __init__(self, name, temperature, temperature_increase_per_tick, temperature_decrease_per_tick, max_temperature, min_temperature):
        Container.__init__(self, name)
        Device.__init__(self, name, temperature, temperature_increase_per_tick, temperature_decrease_per_tick, max_temperature, min_temperature)

    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

    def getReferents(self):
        return [self.getProperty("temperature")]

    def tick(self):
        output_str = None
        # increase the temperature of the container
        self.properties["temperature"] += self.properties["temperature_increase_per_tick"]
        # decrease the temperature of the container
        self.properties["temperature"] -= self.properties["temperature_decrease_per_tick"]
        # if the temperature is higher than the max temperature, set it to the max temperature
        if self.properties["temperature"] > self.properties["max_temperature"]:
            self.properties["temperature"] = self.properties["max_temperature"]
        # if the temperature is lower than the min temperature, set it to the min temperature
        if self.properties["temperature"] < self.properties["min_temperature"]:
            self.properties["temperature"] = self.properties["min_temperature"]
        return output_str


# A thermometer that can be used to measure the temperature of an object
class Thermometer(GameObject):
    def __init__(self, name):
        GameObject.__init__(self, name)

    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

    def getReferents(self):
        return [self.getProperty("temperature")]

    def tick(self):
        output_str = None
        # if the thermometer is being used to measure the temperature of an object, set the temperature of the thermometer to the temperature of the object
        if self.properties["isBeingUsed"] == True:
            self.properties["temperature"] = self.properties["objectBeingMeasured"].getProperty("temperature")
        return output_str


# A pot with a temperature that can be increased or decreased
class Pot(ContainerWithTemperature):
    def __init__(self, name, temperature, temperature_increase_per_tick, temperature_decrease_per_tick, max_temperature, min_temperature):
        ContainerWithTemperature.__init__(self, name, temperature, temperature_increase_per_tick, temperature_decrease_per_tick, max_temperature, min_temperature)

    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

    def getReferents(self):
        return [self.getProperty("temperature")]

    def tick(self):
        output_str = None
        # increase the temperature of the pot
        self.properties["temperature"] += self.properties["temperature_increase_per_tick"]
        # decrease the temperature of the pot
        self.properties["temperature"] -= self.properties["temperature_decrease_per_tick"]
        # if the temperature is higher than the max temperature, set it to the max temperature
        if self.properties["temperature"] > self.properties["max_temperature"]:
            self.properties["temperature"] = self.properties["max_temperature"]
        # if the temperature is lower than the min temperature, set it to the min temperature
        if self.properties["temperature"] < self.properties["min_temperature"]:
            self.properties["temperature"] = self.properties["min_temperature"]
        return output_str


# A stove with a temperature that can be increased or decreased
class Stove(Device):
    def __init__(self, name, temperature, temperature_increase_per_tick, temperature_decrease_per_tick, max_temperature, min_temperature):
        Device.__init__(self, name, temperature, temperature_increase_per_tick, temperature_decrease_per_tick, max_temperature, min_temperature)

    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

    def getReferents(self):
        return [self.getProperty("temperature")]

    def tick(self):
        output_str = None
        # increase the temperature of the stove
        self.properties["temperature"] += self.properties["temperature_increase_per_tick"]
        # decrease the temperature of the stove
        self.properties["temperature"] -= self.properties["temperature_decrease_per_tick"]
        # if the temperature is higher than the max temperature, set it to the max temperature
        if self.properties["temperature"] > self.properties["max_temperature"]:
            self.properties["temperature"] = self.properties["max_temperature"]
        # if the temperature is lower than the min temperature, set it to the min temperature
        if self.properties["temperature"] < self.properties["min_temperature"]:
            self.properties["temperature"] = self.properties["min_temperature"]
        return output_str


# A fridge with a temperature that can be increased or decreased
class Fridge(ContainerWithTemperature):
    def __init__(self, name, temperature, temperature_increase_per_tick, temperature_decrease_per_tick, max_temperature, min_temperature):
        ContainerWithTemperature.__init__(self, name, temperature, temperature_increase_per_tick, temperature_decrease_per_tick, max_temperature, min_temperature)

    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

    def getReferents(self):
        return [self.getProperty("temperature")]

    def tick(self):
        output_str = None
        # increase the temperature of the fridge
        self.properties["temperature"] += self.properties["temperature_increase_per_tick"]
        # decrease the temperature of the fridge
        self.properties["temperature"] -= self.properties["temperature_decrease_per_tick"]
        # if the temperature is higher than the max temperature, set it to the max temperature
        if self.properties["temperature"] > self.properties["max_temperature"]:
            self.properties["temperature"] = self.properties["max_temperature"]
        # if the temperature is lower than the min temperature, set it to the min temperature
        if self.properties["temperature"] < self.properties["min_temperature"]:
            self.properties["temperature"] = self.properties["min_temperature"]
        return output_str


# A milk with a temperature that can be increased or decreased
class Milk(GameObject):
    def __init__(self, name, temperature, temperature_increase_per_tick, temperature_decrease_per_tick, max_temperature, min_temperature):
        GameObject.__init__(self, name)
        self.properties["temperature"] = temperature
        self.properties["temperature_increase_per_tick"] = temperature_increase_per_tick
        self.properties["temperature_decrease_per_tick"] = temperature_decrease_per_tick
        self.properties["max_temperature"] = max_temperature
        self.properties["min_temperature"] = min_temperature

    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

    def getReferents(self):
        return [self.getProperty("temperature")]

    def tick(self):
        output_str = None
        # increase the temperature of the milk
        self.properties["temperature"] += self.properties["temperature_increase_per_tick"]
        # decrease the temperature of the milk
        self.properties["temperature"] -= self.properties["temperature_decrease_per_tick"]
        # if the temperature is higher than the max temperature, set it to the max temperature
        if self.properties["temperature"] > self.properties["max_temperature"]:
            self.properties["temperature"] = self.properties["max_temperature"]
        # if the temperature is lower than the min temperature, set it to the min temperature
        if self.properties["temperature"] < self.properties["min_temperature"]:
            self.properties["temperature"] = self.properties["min_temperature"]
        return output_str


# The world is the root object of the game object tree.  In single room environments, it's where all the objects are located.
class World(Container):
    def __init__(self):
        Container.__init__(self, "kitchen")

    def makeDescriptionStr(self, makeDetailed=False):
        outStr = "You are in the kitchen.  In the kitchen, you see: \n"
        for obj in self.contains:
            outStr += "\t" + obj.makeDescriptionStr() + "\n"

        return outStr


# The agent (just a placeholder for a container for the inventory)
class Agent(GameObject):
    def __init__(self):
        GameObject.__init__(self, "agent")

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

        # Add the agent (the player) into the world (kitchen)
        world.addObject(self.agent)
        # Add a stove into the kitchen
        stove = Stove("stove", 0, 1, 0, 100, 0)
        world.addObject(stove)
        # Add a fridge into the kitchen
        fridge = Fridge("fridge", 0, 0, 1, 0, -20)
        world.addObject(fridge)
        # Add a pot into the kitchen
        pot = Pot("pot", 0, 1, 0, 100, 0)
        world.addObject(pot)
        # Add a thermometer into the kitchen
        thermometer = Thermometer("thermometer")
        world.addObject(thermometer)
        # Add a milk into the fridge
        milk = Milk("milk", 0, 0, 0, 100, 0)
        fridge.addObject(milk)

        # Return the world
        return world

    # Get the task description for this game
    def getTaskDescription(self):
        return f"Your task is to heat the milk to a temperature that is suitable for a baby to drink."

    # Make a dictionary whose keys are object names (strings), and whose values are lists of object references with those names.
    # This is useful for generating valid actions, and parsing user input.
    def makeNameToObjectDict(self):
        # Get a list of all game objects that could serve as arguments to actions
        allObjects = self.rootObject.getAllContainedObjectsRecursive()

        # Make a dictionary whose keys are object names (strings), and whose values are lists of object references with those names.
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
        allObjects = self.rootObject.getAllContainedObjectsRecursive()

        # Make a dictionary whose keys are object names (strings), and whose values are lists of object references with those names.
        nameToObjectDict = self.makeNameToObjectDict()

        # Make a dictionary whose keys are possible action strings, and whose values are lists that contain the arguments.
        self.possibleActions = {}

        # Actions with zero arguments
        # (0-arg) Look around the environment
        self.addAction("look around", ["look around"])
        self.addAction("look", ["look around"])

        # (0-arg) Look at the agent's current inventory
        self.addAction("inventory", ["inventory"])

        # (0-arg) Examine the stove
        self.addAction("examine stove", ["examine", "stove"])
        self.addAction("examine the stove", ["examine", "stove"])
        self.addAction("examine the stove", ["examine", "stove"])

        # (0-arg) Examine the fridge
        self.addAction("examine fridge", ["examine", "fridge"])
        self.addAction("examine the fridge", ["examine", "fridge"])
        self.addAction("examine the fridge", ["examine", "fridge"])

        # (0-arg) Examine the pot
        self.addAction("examine pot", ["examine", "pot"])
        self.addAction("examine the pot", ["examine", "pot"])
        self.addAction("examine the pot", ["examine", "pot"])

        # (0-arg) Examine the thermometer
        self.addAction("examine thermometer", ["examine", "thermometer"])
        self.addAction("examine the thermometer", ["examine", "thermometer"])
        self.addAction("examine the thermometer", ["examine", "thermometer"])

        # (0-arg) Turn on the stove
        self.addAction("turn on stove", ["turn on", "stove"])
        self.addAction("turn on the stove", ["turn on", "stove"])
        self.addAction("turn on the stove", ["turn on", "stove"])

        # (0-arg) Turn off the stove
        self.addAction("turn off stove", ["turn off", "stove"])
        self.addAction("turn off the stove", ["turn off", "stove"])
        self.addAction("turn off the stove", ["turn off", "stove"])

        # (0-arg) Open the fridge
        self.addAction("open fridge", ["open", "fridge"])
        self.addAction("open the fridge", ["open", "fridge"])
        self.addAction("open the fridge", ["open", "fridge"])

        # (0-arg) Close the fridge
        self.addAction("close fridge", ["close", "fridge"])
        self.addAction("close the fridge", ["close", "fridge"])
        self.addAction("close the fridge", ["close", "fridge"])

        # (0-arg) Use the thermometer on the stove
        self.addAction("use thermometer on stove", ["use", "thermometer", "stove"])
        self.addAction("use the thermometer on the stove", ["use", "thermometer", "stove"])
        self.addAction("use the thermometer on the stove", ["use", "thermometer", "stove"])

        # (0-arg) Use the thermometer on the fridge
        self.addAction("use thermometer on fridge", ["use", "thermometer", "fridge"])
        self.addAction("use the thermometer on the fridge", ["use", "thermometer", "fridge"])
        self.addAction("use the thermometer on the fridge", ["use", "thermometer", "fridge"])

        # (0-arg) Use the thermometer on the pot
        self.addAction("use thermometer on pot", ["use", "thermometer", "pot"])
        self.addAction("use the thermometer on the pot", ["use", "thermometer", "pot"])
        self.addAction("use the thermometer on the pot", ["use", "thermometer", "pot"])

        # (0-arg) Use the thermometer on the milk
        self.addAction("use thermometer on milk", ["use", "thermometer", "milk"])
        self.addAction("use the thermometer on the milk", ["use", "thermometer", "milk"])
        self.addAction("use the thermometer on the milk", ["use", "thermometer", "milk"])

        # Actions with one object argument
        # (1-arg) Take an object
        for objReferent, objs in nameToObjectDict.items():
            for obj in objs:
                self.addAction("take " + objReferent, ["take", obj])

        # (1-arg) Put an object in a container
        for objReferent, objs in nameToObjectDict.items():
            for obj in objs:
                self.addAction("put " + objReferent + " in", ["put", obj, "in"])

        # (1-arg) Open a container
        for objReferent, objs in nameToObjectDict.items():
            for obj in objs:
                self.addAction("open " + objReferent, ["open", obj])

        # (1-arg) Close a container
        for objReferent, objs in nameToObjectDict.items():
            for obj in objs:
                self.addAction("close " + objReferent, ["close", obj])

        # (1-arg) Turn on a device
        for objReferent, objs in nameToObjectDict.items():
            for obj in objs:
                self.addAction("turn on " + objReferent, ["turn on", obj])

        # (1-arg) Turn off a device
        for objReferent, objs in nameToObjectDict.items():
            for obj in objs:
                self.addAction("turn off " + objReferent, ["turn off", obj])

        # (1-arg) Use a thermometer on an object
        for objReferent, objs in nameToObjectDict.items():
            for obj in objs:
                self.addAction("use thermometer on " + objReferent, ["use", "thermometer", obj])

        # (1-arg) Feed a baby with milk
        for objReferent, objs in nameToObjectDict.items():
            for obj in objs:
                self.addAction("feed baby with " + objReferent, ["feed", "baby", obj])

        return self.possibleActions

    #
    #   Interpret actions
    #

    # # Perform the "eat" action.  Returns an observation string.
    # def actionEat(self, obj):
    #     # Enforce that the object must be in the inventory to do anything with it
    #     if (obj.parentContainer != self.agent):
    #         return "You don't currently have the " + obj.getReferents()[0] + " in your inventory."

    #     # Check if the object is food
    #     if (obj.getProperty("isFood") == True):
    #         # Try to pick up/take the food
    #         obsStr, objRef, success = obj.parentContainer.takeObjectFromContainer(obj)
    #         if (success == False):
    #             # If it failed, we were unable to take the food (e.g. it was in a closed container)
    #             return "You can't see that."

    #         # Update the game observation
    #         return "You eat the " + obj.foodName + "."
    #     else:
    #         return "You can't eat that."


    # Display agent inventory
    def actionInventory(self):
        # Get the inventory
        inventory = self.agent.contains
        # If the inventory is empty, return a message
        if (len(inventory) == 0):
            return "Your inventory is empty."
        # Otherwise, return a list of the inventory items
        else:
            obsStr = "You have the following items in your inventory:\n"
            for obj in inventory:
                obsStr += "\t" + obj.makeDescriptionStr() + "\n"
            return obsStr

    # Examine an object
    def actionExamine(self, obj):
        # Enforce that the object must be in the environment to do anything with it
        if (obj.parentContainer != self.rootObject):
            return "You don't currently see the " + obj.getReferents()[0] + " in the environment."

        # Update the game observation
        return "You examine the " + obj.name + "."

    # Turn on a device
    def actionTurnOn(self, obj):
        # Enforce that the object must be in the environment to do anything with it
        if (obj.parentContainer != self.rootObject):
            return "You don't currently see the " + obj.getReferents()[0] + " in the environment."

        # Check if the object is a device
        if (obj.getProperty("isDevice") == True):
            # Try to turn on the device
            obsStr, success = obj.turnOn()
            if (success == False):
                # If it failed, we were unable to turn on the device (e.g. it was already on)
                return "You can't turn on the " + obj.name + "."

            # Update the game observation
            return "You turn on the " + obj.name + "."
        else:
            return "You can't turn on that."

    # Turn off a device
    def actionTurnOff(self, obj):
        # Enforce that the object must be in the environment to do anything with it
        if (obj.parentContainer != self.rootObject):
            return "You don't currently see the " + obj.getReferents()[0] + " in the environment."

        # Check if the object is a device
        if (obj.getProperty("isDevice") == True):
            # Try to turn off the device
            obsStr, success = obj.turnOff()
            if (success == False):
                # If it failed, we were unable to turn off the device (e.g. it was already off)
                return "You can't turn off the " + obj.name + "."

            # Update the game observation
            return "You turn off the " + obj.name + "."
        else:
            return "You can't turn off that."

    # Open a container
    def actionOpen(self, obj):
        # Enforce that the object must be in the environment to do anything with it
        if (obj.parentContainer != self.rootObject):
            return "You don't currently see the " + obj.getReferents()[0] + " in the environment."

        # Check if the object is a container
        if (obj.getProperty("isContainer") == True):
            # Try to open the container
            obsStr, success = obj.openContainer()
            if (success == False):
                # If it failed, we were unable to open the container (e.g. it was already open)
                return "You can't open the " + obj.name + "."

            # Update the game observation
            return "You open the " + obj.name + "."
        else:
            return "You can't open that."

    # Close a container
    def actionClose(self, obj):
        # Enforce that the object must be in the environment to do anything with it
        if (obj.parentContainer != self.rootObject):
            return "You don't currently see the " + obj.getReferents()[0] + " in the environment."

        # Check if the object is a container
        if (obj.getProperty("isContainer") == True):
            # Try to close the container
            obsStr, success = obj.closeContainer()
            if (success == False):
                # If it failed, we were unable to close the container (e.g. it was already closed)
                return "You can't close the " + obj.name + "."

            # Update the game observation
            return "You close the " + obj.name + "."
        else:
            return "You can't close that."

    # Take an object
    def actionTake(self, obj):
        # Enforce that the object must be in the environment to do anything with it
        if (obj.parentContainer != self.rootObject):
            return "You don't currently see the " + obj.getReferents()[0] + " in the environment."

        # Check if the object is moveable
        if (obj.getProperty("isMoveable") == True):
            # Try to pick up/take the object
            obsStr, objRef, success = obj.parentContainer.takeObjectFromContainer(obj)
            if (success == False):
                # If it failed, we were unable to take the object (e.g. it was in a closed container)
                return "You can't see that."

            # Add the object to the agent's inventory
            self.agent.addObject(obj)

            # Update the game observation
            return "You take the " + obj.getReferents()[0] + "."
        else:
            return "You can't take that."

    # Put an object in a container
    def actionPut(self, obj, container):
        # Enforce that the object must be in the environment to do anything with it
        if (obj.parentContainer != self.rootObject):
            return "You don't currently see the " + obj.getReferents()[0] + " in the environment."

        # Check if the object is moveable
        if (obj.getProperty("isMoveable") == True):
            # Try to pick up/take the object
            obsStr, objRef, success = obj.parentContainer.takeObjectFromContainer(obj)
            if (success == False):
                # If it failed, we were unable to take the object (e.g. it was in a closed container)
                return "You can't see that."

            # Try to put the object in the container
            obsStr, success = container.placeObjectInContainer(obj)
            if (success == False):
                # If it failed, we were unable to put the object in the container (e.g. it was closed)
                return "You can't put the " + obj.getReferents()[0] + " in the " + container.getReferents()[0] + "."

            # Update the game observation
            return "You put the " + obj.getReferents()[0] + " in the " + container.getReferents()[0] + "."
        else:
            return "You can't put that."

    # Use a thermometer on an object
    def actionUseThermometer(self, thermometer, obj):
        # Enforce that the object must be in the environment to do anything with it
        if (obj.parentContainer != self.rootObject):
            return "You don't currently see the " + obj.getReferents()[0] + " in the environment."

        # Check if the object is a device
        if (obj.getProperty("isDevice") == True):
            # Try to use the thermometer on the device
            obsStr, success = thermometer.useOn(obj)
            if (success == False):
                # If it failed, we were unable to use the thermometer on the device (e.g. it was already on)
                return "You can't use the thermometer on the " + obj.name + "."

            # Update the game observation
            return "You use the thermometer on the " + obj.name + "."
        else:
            return "You can't use the thermometer on that."

    # Feed a baby with milk
    def actionFeedBaby(self, milk):
        # Enforce that the object must be in the environment to do anything with it
        if (milk.parentContainer != self.rootObject):
            return "You don't currently see the " + milk.getReferents()[0] + " in the environment."

        # Check if the object is a milk
        if (milk.getProperty("isMilk") == True):
            # Try to feed the baby with the milk
            obsStr, success = milk.feedBaby()
            if (success == False):
                # If it failed, we were unable to feed the baby with the milk (e.g. it was not in the fridge)
                return "You can't feed the baby with the " + milk.name + "."

            # Update the game observation
            return "You feed the baby with the " + milk.name + "."
        else:
            return "You can't feed the baby with that."


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
        elif (actionVerb == "examine"):
            # Examine an object
            obj = action[1]
            self.observationStr = self.actionExamine(obj)
        elif (actionVerb == "take"):
            # Take an object
            obj = action[1]
            self.observationStr = self.actionTake(obj)
        elif (actionVerb == "put"):
            # Put an object in a container
            obj = action[1]
            container = action[2]
            self.observationStr = self.actionPut(obj, container)
        elif (actionVerb == "open"):
            # Open a container
            obj = action[1]
            self.observationStr = self.actionOpen(obj)
        elif (actionVerb == "close"):
            # Close a container
            obj = action[1]
            self.observationStr = self.actionClose(obj)
        elif (actionVerb == "turn on"):
            # Turn on a device
            obj = action[1]
            self.observationStr = self.actionTurnOn(obj)
        elif (actionVerb == "turn off"):
            # Turn off a device
            obj = action[1]
            self.observationStr = self.actionTurnOff(obj)
        elif (actionVerb == "use"):
            # Use a thermometer on an object
            thermometer = action[1]
            obj = action[2]
            self.observationStr = self.actionUseThermometer(thermometer, obj)
        elif (actionVerb == "feed"):
            # Feed a baby with milk
            milk = action[2]
            self.observationStr = self.actionFeedBaby(milk)


        # Catch-all
        else:
            self.observationStr = "ERROR: Unknown action."

        # Do one tick of the environment
        tick_output_strs = self.doWorldTick()
        # if any tick output some information, add it to the output string
        if len(tick_output_strs) > 0:
            self.observationStr = '\n'.join([self.observationStr] + tick_output_strs)
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
        output_strs = []
        for obj in allObjects:
            tick_output_str = obj.tick()
            if tick_output_str is not None:
                output_strs.append(tick_output_str)
        return output_strs

    # Calculate the game score
    def calculateScore(self):
        # Baseline score
        self.score = 0

        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        for obj in allObjects:
            # If there is a baby in the environment, the player wins.
            if (obj.name == "baby"):
                self.score += 1
                self.gameOver = True
                self.gameWon = True
            # The player loses the game if the milk is not heated to a suitable temperature.
            if (obj.getProperty("temperature") < 37):
                self.score = 0
                self.gameOver = True
                self.gameWon = False



# Main Program
def main():
    # Random seed
    randomSeed = 0

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
