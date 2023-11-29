# box_screwdriver.py
# based on bird-life-cycle.py
# ruoyao wang (feb 8/2023)

# Task: Create a micro-simulation that models how to open a box whose cover is fixed by screws with a screwdriver.
# Environment: room
# Task-critical Objects: Screw, Screwdriver, Box, Coin
# High-level object classes: Container (Box)
# Critical properties: is_open (Box), is_openable (Box)
# Actions: look, inventory, examine, take/put object, screw/unscrew screw with screwdriver, open/close container
# Distractor Items: Hammer
# Distractor Actions: None
# High-level solution procedure: take screwdriver, unscrew all screws, open box, take coin, put coin in answer box

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


# A box, has a screw and a coin
class Box(Container):
    def __init__(self, name):
        GameObject.__init__(self, name)
        Container.__init__(self, name)
        self.properties["isOpenable"] = True
        self.properties["isOpen"] = False
        self.properties["is_open"] = False
        self.properties["is_openable"] = True

    def makeDescriptionStr(self, makeDetailed=False):
        if self.properties["is_open"]:
            return f"{self.name} is open. It contains {self.contains[0].makeDescriptionStr()}."
        else:
            return f"{self.name} is closed. It contains {self.contains[0].makeDescriptionStr()}."

# A screw
class Screw(GameObject):
    def __init__(self, name):
        GameObject.__init__(self, name)
        self.properties["is_unscrewed"] = False

    def makeDescriptionStr(self, makeDetailed=False):
        if self.properties["is_unscrewed"]:
            return f"{self.name} is unscrewed."
        else:
            return f"{self.name} is screwed."

# A screwdriver
class Screwdriver(GameObject):
    def __init__(self, name):
        GameObject.__init__(self, name)
        self.properties["is_unscrewed"] = False

    def makeDescriptionStr(self, makeDetailed=False):
        if self.properties["is_unscrewed"]:
            return f"{self.name} is unscrewed."
        else:
            return f"{self.name} is screwed."

# A coin
class Coin(GameObject):
    def __init__(self, name):
        GameObject.__init__(self, name)

    def makeDescriptionStr(self, makeDetailed=False):
        return f"{self.name}."

# The room is the root object of the game object tree.  In single room environments, it's where all the objects are located.
class Room(Container):
    def __init__(self):
        Container.__init__(self, "room")

    def makeDescriptionStr(self, makeDetailed=False):
        outStr = "You are in a room. "
        for obj in self.contains:
            outStr += "\t" + obj.makeDescriptionStr() + "\n"

        return outStr


