# melting_butter.py
# based on space-walk.py
# ruoyao wang (apr 29/2023)

# Task Description: Create a micro-simulation that models how to melt butter
# Environment: room
# Task-critical Objects: Stove, Butter, Pot
# High-level object classes: Device (Stove), Container (Stove, Pot) 
# Critical properties: maxTemperature (Stove), tempIncreasePerTick (Stove), temperature (Butter), stateOfMatter (Butter), solidName/liquidName/gasName (Butter), meltingPoint/boilingPoint (Butter)
# Actions: look, inventory, examine, take/put object, turn on/off, eat butter
# Distractor Items: None
# Distractor Actions: eat butter
# High-level solution procedure: take butter, put butter in pot, take pot, put pot on stove, turn on stove, wait till butter melts

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
        return f"a {self.name}"


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
        return "a " + self.name


# A device
class Device(GameObject):
    def __init__(self, name):
        GameObject.__init__(self, name)
        self.properties["isDevice"] = True
        self.properties["isOn"] = False

    # Turn the device on
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

    # Turn the device off
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
        return "a " + self.name


# A container that can hold liquids
class LiquidContainer(Container):
    def __init__(self, name):
        Container.__init__(self, name)
        self.properties["isLiquidContainer"] = True
        self.properties["liquidName"] = "liquid"
        self.properties["maxLiquidVolume"] = 100
        self.properties["currentLiquidVolume"] = 0

    # Add liquid to the container
    # Returns an observation string, and a success flag (boolean)
    def addLiquid(self, amount):
        # First, check to see if this object is a liquid container
        if not (self.getProperty("isLiquidContainer") == True):
            # If not, then it can't hold liquid
            return ("The " + self.name + " is not a liquid container, so liquid can't be added to it.", False)

        # If this object is a liquid container, then check to see if it is already full
        if self.getProperty("currentLiquidVolume") >= self.getProperty("maxLiquidVolume"):
            # If so, then it can't hold any more liquid
            return ("The " + self.name + " is already full of " + self.getProperty("liquidName") + ".", False)

        # If this object is a liquid container and it is not full, then add the liquid
        self.properties["currentLiquidVolume"] += amount
        return ("The " + self.name + " is now filled with " + str(self.getProperty("currentLiquidVolume")) + " ml of " + self.getProperty("liquidName") + ".", True)

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "a " + self.name + " containing " + str(self.getProperty("currentLiquidVolume")) + " ml of " + self.getProperty("liquidName")


