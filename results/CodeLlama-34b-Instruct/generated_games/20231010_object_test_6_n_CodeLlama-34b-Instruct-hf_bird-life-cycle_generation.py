# led-lighting.py
# based on make-ice-cubes.py
# ruoyao wang (feb 7/2023)

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


# A class for electrical objects (e.g. LED, Wire, Battery)
class ElectricalObject(GameObject):
    def __init__(self, name):
        GameObject.__init__(self, name)
        self.properties["isElectrical"] = True
        self.properties["isConductive"] = False
        self.properties["isOn"] = False

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        if self.getProperty("isOn"):
            return "the " + self.name + " (on)"
        else:
            return "the " + self.name + " (off)"

    # Get a list of referents (i.e. names that this object can be called by)
    def getReferents(self):
        return [self.name, "the " + self.name]


# A class for LEDs
class LED(ElectricalObject):
    def __init__(self, name):
        ElectricalObject.__init__(self, name)
        self.properties["isConductive"] = True
        self.properties["isOn"] = False

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        if self.getProperty("isOn"):
            return "the " + self.name + " (on)"
        else:
            return "the " + self.name + " (off)"

    # Get a list of referents (i.e. names that this object can be called by)
    def getReferents(self):
        return [self.name, "the " + self.name]

# A class for Wires
class Wire(ElectricalObject):
    def __init__(self, name):
        ElectricalObject.__init__(self, name)
        self.properties["isConductive"] = True
        self.properties["isOn"] = False

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        if self.getProperty("isOn"):
            return "the " + self.name + " (on)"
        else:
            return "the " + self.name + " (off)"

    # Get a list of referents (i.e. names that this object can be called by)
    def getReferents(self):
        return [self.name, "the " + self.name]

# A class for Batteries
class Battery(ElectricalObject):
    def __init__(self, name):
        ElectricalObject.__init__(self, name)
        self.properties["isConductive"] = True
        self.properties["isOn"] = False

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        if self.getProperty("isOn"):
            return "the " + self.name + " (on)"
        else:
            return "the " + self.name + " (off)"

    # Get a list of referents (i.e. names that this object can be called by)
    def getReferents(self):
        return [self.name, "the " + self.name]

# The world is the root object of the game object tree.  In single room environments, it's where all the objects are located.
class World(Container):
    def __init__(self):
        Container.__init__(self, "workshop")

    def makeDescriptionStr(self, makeDetailed=False):
        outStr = "You are in a workshop.  In the workshop, you see: \n"
        for obj in self.contains:
            outStr += "\t" + obj.makeDescriptionStr() + "\n"

        return outStr


# The agent (just a placeholder for a container for the inventory)
class Agent(ElectricalObject):
    def __init__(self):
        GameObject.__init__(self, "agent")
        ElectricalObject.__init__(self, "agent")

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

        # Add the agent (the player) into the world (workshop)
        world.addObject(self.agent)
        # Add a LED into the workshop
        led = LED("LED")
        world.addObject(led)
        # Add a Wire into the workshop
        wire = Wire("Wire")
        world.addObject(wire)
        # Add a Battery into the workshop
        battery = Battery("Battery")
        world.addObject(battery)

        # Return the world
        return world

    # Get the task description for this game
    def getTaskDescription(self):
        return f"Your task is to light the LED."

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

        # (0-arg) Look at the agent's current inventory
        self.addAction("inventory", ["inventory"])

        # Actions with one object argument
        # (1-arg) Examine
        for objReferent, objs in allObjects.items():
            for obj in objs:
                self.addAction("examine " + objReferent, ["examine", obj])

        # (1-arg) Take/put object
        for objReferent, objs in allObjects.items():
            for obj in objs:
                self.addAction("take " + objReferent, ["take", obj])
                self.addAction("put " + objReferent, ["put", obj])

        # (1-arg) Connect X terminal A to Y terminal B
        for objReferent, objs in allObjects.items():
            for obj in objs:
                self.addAction("connect " + objReferent + " terminal A to", ["connect", obj, "terminal A"])
                self.addAction("connect " + objReferent + " terminal B to", ["connect", obj, "terminal B"])

        return self.possibleActions

    #
    #   Interpret actions
    #

    # # Perform the "examine" action.  Returns an observation string.
    # def actionExamine(self, obj):
    #     # Enforce that the object must be in the environment to do anything with it
    #     if (obj.parentContainer != self.rootObject):
    #         return "You don't currently have the " + obj.getReferents()[0] + " in your inventory."

    #     # Check if the object is an electrical object
    #     if (obj.getProperty("isElectrical") == True):
    #         # Try to pick up/take the electrical object
    #         obsStr, objRef, success = obj.parentContainer.takeObjectFromContainer(obj)
    #         if (success == False):
    #             # If it failed, we were unable to take the electrical object (e.g. it was in a closed container)
    #             return "You can't see that."

    #         # Update the game observation
    #         return "You examine the " + obj.name + "."
    #     else:
    #         return "You can't examine that."

    # Perform the "take" action.  Returns an observation string.
    def actionTake(self, obj):
        # Enforce that the object must be in the environment to do anything with it
        if (obj.parentContainer != self.rootObject):
            return "You don't currently have the " + obj.getReferents()[0] + " in your inventory."

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
            return "You take the " + obj.name + "."
        else:
            return "You can't take that."

    # Perform the "put" action.  Returns an observation string.
    def actionPut(self, obj):
        # Enforce that the object must be in the agent's inventory to do anything with it
        if (obj.parentContainer != self.agent):
            return "You don't currently have the " + obj.getReferents()[0] + " in your inventory."

        # Check if the object is moveable
        if (obj.getProperty("isMoveable") == True):
            # Try to put the object in the environment
            obsStr, objRef, success = self.rootObject.placeObjectInContainer(obj)
            if (success == False):
                # If it failed, we were unable to put the object (e.g. it was in a closed container)
                return "You can't see that."

            # Remove the object from the agent's inventory
            self.agent.removeObject(obj)
            # Update the game observation
            return "You put the " + obj.name + "."
        else:
            return "You can't put that."

    # Perform the "connect" action.  Returns an observation string.
    def actionConnect(self, obj, terminal):
        # Enforce that the object must be in the environment to do anything with it
        if (obj.parentContainer != self.rootObject):
            return "You don't currently have the " + obj.getReferents()[0] + " in your inventory."

        # Check if the object is an electrical object
        if (obj.getProperty("isElectrical") == True):
            # Try to connect the object to the terminal
            if (terminal == "terminal A"):
                obj.properties["connects"] = "terminal A"
            elif (terminal == "terminal B"):
                obj.properties["connects"] = "terminal B"
            else:
                return "You can't connect that."

            # Update the game observation
            return "You connect the " + obj.name + " to " + terminal + "."
        else:
            return "You can't connect that."

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
        # elif (actionVerb == "examine"):
        #     # Examine an electrical object
        #     thingToExamine = action[1]
        #     self.observationStr = self.actionExamine(thingToExamine)
        elif (actionVerb == "take"):
            # Take an object
            thingToTake = action[1]
            self.observationStr = self.actionTake(thingToTake)
        elif (actionVerb == "put"):
            # Put an object
            thingToPut = action[1]
            self.observationStr = self.actionPut(thingToPut)
        elif (actionVerb == "connect"):
            # Connect an electrical object to a terminal
            thingToConnect = action[1]
            terminal = action[2]
            self.observationStr = self.actionConnect(thingToConnect, terminal)

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
            # If there is a lit LED, the player wins.
            if (obj.name == "LED" and obj.getProperty("isOn") == True):
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
