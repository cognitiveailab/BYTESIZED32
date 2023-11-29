# led.py
# based on bird-life-cycle.py
# ruoyao wang (feb 8/2023)

# Task: Create a micro-simulation that models how to lit an LED.
# Environment: workshop
# Task-critical Objects: LED, Wire, Battery
# High-level object classes: ElectricalObject (LED, Wire, Battery)
# Critical properties: connects (ElectricalObject), is_conductive (ElectricalObject), on (LED)
# Actions: look, inventory, examine, take/put object, connect X terminal A to Y terminal B
# Distractor Items: ElectricalObject
# Distractor Actions: None
# High-level solution procedure: connect battery anode to LED anode with a wire, connect battery cathode to LED cathode with a wire

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


# A workshop is a container that is always open
class Workshop(Container):
    def __init__(self, name):
        GameObject.__init__(self, name)
        Container.__init__(self, name)
        self.properties["isOpen"] = True
        self.properties["containerPrefix"] = "in the workshop"

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the workshop."


# An electrical object is a game object that can be connected to other electrical objects
class ElectricalObject(GameObject):
    def __init__(self, name):
        GameObject.__init__(self, name)
        self.properties["isElectrical"] = True
        self.properties["connects"] = []
        self.properties["is_conductive"] = False

    # Try to connect this object to another object
    # Returns an observation string, and a success flag (boolean)
    def connectTo(self, obj):
        # First, check to see if this object is electrical
        if not (self.getProperty("isElectrical") == True):
            # If not, then it can't be connected to anything
            return ("The " + self.name + " is not electrical, so it can't be connected to anything.", False)

        # If this object is electrical, then check to see if it is already connected to the other object
        if obj in self.properties["connects"]:
            # If so, then it can't be connected again
            return ("The " + self.name + " is already connected to the " + obj.name + ".", False)

        # If this object is electrical and it is not already connected to the other object, then connect it
        self.properties["connects"].append(obj)
        return ("The " + self.name + " is now connected to the " + obj.name + ".", True)

    # Try to disconnect this object from another object
    # Returns an observation string, and a success flag (boolean)
    def disconnectFrom(self, obj):
        # First, check to see if this object is electrical
        if not (self.getProperty("isElectrical") == True):
            # If not, then it can't be disconnected from anything
            return ("The " + self.name + " is not electrical, so it can't be disconnected from anything.", False)

        # If this object is electrical, then check to see if it is connected to the other object
        if obj not in self.properties["connects"]:
            # If not, then it can't be disconnected
            return ("The " + self.name + " is not connected to the " + obj.name + ".", False)

        # If this object is electrical and it is connected to the other object, then disconnect it
        self.properties["connects"].remove(obj)
        return ("The " + self.name + " is now disconnected from the " + obj.name + ".", True)

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."


# A LED is an electrical object that can be turned on and off
class LED(ElectricalObject):
    def __init__(self, name):
        ElectricalObject.__init__(self, name)
        self.properties["is_conductive"] = True
        self.properties["on"] = False

    # Try to turn the LED on
    # Returns an observation string, and a success flag (boolean)
    def turnOn(self):
        # First, check to see if the LED is connected to a power source
        if not (self.getProperty("is_conductive") == True):
            # If not, then it can't be turned on
            return ("The " + self.name + " is not connected to a power source, so it can't be turned on.", False)

        # If the LED is connected to a power source, then turn it on
        self.properties["on"] = True
        return ("The " + self.name + " is now on.", True)

    # Try to turn the LED off
    # Returns an observation string, and a success flag (boolean)
    def turnOff(self):
        # First, check to see if the LED is connected to a power source
        if not (self.getProperty("is_conductive") == True):
            # If not, then it can't be turned off
            return ("The " + self.name + " is not connected to a power source, so it can't be turned off.", False)

        # If the LED is connected to a power source, then turn it off
        self.properties["on"] = False
        return ("The " + self.name + " is now off.", True)

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        if self.properties["on"]:
            return "the " + self.name + " (which is on)."
        else:
            return "the " + self.name + " (which is off)."


# A wire is an electrical object that can be connected to other electrical objects
class Wire(ElectricalObject):
    def __init__(self, name):
        ElectricalObject.__init__(self, name)
        self.properties["is_conductive"] = True

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."


# A battery is an electrical object that can be connected to other electrical objects
class Battery(ElectricalObject):
    def __init__(self, name):
        ElectricalObject.__init__(self, name)
        self.properties["is_conductive"] = True

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."


# The world is the root object of the game object tree.  In single room environments, it's where all the objects are located.
class World(Workshop):
    def __init__(self):
        Workshop.__init__(self, "workshop")

    def makeDescriptionStr(self, makeDetailed=False):
        return "You are in the workshop. There is a LED, a wire, and a battery here."


class TextGame:

    def __init__(self, randomSeed):
        # Random number generator, initialized with a seed passed as an argument
        self.random = random.Random(randomSeed)

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

        # Generate a LED, a wire, and a battery
        led = LED("LED")
        wire = Wire("wire")
        battery = Battery("battery")

        # Add the objects to the world
        world.addObject(led)
        world.addObject(wire)
        world.addObject(battery)

        # Return the world
        return world

    # Get the task description for this game
    def getTaskDescription(self):
        return "Your task is to connect the battery to the LED using the wire."

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
        allObjects = self.makeNameToObjectDict()

        # Make a dictionary whose keys are possible action strings, and whose values are lists that contain the arguments.
        self.possibleActions = {}

        # Actions with zero arguments
        # (0-arg) Look around the environment
        self.addAction("look around", ["look around"])
        self.addAction("look", ["look around"])

        # Actions with one object argument
        # (1-arg) Examine an object
        for objReferent, objs in allObjects.items():
            for obj in objs:
                self.addAction("examine " + objReferent, ["examine", obj])

        # Actions with two object arguments
        # (2-arg) Connect X terminal A to Y terminal B
        for objReferent1, objs1 in allObjects.items():
            for obj1 in objs1:
                for objReferent2, objs2 in allObjects.items():
                    for obj2 in objs2:
                        self.addAction("connect " + objReferent1 + " terminal A to " + objReferent2 + " terminal B", ["connect", obj1, obj2])

        return self.possibleActions

    #
    #   Interpret actions
    #


    # Connect two electrical objects
    def actionConnect(self, obj1, obj2):
        # Check if the objects are electrical
        if not (obj1.getProperty("isElectrical") == True) or not (obj2.getProperty("isElectrical") == True):
            return "One or both of the objects are not electrical, so they can't be connected."

        # Check if the objects are already connected
        if obj1 in obj2.properties["connects"] or obj2 in obj1.properties["connects"]:
            return "The objects are already connected."

        # Connect the objects
        obj1.connectTo(obj2)
        obj2.connectTo(obj1)
        return "The objects are now connected."



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
        elif (actionVerb == "examine"):
            obj = action[1]
            self.observationStr = obj.makeDescriptionStr()
        elif (actionVerb == "connect"):
            obj1 = action[1]
            obj2 = action[2]
            self.observationStr = self.actionConnect(obj1, obj2)


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
        self.rootObject.tick()
        # Get a list of all objects in the environment
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        # Loop through all objects, and call their tick()
        for obj in allObjects:
            obj.tick()

    # Calculate the game score
    def calculateScore(self):
        # Baseline score
        self.score = 0

        # Check if the LED is on
        led = self.rootObject.containsItemWithName("LED")[0]
        if led.getProperty("on"):
            self.score += 1
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
