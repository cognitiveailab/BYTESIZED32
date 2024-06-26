# heating_milk.py
# based on refridgerate_food.py
### peter jansen (feb 15/2023)

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

        # Initialize everything to have a starting temperature of 20 degrees C
        self.properties["temperature"] = 20.0

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

    # Set the temperature of anything in the container to be closer to the temperature of the container.
    # This functionally simulates heat transfer between the container and the objects inside it.
    def tick(self):
        # Get a list of all objects in the fridge
        objectsInContainer = self.getAllContainedObjectsRecursive()

        maxTempChangePerTick = 5.0      # Maximum temperature change per tick
        # Change the objects in the container's temperature to be closer to the containers temperature
        for obj in objectsInContainer:
            # Case 1: The object's temperature is higher than the container's temperature
            if (obj.properties["temperature"] > self.properties["temperature"]):
                # Decrease the object's temperature, down to the container's temperature
                newTemperature = obj.properties["temperature"] - maxTempChangePerTick
                if (newTemperature < self.properties["temperature"]):
                    newTemperature = self.properties["temperature"]
                obj.properties["temperature"] = newTemperature

            # Case 2: The object's temperature is lower than the container's temperature
            elif (obj.properties["temperature"] < self.properties["temperature"]):
                # Increase the object's temperature, up to the container's temperature
                newTemperature = obj.properties["temperature"] + maxTempChangePerTick
                if (newTemperature > self.properties["temperature"]):
                    newTemperature = self.properties["temperature"]
                obj.properties["temperature"] = newTemperature


    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."


#
#   Abstract Game-object Classes
#

# Abstract class for anything that can be considered a device that turns on or off (e.g. a light, a fan, a TV, etc.)
class Device(GameObject):
    def __init__(self, name):
        # Prevent this constructor from running if it's already been run during multiple inheritance
        if hasattr(self, "constructorsRun"):
            if "Device" in self.constructorsRun:
                return
        GameObject.__init__(self, name)
        # Otherwise, mark this constructor as having been run
        self.constructorsRun.append("Device")

        self.properties["isDevice"] = True
        self.properties["isActivatable"] = True # Can this device be turned on or off?
        self.properties["isOn"] = False         # Is the device currently on or off?

    # Try to turn on the device.
    # Returns an observation string, and a success flag (boolean)
    def turnOn(self):
        # If the device isn't activatable, then return an error
        if (self.getProperty("isActivatable") == False):
            return ("It's not clear how the " + self.getReferents()[0] + " could be turned on.", False)

        # If the device is already on, then return an error
        if self.properties["isOn"]:
            return ("The " + self.getReferents()[0] + " is already on.", False)
        else:
            self.properties["isOn"] = True
            return ("The " + self.getReferents()[0] + " is now turned on.", True)

    # Try to turn off the device.
    # Returns an observation string, and a success flag (boolean)
    def turnOff(self):
        # If the device isn't activatable, then return an error
        if (self.getProperty("isActivatable") == False):
            return ("It's not clear how the " + self.getReferents()[0] + " could be turned off.", False)

        # If the device is already off, then return an error
        if not self.properties["isOn"]:
            return ("The " + self.getReferents()[0] + " is already off.", False)
        else:
            self.properties["isOn"] = False
            return ("The " + self.getReferents()[0] + " is now turned off.", True)

    # Try to use the device with a patient object (e.g. a light with a person, a fan with a person, etc.)
    # Returns an observation string, and a success flag (boolean)
    def useWithObject(self, patientObject):
        return ("You're not sure how to use the " + self.getReferents()[0] + " with the " + patientObject.name + ".", False)

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        outStr = "The " + self.name + ", which is currently "
        if self.properties["isOn"]:
            outStr += "on."
        else:
            outStr += "off."
        return outStr


#
#   Specific Game Objects
#

