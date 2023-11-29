# heating_milk.py
# based on scale-weigh.py
# ruoyao wang (Mar 6/2023)

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

#
#   Specific Game Objects
#

# A device that can be turned on and off
class Device(GameObject):
    def __init__(self, name):
        GameObject.__init__(self, name)
        self.properties["isDevice"] = True
        self.properties["isOn"] = False

    # Try to turn the device on
    # Returns an observation string, and a success flag (boolean)
    def turnOn(self):
        # First, check to see if this object is a device
        if not (self.getProperty("isDevice") == True):
            # If not, then it can't be turned on
            return ("The " + self.name + " is not a device, so it can't be turned on.", False)

        # If this object is a device, then check to see if it is already on
        if self.getProperty("isOn"):
            # If so, then it can't be turned on
            return ("The " + self.name + " is already on.", False)

        # If this object is a device and it is off, then turn it on
        self.properties["isOn"] = True
        return ("The " + self.name + " is now on.", True)

    # Try to turn the device off
    # Returns an observation string, and a success flag (boolean)
    def turnOff(self):
        # First, check to see if this object is a device
        if not (self.getProperty("isDevice") == True):
            # If not, then it can't be turned off
            return ("The " + self.name + " is not a device, so it can't be turned off.", False)

        # If this object is a device, then check to see if it is already off
        if not (self.getProperty("isOn") == True):
            # If so, then it can't be turned off
            return ("The " + self.name + " is already off.", False)

        # If this object is a device and it is on, then turn it off
        self.properties["isOn"] = False
        return ("The " + self.name + " is now off.", True)

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        if self.getProperty("isOn"):
            return "the " + self.name + " (which is on)."
        else:
            return "the " + self.name + " (which is off)."

# A container that can be opened and closed
class OpenableContainer(Container):
    def __init__(self, name):
        Container.__init__(self, name)
        self.properties["isOpenable"] = True

# A container that can be opened and closed, and has a maximum and minimum temperature
class TemperatureControlledContainer(OpenableContainer):
    def __init__(self, name, max_temperature, min_temperature):
        OpenableContainer.__init__(self, name)
        self.properties["max_temperature"] = max_temperature
        self.properties["min_temperature"] = min_temperature

    # Try to set the temperature of the container
    # Returns an observation string, and a success flag (boolean)
    def setTemperature(self, temperature):
        # First, check to see if this object is a temperature controlled container
        if not (self.getProperty("isContainer") == True):
            # If not, then it can't have its temperature set
            return ("The " + self.name + " is not a temperature controlled container, so its temperature can't be set.", False)

        # If this object is a temperature controlled container, then check to see if the temperature is within the valid range
        if (temperature > self.getProperty("max_temperature")) or (temperature < self.getProperty("min_temperature")):
            # If not, then it can't be set
            return ("The " + self.name + " can't be set to " + str(temperature) + " degrees Celsius, because it is outside the valid range of " + str(self.getProperty("min_temperature")) + " to " + str(self.getProperty("max_temperature")) + " degrees Celsius.", False)

        # If this object is a temperature controlled container and the temperature is within the valid range, then set the temperature
        self.properties["temperature"] = temperature
        return ("The " + self.name + " is now set to " + str(temperature) + " degrees Celsius.", True)

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        if self.getProperty("isOpen"):
            return "the " + self.name + " (which is open and set to " + str(self.getProperty("temperature")) + " degrees Celsius)."
        else:
            return "the " + self.name + " (which is closed and set to " + str(self.getProperty("temperature")) + " degrees Celsius)."

# A device that can be turned on and off, and has a temperature increase per tick
class HeatingDevice(Device):
    def __init__(self, name, temperature_increase_per_tick):
        Device.__init__(self, name)
        self.properties["temperature_increase_per_tick"] = temperature_increase_per_tick

    # Game tick: Perform any internal updates that need to be performed at each step of the game.
    def tick(self):
        # First, check to see if this object is a heating device
        if not (self.getProperty("isDevice") == True):
            # If not, then it can't have its temperature increased
            return

        # If this object is a heating device and it is on, then increase the temperature of all objects it contains
        if self.getProperty("isOn"):
            for obj in self.contains:
                if obj.getProperty("isContainer") == True:
                    obj.properties["temperature"] += self.getProperty("temperature_increase_per_tick")

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        if self.getProperty("isOn"):
            return "the " + self.name + " (which is on and set to increase the temperature of all objects it contains by " + str(self.getProperty("temperature_increase_per_tick")) + " degrees Celsius per tick)."
        else:
            return "the " + self.name + " (which is off and set to increase the temperature of all objects it contains by " + str(self.getProperty("temperature_increase_per_tick")) + " degrees Celsius per tick)."

