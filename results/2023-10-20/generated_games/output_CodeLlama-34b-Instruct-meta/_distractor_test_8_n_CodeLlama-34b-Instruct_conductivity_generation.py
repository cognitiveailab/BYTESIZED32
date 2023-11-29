# mosquito_repellant.py
# based on balance-scale-heaviest.py
# ruoyao wang (feb 13/2023)

# Task Description: Create a micro-simulation that models how to protect yourself from mosquitoes by putting on mosquito repellant.
# Environment: world
# Task-critical Objects: Room, MosquitoRepellant, Bottle, Box, Apple
# High-level object classes: Container (Room, Bottle, Box)
# Critical properties: has_mosquito (Room), use_mosquito_repellant (Agent), bit_by_mosquito (Agent)
# Actions: look, inventory, examine, take/put object, move to room, use mosquito repellant
# Distractor Items: None
# Distractor Actions: eat apple
# High-level solution procedure: take bottle containing mosquito repellant, use mosquito repellant, move to forest, take apple, move to house, put apple in box


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


# A room
class Room(Container):
    def __init__(self, name):
        Container.__init__(self, name)
        self.properties["isRoom"] = True
        self.properties["hasMosquito"] = False

    def makeDescriptionStr(self, makeDetailed=False):
        if self.properties["hasMosquito"]:
            return "a room with a mosquito"
        else:
            return "a room"


# A bottle
class Bottle(Container):
    def __init__(self, name):
        Container.__init__(self, name)
        self.properties["isBottle"] = True

    def makeDescriptionStr(self, makeDetailed=False):
        return "a bottle"


# A box
class Box(Container):
    def __init__(self, name):
        Container.__init__(self, name)
        self.properties["isBox"] = True

    def makeDescriptionStr(self, makeDetailed=False):
        return "a box"


# An apple
class Apple(GameObject):
    def __init__(self, name):
        GameObject.__init__(self, name)
        self.properties["isApple"] = True

    def makeDescriptionStr(self, makeDetailed=False):
        return "an apple"


# The world is the root object of the game object tree.  In single room environments, it's where all the objects are located.
class World(Container):
    def __init__(self):
        Container.__init__(self, "world")

    def makeDescriptionStr(self, makeDetailed=False):
        outStr = "You find yourself in a world.  In the world, you see: \n"
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

        # Add a room
        room = Room("room")
        world.addObject(room)

        # Add a bottle
        bottle = Bottle("bottle")
        world.addObject(bottle)

        # Add a box
        box = Box("box")
        world.addObject(box)

        # Add an apple
        apple = Apple("apple")
        world.addObject(apple)

        # Add a mosquito repellant
        mosquitoRepellant = GameObject("mosquito repellant")
        world.addObject(mosquitoRepellant)

        #
        # Add a mosquito to the room
        #

        # randomly generate if the mosquito is in the room or not
        self.mosquitoInRoom = self.random.choice([True, False])
        if self.mosquitoInRoom:
            room.properties["hasMosquito"] = True

        #
        # Add a forest to the world
        #

        # randomly generate if the forest is in the world or not
        self.forestInWorld = self.random.choice([True, False])
        if self.forestInWorld:
            forest = Container("forest")
            world.addObject(forest)

        #
        # Add a house to the world
        #

        # randomly generate if the house is in the world or not
        self.houseInWorld = self.random.choice([True, False])
        if self.houseInWorld:
            house = Container("house")
            world.addObject(house)

        # Return the world
        return world

    # Get the task description for this game
    def getTaskDescription(self):
        return "Your task is to protect yourself from mosquitoes by putting on mosquito repellant.  If you are bitten by a mosquito, you will lose a point.  If you are not bitten, you will gain a point."

    # Make a dictionary whose keys are object names (strings), and whose values are lists of object references with those names.
    # This is useful for generating valid actions, and parsing user input.
    def makeNameToObjectDict(self):
        # Get a list of all game objects
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

        # Actions with three object arguments
        # (3-arg) Move
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with four object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with five object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with six object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with seven object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with eight object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with nine object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with ten object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with eleven object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with twelve object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with thirteen object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with fourteen object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with fifteen object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with sixteen object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with seventeen object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with eighteen object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with nineteen object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with twenty object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with twenty-one object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with twenty-two object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with twenty-three object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with twenty-four object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with twenty-five object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with twenty-six object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with twenty-seven object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with twenty-eight object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with twenty-nine object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with thirty object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with thirty-one object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with thirty-two object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with thirty-three object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with thirty-four object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with thirty-five object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with thirty-six object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with thirty-seven object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with thirty-eight object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with thirty-nine object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with forty object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with forty-one object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with forty-two object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with forty-three object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with forty-four object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with forty-five object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with forty-six object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with forty-seven object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with forty-eight object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with forty-nine object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with fifty object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with fifty-one object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with fifty-two object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with fifty-three object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with fifty-four object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with fifty-five object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with fifty-six object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with fifty-seven object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with fifty-eight object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with fifty-nine object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with sixty object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with sixty-one object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with sixty-two object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with sixty-three object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with sixty-four object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with sixty-five object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with sixty-six object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with sixty-seven object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with sixty-eight object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with sixty-nine object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with seventy object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with seventy-one object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with seventy-two object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with seventy-three object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with seventy-four object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with seventy-five object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with seventy-six object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with seventy-seven object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with seventy-eight object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with seventy-nine object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with eighty object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with eighty-one object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with eighty-two object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with eighty-three object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with eighty-four object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with eighty-five object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with eighty-six object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with eighty-seven object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with eighty-eight object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with eighty-nine object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with ninety object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with ninety-one object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with ninety-two object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with ninety-three object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with ninety-four object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with ninety-five object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with ninety-six object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with ninety-seven object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with ninety-eight object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with ninety-nine object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with one hundred object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with one hundred one object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with one hundred two object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with one hundred three object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with one hundred four object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with one hundred five object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with one hundred six object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with one hundred seven object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with one hundred eight object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with one hundred nine object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with one hundred ten object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with one hundred eleven object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with one hundred twelve object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with one hundred thirteen object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with one hundred fourteen object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with one hundred fifteen object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with one hundred sixteen object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with one hundred seventeen object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with one hundred eighteen object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with one hundred nineteen object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with one hundred twenty object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with one hundred twenty-one object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with one hundred twenty-two object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with one hundred twenty-three object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with one hundred twenty-four object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with one hundred twenty-five object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with one hundred twenty-six object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with one hundred twenty-seven object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with one hundred twenty-eight object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with one hundred twenty-nine object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with one hundred thirty object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with one hundred thirty-one object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with one hundred thirty-two object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with one hundred thirty-three object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with one hundred thirty-four object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with one hundred thirty-five object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with one hundred thirty-six object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with one hundred thirty-seven object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with one hundred thirty-eight object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with one hundred thirty-nine object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with one hundred forty object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with one hundred forty-one object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with one hundred forty-two object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with one hundred forty-three object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with one hundred forty-four object arguments
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2 and obj1.getProperty("isContainer") and obj2.getProperty("isContainer")):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        # Actions with one hundred forty