# A stove, which is a heating device.  It contains things inside of it.  It's always on.  When things are inside it, it heats them up.
class Stove(Container, Device):
    def __init__(self):
        GameObject.__init__(self, "stove")
        Container.__init__(self, "stove")
        Device.__init__(self, "stove")

        self.properties["containerPrefix"] = "on"

        # Set the properties of this object
        self.properties["isOpenable"] = True    # A stove is openable
        self.properties["isOpen"] = False       # A stove starts out closed
        self.properties["isMoveable"] = False   # A stove is too heavy to move (and doesn't really need to be moved for this simulation)

        self.properties["isOn"] = True           # A stove is always on
        self.properties["isActivatable"] = False # A stove essentially never is turned off (unless it's unplugged, which is irelevant for this simulation)

        # Set the maximum temperature of the stove (in degrees Celsius)
        self.properties["maxTemperature"] = 100.0        # Maximum temperature of the stove
        self.properties["temperature_increase_per_tick"] = 5.0   # How much the temperature increases per tick

    # Increase the temperature of anything inside the stove
    def tick(self):
        # If the stove is on, then increase the temperature of anything inside it
        if (self.properties["isOn"] == True):
            # Let's also add fidelity and say the temperature will only increase if the stove is closed
            if (self.properties["isOpen"] == False):

                # Get a list of all objects in the stove
                objectsOnStove = self.getAllContainedObjectsRecursive()

                # Increase the temperature of each object in the stove
                for obj in objectsOnStove:
                    # Increase the object's temperature, up to the maximum temperature
                    newTemperature = obj.properties["temperature"] + self.properties["temperature_increase_per_tick"]
                    if (newTemperature > self.properties["maxTemperature"]):
                        newTemperature = self.properties["maxTemperature"]
                    obj.properties["temperature"] = newTemperature

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        outStr = "a stove"

        # A stove is essentially always on, so we'll only mention it if it's off
        if not self.properties["isOn"]:
            outStr += " that is currently off, and"

        # Check if open
        if self.properties["isOpen"]:
            outStr += " that is currently open"
            # Check if empty
            effectiveContents = []
            for obj in self.contains:
                effectiveContents.append(obj.makeDescriptionStr())

            if (len(effectiveContents) > 0):
                outStr += " that looks to have "
                for i in range(len(effectiveContents)):
                    if (i == len(effectiveContents) - 1) and (len(effectiveContents) > 1):
                        outStr += "and "
                    outStr += effectiveContents[i] + ", "
                outStr = outStr[:-2] + " " + self.properties["containerPrefix"] + " it"
            else:
                outStr += " that is empty"

        else:
            outStr += " that is currently closed"

        return outStr

# A pot, which is a container that can be used to heat things up.  It contains things inside of it.  It's always open.
class Pot(Container):
    # Constructor.
    def __init__(self):
        GameObject.__init__(self, "pot")
        Container.__init__(self, "pot")

        self.properties["containerPrefix"] = "in"
        # Set the properties of this object
        self.properties["isOpenable"] = False # A pot is openable
        self.properties["isOpen"] = True      # A pot starts out open
        self.properties["isMoveable"] = True   # A pot can be moved

    def makeDescriptionStr(self, makeDetailed=False):
        outStr = "a pot"

        effectiveContents = []
        for obj in self.contains:
            effectiveContents.append(obj.makeDescriptionStr())

        if (len(effectiveContents) > 0):
            outStr += " that looks to have "
            for i in range(len(effectiveContents)):
                if (i == len(effectiveContents) - 1) and (len(effectiveContents) > 1):
                    outStr += "and "
                outStr += effectiveContents[i] + ", "
            outStr = outStr[:-2] + " " + self.properties["containerPrefix"] + " it"
        else:
            outStr += " that is empty"

        return outStr

# A fridge, which is a cooling device.  It contains things inside of it.  It's always on.  When things are inside it, it cools them down to some temperature.
class Fridge(Container, Device):
    def __init__(self):
        GameObject.__init__(self, "fridge")
        Container.__init__(self, "fridge")
        Device.__init__(self, "fridge")

        self.properties["containerPrefix"] = "in"

        # Set the properties of this object
        self.properties["isOpenable"] = True    # A fridge is openable
        self.properties["isOpen"] = False       # A fridge starts out closed
        self.properties["isMoveable"] = False   # A fridge is too heavy to move (and doesn't really need to be moved for this simulation)

        self.properties["isOn"] = True           # A fridge is always on
        self.properties["isActivatable"] = False # A fridge essentially never is turned off (unless it's unplugged, which is irelevant for this simulation)

        # Set the minimum temperature of the fridge (in degrees Celsius)
        self.properties["minTemperature"] = 4.0        # Minimum temperature of the fridge
        self.properties["temperature_decrease_per_tick"] = 5.0   # How much the temperature decreases per tick

    # Decrease the temperature of anything inside the fridge
    def tick(self):
        # If the fridge is on, then decrease the temperature of anything inside it
        if (self.properties["isOn"] == True):
            # Let's also add fidelity and say the temperature will only decrease if the fridge is closed
            if (self.properties["isOpen"] == False):

                # Get a list of all objects in the fridge
                objectsOnFridge = self.getAllContainedObjectsRecursive()

                # Decrease the temperature of each object in the fridge
                for obj in objectsOnFridge:
                    # Decrease the object's temperature, down to the minimum temperature
                    newTemperature = obj.properties["temperature"] - self.properties["temperature_decrease_per_tick"]
                    if (newTemperature < self.properties["minTemperature"]):
                        newTemperature = self.properties["minTemperature"]
                    obj.properties["temperature"] = newTemperature

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        outStr = "a fridge"

        # A freezer is essentially always on, so we'll only mention it if it's off
        if not self.properties["isOn"]:
            outStr += " that is currently off, and"

        # Check if open
        if self.properties["isOpen"]:
            outStr += " that is currently open"
            # Check if empty
            effectiveContents = []
            for obj in self.contains:
                effectiveContents.append(obj.makeDescriptionStr())

            if (len(effectiveContents) > 0):
                outStr += " that looks to have "
                for i in range(len(effectiveContents)):
                    if (i == len(effectiveContents) - 1) and (len(effectiveContents) > 1):
                        outStr += "and "
                    outStr += effectiveContents[i] + ", "
                outStr = outStr[:-2] + " " + self.properties["containerPrefix"] + " it"
            else:
                outStr += " that is empty"

        else:
            outStr += " that is currently closed"

        return outStr