class TextGame:

    def __init__(self, randomSeed):
        # Random number generator, initialized with a seed passed as an argument
        self.random = random.Random(randomSeed)

        # Game Object Tree
        self.rootObject = self.initializeRoom()
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
    def initializeRoom(self):
        room = Room()

        # Generate a box, a screw, a screwdriver, and a coin
        box = Box("box")
        screw = Screw("screw")
        screwdriver = Screwdriver("screwdriver")
        coin = Coin("coin")

        # Add the screw and the coin to the box
        box.addObject(screw)
        box.addObject(coin)

        # Add the box and the screwdriver to the room
        room.addObject(box)
        room.addObject(screwdriver)

        # Return the room
        return room

    # Get the task description for this game
    def getTaskDescription(self):
        return f"Your task is to open the box with the screwdriver."

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

        # Actions with one object argument
        # (1-arg) Inventory
        for objReferent, objs in allObjects.items():
            for obj in objs:
                self.addAction("inventory " + objReferent, ["inventory", obj])

        # (1-arg) Examine
        for objReferent, objs in allObjects.items():
            for obj in objs:
                self.addAction("examine " + objReferent, ["examine", obj])

        # (1-arg) Take
        for objReferent, objs in allObjects.items():
            for obj in objs:
                self.addAction("take " + objReferent, ["take", obj])

        # (1-arg) Put
        for objReferent, objs in allObjects.items():
            for obj in objs:
                self.addAction("put " + objReferent, ["put", obj])

        # Actions with two object arguments
        # (2-arg) Screw/unscrew screw with screwdriver
        for objReferent1, objs1 in allObjects.items():
            for obj1 in objs1:
                for objReferent2, objs2 in allObjects.items():
                    for obj2 in objs2:
                        self.addAction("screw " + objReferent1 + " with " + objReferent2, ["screw", obj1, obj2])
                        self.addAction("unscrew " + objReferent1 + " with " + objReferent2, ["unscrew", obj1, obj2])

        # (2-arg) Open/close container
        for objReferent1, objs1 in allObjects.items():
            for obj1 in objs1:
                for objReferent2, objs2 in allObjects.items():
                    for obj2 in objs2:
                        self.addAction("open " + objReferent1 + " with " + objReferent2, ["open", obj1, obj2])
                        self.addAction("close " + objReferent1 + " with " + objReferent2, ["close", obj1, obj2])

        return self.possibleActions

    #
    #   Interpret actions
    #


    # Screw/unscrew a screw with a screwdriver
    def actionScrew(self, screw, screwdriver):
        # check if the screwdriver is valid
        if screwdriver.name != "screwdriver":
            return "You need a screwdriver to screw/unscrew the screw."
        else:
            # check if the screw is valid
            if screw.name != "screw":
                return "You need a screw to screw/unscrew."
            else:
                # check if the screw is already unscrewed
                if screw.properties["is_unscrewed"]:
                    return "The screw is already unscrewed."
                else:
                    # unscrew the screw
                    screw.properties["is_unscrewed"] = True
                    return f"You screw the {screw.name} with the {screwdriver.name}."

    # Open/close a container
    def actionOpen(self, container, screwdriver):
        # check if the screwdriver is valid
        if screwdriver.name != "screwdriver":
            return "You need a screwdriver to open/close the container."
        else:
            # check if the container is valid
            if container.name != "box":
                return "You need a box to open/close."
            else:
                # check if the container is already open
                if container.properties["is_open"]:
                    return "The box is already open."
                else:
                    # check if all screws are unscrewed
                    if not all(screw.properties["is_unscrewed"] for screw in container.contains):
                        return "All screws need to be unscrewed before opening the box."
                    else:
                        # open the container
                        container.properties["is_open"] = True
                        return f"You open the {container.name} with the {screwdriver.name}."

    # Take an object
    def actionTake(self, obj):
        # check if the object is valid
        if obj.name != "screwdriver" and obj.name != "coin":
            return "You can't take that."
        else:
            # check if the object is already taken
            if obj.parentContainer == None:
                return "The " + obj.name + " is already taken."
            else:
                # take the object
                obj.removeSelfFromContainer()
                return f"You take the {obj.name}."

    # Put an object
    def actionPut(self, obj, container):
        # check if the object is valid
        if obj.name != "screwdriver" and obj.name != "coin":
            return "You can't put that."
        else:
            # check if the container is valid
            if container.name != "box":
                return "You can't put the " + obj.name + " in that."
            else:
                # check if the object is already in the container
                if obj.parentContainer == container:
                    return "The " + obj.name + " is already in the " + container.name + "."
                else:
                    # put the object in the container
                    container.addObject(obj)
                    return f"You put the {obj.name} in the {container.name}."


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
            # Look around the environment -- i.e. show the description of the room.
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif (actionVerb == "inventory"):
            obj = action[1]
            self.observationStr = obj.makeDescriptionStr()
        elif (actionVerb == "examine"):
            obj = action[1]
            self.observationStr = obj.makeDescriptionStr()
        elif (actionVerb == "take"):
            obj = action[1]
            self.observationStr = self.actionTake(obj)
        elif (actionVerb == "put"):
            obj = action[1]
            container = action[2]
            self.observationStr = self.actionPut(obj, container)
        elif (actionVerb == "screw"):
            screw = action[1]
            screwdriver = action[2]
            self.observationStr = self.actionScrew(screw, screwdriver)
        elif (actionVerb == "open"):
            container = action[1]
            screwdriver = action[2]
            self.observationStr = self.actionOpen(container, screwdriver)


        # Catch-all
        else:
            self.observationStr = "ERROR: Unknown action."

        # Do one tick of the environment
        self.doRoomTick()

        # Calculate the score
        lastScore = self.score
        self.calculateScore()
        reward = self.score - lastScore

        return (self.observationStr, self.score, reward, self.gameOver, self.gameWon)


    # Call the object update for each object in the environment
    def doRoomTick(self):
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



        allObjects = self.rootObject.contains
        box = None
        screwdriver = None
        coin = None
        for obj in allObjects:
            if obj.name == "box":
                box = obj
            elif obj.name == "screwdriver":
                screwdriver = obj
            elif obj.name == "coin":
                coin = obj

        if box.properties["is_open"] and coin.parentContainer == box:
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