# A device that can be turned on and off, and has a temperature decrease per tick
class CoolingDevice(Device):
    def __init__(self, name, temperature_decrease_per_tick):
        Device.__init__(self, name)
        self.properties["temperature_decrease_per_tick"] = temperature_decrease_per_tick

    # Game tick: Perform any internal updates that need to be performed at each step of the game.
    def tick(self):
        # First, check to see if this object is a cooling device
        if not (self.getProperty("isDevice") == True):
            # If not, then it can't have its temperature decreased
            return

        # If this object is a cooling device and it is on, then decrease the temperature of all objects it contains
        if self.getProperty("isOn"):
            for obj in self.contains:
                if obj.getProperty("isContainer") == True:
                    obj.properties["temperature"] -= self.getProperty("temperature_decrease_per_tick")

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        if self.getProperty("isOn"):
            return "the " + self.name + " (which is on and set to decrease the temperature of all objects it contains by " + str(self.getProperty("temperature_decrease_per_tick")) + " degrees Celsius per tick)."
        else:
            return "the " + self.name + " (which is off and set to decrease the temperature of all objects it contains by " + str(self.getProperty("temperature_decrease_per_tick")) + " degrees Celsius per tick)."

# An object that can be heated or cooled
class TemperatureControlledObject(GameObject):
    def __init__(self, name, temperature):
        GameObject.__init__(self, name)
        self.properties["temperature"] = temperature

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + " (which is currently set to " + str(self.getProperty("temperature")) + " degrees Celsius)."