# A milk, which is a type of object that can be heated up.  It has a certain amount of time before it spoils.
class Milk(GameObject):
    def __init__(self, milkPrefix, milkName, spoilTime=20):
        GameObject.__init__(self, milkName)
        self.properties["milkPrefix"] = milkPrefix  # The prefix to use when referring to the milk item (e.g. "a", "some", "the", etc.)

        self.properties["isMilk"] = True
        self.properties["spoilTime"] = spoilTime    # How long the milk item lasts before it spoils (in steps)
        self.properties["maxTemperature"] = 4.0     # Maximum temperature of the milk item (in degrees Celsius).  If the milk item is hotter than this, it will eventually spoil.
        self.properties["timeAboveMaxTemp"] = 0     # How long the milk item has been above the maximum temperature (in steps)
        self.properties["isSpoiled"] = False        # Whether the milk item is spoiled or not
        self.properties["isAboveMaxTemp"] = True    # Whether the milk item is above the maximum temperature or not (helpful for scoring)

    # Tick the milk item
    def tick(self):
        # Check to see if the milk item is above the maximum temperature
        if (self.properties["temperature"] > self.properties["maxTemperature"]):
            self.properties["isAboveMaxTemp"] = True
        else:
            self.properties["isAboveMaxTemp"] = False

        # If the milk item is above the maximum temperature, then increase the time it's been above the maximum temperature
        if (self.properties["isAboveMaxTemp"] == True):
            self.properties["timeAboveMaxTemp"] += 1

        # If the milk item has been above the maximum temperature for too long, then it spoils
        if (self.properties["timeAboveMaxTemp"] > self.properties["spoilTime"]):
            self.properties["isSpoiled"] = True

    # Get a list of referents (i.e. names that this object can be called by)
    def getReferents(self):
        referents = []
        # Add the milk item's potentially spoiled property as a prefix
        if (self.properties["isSpoiled"]):
            referents.append("spoiled " + self.name)
        referents.append(self.name)
        return referents

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        outStr = self.properties["milkPrefix"] + " "
        if (self.properties["isSpoiled"]):
            outStr += "spoiled "
        outStr += self.name

        return outStr

# A thermometer, which is a device that can be used to measure the temperature of an object.
class Thermometer(Device):
    def __init__(self):
        GameObject.__init__(self, "thermometer")
        Device.__init__(self, "thermometer")

        self.properties["isThermometer"] = True
        self.properties["isActivatable"] = False # A thermometer is not activatable
        self.properties["isOn"] = False         # A thermometer is not on

    # Try to use the thermometer with a patient object (e.g. a light with a person, a fan with a person, etc.)
    # Returns an observation string, and a success flag (boolean)
    def useWithObject(self, patientObject):
        # Check if the patient object is a milk
        if (patientObject.getProperty("isMilk") == True):
            # If so, then return the temperature of the milk
            return ("The " + patientObject.name + " is at " + str(patientObject.properties["temperature"]) + " degrees Celsius.", True)
        else:
            return ("You're not sure how to use the " + self.getReferents()[0] + " with the " + patientObject.name + ".", False)

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        outStr = "a thermometer"

        # A thermometer is essentially always on, so we'll only mention it if it's off
        if not self.properties["isOn"]:
            outStr += " that is currently off, and"

        return outStr