# A stove
class Stove(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isStove"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10
        self.properties["currentTemperature"] = 0

    # Turn the stove on
    # Returns an observation string, and a success flag (boolean)
    def turnOn(self):
        # First, check to see if this object is a stove
        if not (self.getProperty("isStove") == True):
            # If not, then it can't be turned on
            return ("The " + self.name + " is not a stove, so it can't be turned on.", False)

        # If this object is a stove, then check to see if it is already on
        if self.getProperty("isOn"):
            # If so, then it can't be turned on
            return ("The " + self.name + " is already on.", False)

        # If this object is a stove and it is off, then turn it on
        self.properties["isOn"] = True
        return ("The " + self.name + " is now on.", True)

    # Turn the stove off
    # Returns an observation string, and a success flag (boolean)
    def turnOff(self):
        # First, check to see if this object is a stove
        if not (self.getProperty("isStove") == True):
            # If not, then it can't be turned off
            return ("The " + self.name + " is not a stove, so it can't be turned off.", False)

        # If this object is a stove, then check to see if it is already off
        if not (self.getProperty("isOn") == True):
            # If so, then it can't be turned off
            return ("The " + self.name + " is already off.", False)

        # If this object is a stove and it is on, then turn it off
        self.properties["isOn"] = False
        return ("The " + self.name + " is now off.", True)

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "a " + self.name


# A pot
class Pot(LiquidContainer):
    def __init__(self, name):
        LiquidContainer.__init__(self, name)
        self.properties["isPot"] = True
        self.properties["maxLiquidVolume"] = 100
        self.properties["currentLiquidVolume"] = 0

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "a " + self.name + " containing " + str(self.getProperty("currentLiquidVolume")) + " ml of " + self.getProperty("liquidName")


# A butter
class Butter(GameObject):
    def __init__(self, name):
        GameObject.__init__(self, name)
        self.properties["isButter"] = True
        self.properties["temperature"] = 20
        self.properties["stateOfMatter"] = "solid"
        self.properties["solidName"] = "butter"
        self.properties["liquidName"] = "melted butter"
        self.properties["gasName"] = "butter gas"
        self.properties["meltingPoint"] = 30
        self.properties["boilingPoint"] = 100

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "a " + self.name


# The world is the root object of the game object tree.
class World(Container):
    def __init__(self):
        Container.__init__(self, "room")

    # Describe the a room
    def makeDescriptionStr(self, room, makeDetailed=False):
        outStr = room.makeDescriptionStr()
        # describe room connection information
        outStr += "You also see:\n"
        for direction in room.connects:
            if room.connects[direction] is not None:
                outStr += f"\t a way to {direction}\n"

        return outStr

# The agent
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
        self.observationStr = self.rootObject.makeDescriptionStr(self.current_room)
        # Do calculate initial scoring
        self.calculateScore()

    # Create/initialize the world/environment for this game
    def initializeWorld(self):
        world = World()

        # Add a stove
        stove = Stove("stove")
        world.addObject(stove)

        # Add a pot
        pot = Pot("pot")
        world.addObject(pot)

        # Add butter
        butter = Butter("butter")
        world.addObject(butter)

        # Return the world
        return world

    # Get the task description for this game
    def getTaskDescription(self):
        return "Your task is to melt the butter. You win the game by melting the butter."

    # Make a dictionary whose keys are object names (strings), and whose values are lists of object references with those names.
    # This is useful for generating valid actions, and parsing user input.
    def makeNameToObjectDict(self):
        # Get a list of all game objects that could serve as arguments to actions
        allObjects = self.current_room.getAllContainedObjectsRecursive()

        # Make a dictionary whose keys are object names (strings), and whose values are lists of object references with those names.
        nameToObjectDict = {}
        for obj in allObjects:
            if obj not in self.current_room.buried:
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

        # (1-arg) Examine
        for objReferent, objs in allObjects.items():
            for obj in objs:
                self.addAction("examine " + objReferent, ["examine", obj])

        # (1-arg) Turn on
        for objReferent, objs in allObjects.items():
            for obj in objs:
                if obj.getProperty("isDevice"):
                    self.addAction("turn on " + objReferent, ["turn on", obj])

        # (1-arg) Turn off
        for objReferent, objs in allObjects.items():
            for obj in objs:
                if obj.getProperty("isDevice"):
                    self.addAction("turn off " + objReferent, ["turn off", obj])

        # (1-arg) Add liquid
        for objReferent, objs in allObjects.items():
            for obj in objs:
                if obj.getProperty("isLiquidContainer"):
                    self.addAction("add liquid to " + objReferent, ["add liquid", obj])

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
        # Check to make sure the object is in the environment
        if (obj.parentContainer == None):
            return "Something has gone wrong -- that object is dangling in the void.  You can't examine that."

        # Check to make sure the object is in the agent's inventory or the current room
        if (obj.parentContainer != self.agent) and (obj.parentContainer != self.current_room):
            return "You don't currently have the " + obj.getReferents()[0] + " in your inventory or in the current room."

        # Return a description of the object
        return obj.makeDescriptionStr()

    # Turn on a device
    def actionTurnOn(self, device):
        # Check to make sure the object is a device
        if (device.getProperty("isDevice") == False):
            return "You can't turn on the " + device.getReferents()[0] + "."

        # Check to make sure the device is in the environment
        if (device.parentContainer == None):
            return "Something has gone wrong -- that device is dangling in the void.  You can't turn it on."

        # Check to make sure the device is in the agent's inventory or the current room
        if (device.parentContainer != self.agent) and (device.parentContainer != self.current_room):
            return "You don't currently have the " + device.getReferents()[0] + " in your inventory or in the current room."

        # Turn the device on
        obsStr, success = device.turnOn()
        if (success == False):
            return obsStr

        # Success -- show the observation
        return obsStr

    # Turn off a device
    def actionTurnOff(self, device):
        # Check to make sure the object is a device
        if (device.getProperty("isDevice") == False):
            return "You can't turn off the " + device.getReferents()[0] + "."

        # Check to make sure the device is in the environment
        if (device.parentContainer == None):
            return "Something has gone wrong -- that device is dangling in the void.  You can't turn it off."

        # Check to make sure the device is in the agent's inventory or the current room
        if (device.parentContainer != self.agent) and (device.parentContainer != self.current_room):
            return "You don't currently have the " + device.getReferents()[0] + " in your inventory or in the current room."

        # Turn the device off
        obsStr, success = device.turnOff()
        if (success == False):
            return obsStr

        # Success -- show the observation
        return obsStr

    # Add liquid to a container
    def actionAddLiquid(self, container):
        # Check to make sure the object is a liquid container
        if (container.getProperty("isLiquidContainer") == False):
            return "You can't add liquid to the " + container.getReferents()[0] + "."

        # Check to make sure the container is in the environment
        if (container.parentContainer == None):
            return "Something has gone wrong -- that container is dangling in the void.  You can't add liquid to it."

        # Check to make sure the container is in the agent's inventory or the current room
        if (container.parentContainer != self.agent) and (container.parentContainer != self.current_room):
            return "You don't currently have the " + container.getReferents()[0] + " in your inventory or in the current room."

        # Add liquid to the container
        obsStr, success = container.addLiquid(10)
        if (success == False):
            return obsStr

        # Success -- show the observation
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
            self.observationStr = self.rootObject.makeDescriptionStr(self.agent.parentContainer)
        elif (actionVerb == "inventory"):
            # Display the agent's inventory
            self.observationStr = self.actionInventory()
        elif (actionVerb == "take"):
            # Take an object from a container
            thingToTake = action[1]
            self.observationStr = self.actionTake(thingToTake)
        elif (actionVerb == "put"):
            # Put an object in a container
            thingToMove = action[1]
            newContainer = action[2]
            self.observationStr = self.actionPut(thingToMove, newContainer)
        elif (actionVerb == "examine"):
            # Examine an object
            thingToExamine = action[1]
            self.observationStr = self.actionExamine(thingToExamine)
        elif (actionVerb == "turn on"):
            # Turn on a device
            deviceToTurnOn = action[1]
            self.observationStr = self.actionTurnOn(deviceToTurnOn)
        elif (actionVerb == "turn off"):
            # Turn off a device
            deviceToTurnOff = action[1]
            self.observationStr = self.actionTurnOff(deviceToTurnOff)
        elif (actionVerb == "add liquid"):
            # Add liquid to a container
            containerToAddLiquid = action[1]
            self.observationStr = self.actionAddLiquid(containerToAddLiquid)
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

        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        for obj in allObjects:
            if obj.name == "butter" and type(obj.parentContainer) == Pot and obj.getProperty("stateOfMatter") == "liquid":
                self.score = 1
                self.gameOver = True
                self.gameWon = True




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