# The world is the root object of the game object tree.  In single room environments, it's where all the objects are located.
class World(Container):
    def __init__(self):
        Container.__init__(self, "kitchen")

    def makeDescriptionStr(self, makeDetailed=False):
        outStr = "You find yourself in a kitchen. In the kitchen, you see: \n"
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
        # Variable to store the answer
        self.answer_weight = None
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

        # possible objects to heat
        possible_objects = ['milk']
        self.random.shuffle(possible_objects)

        # generate 1-2 objects
        # one object is the target object and the others are distractors
        num_objects = self.random.randint(1, 2)
        temperatures = self.random.choices(range(30, 40), k=num_objects)
        target_id = self.random.randint(0, num_objects-1)

        for i in range(num_objects):
            obj = TemperatureControlledObject(possible_objects[i],temperatures[i])
            world.addObject(obj)

        # record the target object name weight
        self.target_object = possible_objects[target_id]
        self.target_temperature = temperatures[target_id]

        # Add a stove
        stove = HeatingDevice("stove", 1)
        world.addObject(stove)

        # Add a fridge
        fridge = CoolingDevice("fridge", 1)
        world.addObject(fridge)

        # Add a pot
        pot = TemperatureControlledContainer("pot", 100, 0)
        world.addObject(pot)

        # Add a thermometer
        thermometer = Device("thermometer")
        world.addObject(thermometer)

        # Return the world
        return world

    # Get the task description for this game
    def getTaskDescription(self):
        return f"Your task is to heat the {self.target_object} to a temperature that is suitable for a baby to drink."

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
                self.addAction("take " + objReferent + " from " + obj.parentContainer.getReferents()[0], ["take", obj])

        # (1-arg) Detailed look/examine
        for objReferent, objs in allObjects.items():
            for obj in objs:
                self.addAction("examine " + objReferent, ["examine", obj])

        # (1-arg) Open
        for objReferent, objs in allObjects.items():
            for obj in objs:
                self.addAction("open " + objReferent, ["open", obj])

        # (1-arg) Close
        for objReferent, objs in allObjects.items():
            for obj in objs:
                self.addAction("close " + objReferent, ["close", obj])

        # (1-arg) Turn on
        for objReferent, objs in allObjects.items():
            for obj in objs:
                self.addAction("turn on " + objReferent, ["turn on", obj])

        # (1-arg) Turn off
        for objReferent, objs in allObjects.items():
            for obj in objs:
                self.addAction("turn off " + objReferent, ["turn off", obj])

        # (1-arg) Use thermometer on object
        for objReferent, objs in allObjects.items():
            for obj in objs:
                self.addAction("use thermometer on " + objReferent, ["use thermometer on", obj])

        # (1-arg) Feed baby with milk
        for objReferent, objs in allObjects.items():
            for obj in objs:
                self.addAction("feed baby with " + objReferent, ["feed baby with", obj])

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



        return self.possibleActions

    #
    #   Interpret actions
    #

    # Take an object from a container
    def actionTake(self, obj):
        # If the object doesn't have a parent container, then it's dangling and something has gone wrong
        if (obj.parentContainer == None):
            return "Something has gone wrong -- that object is dangling in the void.  You can't take that."

        # Take the object from the parent container, and put it in the inventory
        obsStr, objRef, success = obj.parentContainer.takeObjectFromContainer(obj)
        if (success == False):
            return obsStr

        # Add the object to the inventory
        self.agent.addObject(obj)
        return obsStr + " You put the " + obj.getReferents()[0] + " in your inventory."

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

    # Open a container
    def actionOpen(self, obj):
        # Check that the object is a container
        if (obj.getProperty("isContainer") == False):
            return "You can't open the " + obj.getReferents()[0] + "."

        # Open the container
        obsStr, success = obj.openContainer()
        if (success == False):
            return obsStr

        # Success -- show the observation
        return obsStr

    # Close a container
    def actionClose(self, obj):
        # Check that the object is a container
        if (obj.getProperty("isContainer") == False):
            return "You can't close the " + obj.getReferents()[0] + "."

        # Close the container
        obsStr, success = obj.closeContainer()
        if (success == False):
            return obsStr

        # Success -- show the observation
        return obsStr

    # Turn on a device
    def actionTurnOn(self, obj):
        # Check that the object is a device
        if (obj.getProperty("isDevice") == False):
            return "You can't turn on the " + obj.getReferents()[0] + "."

        # Turn on the device
        obsStr, success = obj.turnOn()
        if (success == False):
            return obsStr

        # Success -- show the observation
        return obsStr

    # Turn off a device
    def actionTurnOff(self, obj):
        # Check that the object is a device
        if (obj.getProperty("isDevice") == False):
            return "You can't turn off the " + obj.getReferents()[0] + "."

        # Turn off the device
        obsStr, success = obj.turnOff()
        if (success == False):
            return obsStr

        # Success -- show the observation
        return obsStr

    # Use a thermometer on an object
    def actionUseThermometerOn(self, thermometer, obj):
        # Check that the thermometer is a device
        if (thermometer.getProperty("isDevice") == False):
            return "You can't use the " + thermometer.getReferents()[0] + "."

        # Check that the object is a temperature controlled object
        if (obj.getProperty("isTemperatureControlledObject") == False):
            return "You can't use the " + thermometer.getReferents()[0] + " on the " + obj.getReferents()[0] + "."

        # Use the thermometer on the object
        obsStr = "You use the " + thermometer.getReferents()[0] + " on the " + obj.getReferents()[0] + " and see that it is currently set to " + str(obj.getProperty("temperature")) + " degrees Celsius."
        return obsStr

    # Feed baby with milk
    def actionFeedBabyWith(self, milk):
        # Check that the milk is a temperature controlled object
        if (milk.getProperty("isTemperatureControlledObject") == False):
            return "You can't feed the baby with the " + milk.getReferents()[0] + "."

        # Check that the milk is in the pot
        if (milk.parentContainer != pot):
            return "You don't currently have the " + milk.getReferents()[0] + " in the pot."

        # Check that the pot is on the stove
        if (pot.parentContainer != stove):
            return "You don't currently have the pot on the stove."

        # Check that the stove is on
        if (stove.getProperty("isOn") == False):
            return "You need to turn on the stove before you can heat the milk."

        # Check that the temperature of the milk is suitable for a baby to drink
        if (milk.getProperty("temperature") < 37):
            return "The temperature of the milk is not suitable for a baby to drink."

        # Feed the baby with the milk
        obsStr = "You feed the baby with the " + milk.getReferents()[0] + "."
        self.gameOver = True
        self.gameWon = True
        return obsStr


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
        elif (actionVerb == "take"):
            # Take an object from a container
            thingToTake = action[1]
            self.observationStr = self.actionTake(thingToTake)
        elif (actionVerb == "put"):
            # Put an object in a container
            thingToMove = action[1]
            newContainer = action[2]
            self.observationStr = self.actionPut(thingToMove, newContainer)
        elif (actionVerb == "open"):
            # Open a container
            thingToOpen = action[1]
            self.observationStr = self.actionOpen(thingToOpen)
        elif (actionVerb == "close"):
            # Close a container
            thingToClose = action[1]
            self.observationStr = self.actionClose(thingToClose)
        elif (actionVerb == "turn on"):
            # Turn on a device
            thingToTurnOn = action[1]
            self.observationStr = self.actionTurnOn(thingToTurnOn)
        elif (actionVerb == "turn off"):
            # Turn off a device
            thingToTurnOff = action[1]
            self.observationStr = self.actionTurnOff(thingToTurnOff)
        elif (actionVerb == "use thermometer on"):
            # Use a thermometer on an object
            thermometer = action[1]
            thingToUseThermometerOn = action[2]
            self.observationStr = self.actionUseThermometerOn(thermometer, thingToUseThermometerOn)
        elif (actionVerb == "feed baby with"):
            # Feed baby with milk
            milk = action[1]
            self.observationStr = self.actionFeedBabyWith(milk)
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

        if self.gameWon:
            self.score += 1



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