# The world is the root object of the game object tree.  In single room environments, it's where all the objects are located.
class World(Container):
    def __init__(self):
        Container.__init__(self, "kitchen")

    def makeDescriptionStr(self, makeDetailed=False):
        outStr = "You find yourself in a kitchen.  In the kitchen, you see: \n"
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

        # Add a stove
        stove = Stove()
        world.addObject(stove)

        # Add a pot
        pot = Pot()
        world.addObject(pot)

        # Add a fridge
        fridge = Fridge()
        world.addObject(fridge)

        # Add a thermometer
        thermometer = Thermometer()
        world.addObject(thermometer)

        # Create milk
        possibleMilks = []
        possibleMilks.append(Milk("some", "milk", spoilTime=20))

        # Randomly shuffle the milk
        self.random.shuffle(possibleMilks)

        # Add a milk
        milk = possibleMilks[0]
        fridge.addObject(milk)

        # Store the number of milk that need to be heated
        self.numMilkToHeat = 1

        # Return the world
        return world

    # Get the task description for this game
    def getTaskDescription(self):
        return "Your task is to heat the milk to a temperature that is suitable for a baby."

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
        # (1-arg) Eat
        for objReferent, objs in allObjects.items():
            for obj in objs:
                self.addAction("eat " + objReferent, ["eat", obj])

        # (1-arg) Take
        for objReferent, objs in allObjects.items():
            for obj in objs:
                self.addAction("take " + objReferent, ["take", obj])
                self.addAction("take " + objReferent + " from " + obj.parentContainer.getReferents()[0], ["take", obj])

        # (1-arg) Open/Close
        for objReferent, objs in allObjects.items():
            for obj in objs:
                self.addAction("open " + objReferent, ["open", obj])
                self.addAction("close " + objReferent, ["close", obj])

        # (1-arg) Detailed look/examine
        for objReferent, objs in allObjects.items():
            for obj in objs:
                self.addAction("examine " + objReferent, ["examine", obj])

        # (1-arg) Turn on/Turn off device
        for objReferent, objs in allObjects.items():
            for obj in objs:
                self.addAction("turn on " + objReferent, ["turn on", obj])
                self.addAction("turn off " + objReferent, ["turn off", obj])

        # (1-arg) Use
        for objReferent, objs in allObjects.items():
            for obj in objs:
                self.addAction("use " + objReferent, ["use", obj])

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

        # (2-arg) Use
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2):
                            self.addAction("use " + objReferent1 + " on " + objReferent2, ["use", obj1, obj2])

        # (2-arg) Feed
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2):
                            self.addAction("feed " + objReferent1 + " to " + objReferent2, ["feed", obj1, obj2])

        return self.possibleActions

    #
    #   Interpret actions
    #

    # Perform the "eat" action.  Returns an observation string.
    def actionEat(self, obj):
        # Enforce that the object must be in the inventory to do anything with it
        if (obj.parentContainer != self.agent):
            return "You don't currently have the " + obj.getReferents()[0] + " in your inventory."

        # Check if the object is food
        if (obj.getProperty("isFood") == True):
            # Try to pick up/take the food
            obsStr, objRef, success = obj.parentContainer.takeObjectFromContainer(obj)
            if (success == False):
                # If it failed, we were unable to take the food (e.g. it was in a closed container)
                return "You can't see that."

            # Update the game observation
            return "You eat the " + obj.name + "."
        else:
            return "You can't eat that."

    # Open a container
    def actionOpen(self, obj):
        # Check if the object is a container
        if (obj.getProperty("isContainer") == True):
            # This is handled by the object itself
            obsStr, success = obj.openContainer()
            return obsStr
        else:
            return "You can't open that."

    # Close a container
    def actionClose(self, obj):
        # Check if the object is a container
        if (obj.getProperty("isContainer") == True):
            # This is handled by the object itself
            obsStr, success = obj.closeContainer()
            return obsStr
        else:
            return "You can't close that."

    # Take an object from a container
    def actionTake(self, obj):
        # If the object doesn't have a parent container, then it's dangling and something has gone wrong
        if (obj.parentContainer == None):
            return "Something has gone wrong -- that object is dangling in the void.  You can't take that."

        # Take the object from the parent container, and put it in the inventory
        obsStr1, objRef, success = obj.parentContainer.takeObjectFromContainer(obj)
        if (success == False):
            return obsStr1

        # Add the object to the inventory
        self.agent.addObject(obj)
        return obsStr1 + " You put the " + obj.getReferents()[0] + " in your inventory."

    # Put an object in a container
    def actionPut(self, objToMove, newContainer):
        # Check that the destination container is a container
        if (newContainer.getProperty("isContainer") == False):
            return "You can't put things in the " + newContainer.getReferents()[0] + "."

        # Enforce that the object must be in the inventory to do anything with it
        if (objToMove.parentContainer != self.agent):
            return "You don't currently have the " + objToMove.getReferents()[0] + " in your inventory."

        # Take the object from it's current container, and put it in the new container.
        # Deep copy the reference to the original parent container, because the object's parent container will be changed when it's taken from the original container
        originalContainer = objToMove.parentContainer
        obsStr1, objRef, success = objToMove.parentContainer.takeObjectFromContainer(objToMove)
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

    # Use a device on an object
    def actionUse(self, deviceObj, patientObject):
        # Check if the object is a device
        if (deviceObj.getProperty("isDevice") == True):
            # This is handled by the object itself
            obsStr, success = deviceObj.useWithObject(patientObject)
            return obsStr
        else:
            return "You can't use that."

    # Feed a baby with milk
    def actionFeed(self, milkObj, babyObj):
        # Check if the object is a baby
        if (babyObj.getProperty("isBaby") == True):
            # Check if the milk is in the inventory
            if (milkObj.parentContainer != self.agent):
                return "You don't currently have the " + milkObj.getReferents()[0] + " in your inventory."

            # Check if the milk is hot enough
            if (milkObj.getProperty("isAboveMaxTemp") == False):
                return "The " + milkObj.name + " is not hot enough to give to the baby."

            # Try to pick up/take the milk
            obsStr, objRef, success = milkObj.parentContainer.takeObjectFromContainer(milkObj)
            if (success == False):
                # If it failed, we were unable to take the milk (e.g. it was in a closed container)
                return "You can't see that."

            # Update the game observation
            return "You feed the baby with the " + milkObj.name + "."
        else:
            return "You can't feed that."



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
            thingToExamine = action[1]
            self.observationStr = thingToExamine.makeDescriptionStr(makeDetailed = True)
        elif (actionVerb == "eat"):
            # Eat a food
            thingToEat = action[1]
            self.observationStr = self.actionEat(thingToEat)
        elif (actionVerb == "open"):
            # Open a container
            thingToOpen = action[1]
            self.observationStr = self.actionOpen(thingToOpen)
        elif (actionVerb == "close"):
            # Close a container
            thingToClose = action[1]
            self.observationStr = self.actionClose(thingToClose)
        elif (actionVerb == "take"):
            # Take an object from a container
            thingToTake = action[1]
            self.observationStr = self.actionTake(thingToTake)
        elif (actionVerb == "turn on"):
            # Turn on a device
            thingToTurnOn = action[1]
            self.observationStr = self.actionTurnOn(thingToTurnOn)
        elif (actionVerb == "turn off"):
            # Turn off a device
            thingToTurnOff = action[1]
            self.observationStr = self.actionTurnOff(thingToTurnOff)

        elif (actionVerb == "put"):
            # Put an object in a container
            thingToMove = action[1]
            newContainer = action[2]
            self.observationStr = self.actionPut(thingToMove, newContainer)

        elif (actionVerb == "use"):
            # Use a device on an object
            deviceObj = action[1]
            patientObject = action[2]
            self.observationStr = self.actionUse(deviceObj, patientObject)

        elif (actionVerb == "feed"):
            # Feed a baby with milk
            milkObj = action[1]
            babyObj = action[2]
            self.observationStr = self.actionFeed(milkObj, babyObj)

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

        # Give a positive score for each milk that's heated, and a negative score for each milk that's spoiled.
        # Also, give a negative score for each milk that's missing (e.g. it's been eaten)
        numMilksFound = 0
        numMilksChanged = 0     # Milks modified (e.g. spoiled or heated)
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        for obj in allObjects:
            # Check if the object is a milk
            if (obj.getProperty("isMilk") == True):
                # Check if the milk is spoiled
                if (obj.getProperty("isSpoiled") == True):
                    self.score -= 1
                    numMilksChanged += 1
                # Otherwise, check if the milk is hot enough
                elif (obj.getProperty("isAboveMaxTemp") == True):
                    self.score += 1
                    numMilksChanged += 1

                numMilksFound += 1

        # Give a negative score for each milk that's missing (e.g. it's been eaten)
        numMilksMissing = self.numMilkToHeat - numMilksFound
        self.score -= numMilksMissing

        # Check if the game is over
        # Check for winning condition -- score is the same as the number of milk to heat
        if (self.score == self.numMilkToHeat):
            self.gameOver = True
            self.gameWon = True
        # Check for losing condition -- all milk changed, one or more milk are spoiled or missing
        elif ((numMilksChanged + numMilksMissing) >= self.numMilkToHeat):
            self.gameOver = True
            self.gameWon = False
        else:
            self.gameOver = False
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
