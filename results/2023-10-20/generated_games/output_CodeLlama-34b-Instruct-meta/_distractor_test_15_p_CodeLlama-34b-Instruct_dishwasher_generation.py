# winter_day.py
# peter jansen (feb 2/2023)

# Task: Create a micro-simulation that models how to keep warm, go outside and navigate to another house in a cold winter day
# Environment: world
# Task-critical Objects: Room, Clothes
# High-level object classes: Container (Room)
# Critical properties: cold (Room), cold_resistance (Clothes), warmth (Agent)
# Actions: look, inventory, examine, take/put object, put on clothes, move
# Distractor Items: Clothes, Room
# Distractor Actions: None
# High-level solution procedure: take down coat, put on down coat, move outside, find a way to another house

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
        if self.properties["isOpen"]:
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

# A Room, which is a container that can be open or closed.  If it's closed, then it's cold inside.
class Room(Container):
    def __init__(self, name):
        GameObject.__init__(self, name)
        Container.__init__(self, name)

        # Set the properties of this object
        self.properties["isOpenable"] = True  # A room is openable
        self.properties["isOpen"] = False     # A room is closed by default
        self.properties["isMoveable"] = False # A room is too heavy to move (and doesn't really need to be moved for this simulation)

        self.properties["cold"] = True        # A room is cold by default
        self.properties["cold_resistance"] = 0 # A room has no cold resistance by default

    # Try to open the room.
    # Returns an observation string, and a success flag (boolean)
    def openRoom(self):
        # If the room is already open, then return an error
        if self.properties["isOpen"]:
            return ("The " + self.name + " is already open.", False)
        else:
            self.properties["isOpen"] = True
            return ("The " + self.name + " is now open.", True)

    # Try to close the room.
    # Returns an observation string, and a success flag (boolean)
    def closeRoom(self):
        # If the room is already closed, then return an error
        if not self.properties["isOpen"]:
            return ("The " + self.name + " is already closed.", False)
        else:
            self.properties["isOpen"] = False
            return ("The " + self.name + " is now closed.", True)

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        outStr = "a room"
        if self.properties["isOpen"]:
            outStr += " that is currently open"
        else:
            outStr += " that is currently closed"

        return outStr


# A Clothes, which is a container that can be worn or unworn.  If it's worn, then it provides warmth.
class Clothes(Container):
    def __init__(self, name):
        GameObject.__init__(self, name)
        Container.__init__(self, name)

        # Set the properties of this object
        self.properties["isOpenable"] = False  # Clothes are not openable
        self.properties["isOpen"] = False     # Clothes are not open by default
        self.properties["isMoveable"] = True  # Clothes are moveable

        self.properties["worn"] = False       # Clothes are not worn by default
        self.properties["cold_resistance"] = 0 # Clothes have no cold resistance by default

    # Try to wear the clothes.
    # Returns an observation string, and a success flag (boolean)
    def wearClothes(self):
        # If the clothes are already worn, then return an error
        if self.properties["worn"]:
            return ("The " + self.name + " is already worn.", False)
        else:
            self.properties["worn"] = True
            return ("The " + self.name + " is now worn.", True)

    # Try to unwear the clothes.
    # Returns an observation string, and a success flag (boolean)
    def unwearClothes(self):
        # If the clothes are already unworn, then return an error
        if not self.properties["worn"]:
            return ("The " + self.name + " is already unworn.", False)
        else:
            self.properties["worn"] = False
            return ("The " + self.name + " is now unworn.", True)

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        outStr = "a pair of " + self.name
        if self.properties["worn"]:
            outStr += " that is currently worn"
        else:
            outStr += " that is currently unworn"

        return outStr


# The world is the root object of the game object tree.  In single room environments, it's where all the objects are located.
class World(Container):
    def __init__(self):
        Container.__init__(self, "world")

    def makeDescriptionStr(self, makeDetailed=False):
        outStr = "You find yourself in a cold winter day.  In the world, you see: \n"
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
        # Generate possible actions
        self.generatePossibleActions()

    # Create/initialize the world/environment for this game
    def initializeWorld(self):
        world = World()

        # Add the agent
        world.addObject(self.agent)

        # Add a room
        room = Room("room")
        world.addObject(room)

        # Add some clothes
        clothesNames = ["coat", "down coat", "hat", "gloves", "scarf"]
        # Shuffle the clothes names
        self.random.shuffle(clothesNames)

        # Add some random number of clothes to the world (minimum 3, maximum 8)
        numClothes = self.random.randint(3, 5)
        for i in range(numClothes):
            # Choose the next clothes type
            clothesType = clothesNames[i % len(clothesNames)]
            # Create a new clothes of that type
            clothes = Clothes(clothesType)
            # Add the clothes to the environment
            world.addObject(clothes)

        # Return the world
        return world

    # Get the task description for this game
    def getTaskDescription(self):
        return "Your task is to keep warm, go outside and navigate to another house."

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

        # (1-arg) Wear
        for objReferent, objs in allObjects.items():
            for obj in objs:
                self.addAction("wear " + objReferent, ["wear", obj])

        # (1-arg) Unwear
        for objReferent, objs in allObjects.items():
            for obj in objs:
                self.addAction("unwear " + objReferent, ["unwear", obj])

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

        # (2-arg) Move
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2):
                            self.addAction("move " + objReferent1 + " to " + objReferent2, ["move", obj1, obj2])

        return self.possibleActions

    #
    #   Interpret actions
    #

    # Perform the "examine" action.  Returns an observation string.
    def actionExamine(self, obj):
        # Enforce that the object must be in the environment to do anything with it
        if (obj.parentContainer == None):
            return "You don't currently have the " + obj.getReferents()[0] + " in your environment."

        # Examine the object
        return obj.makeDescriptionStr(makeDetailed = True)

    # Perform the "take" action.  Returns an observation string.
    def actionTake(self, obj):
        # Enforce that the object must be in the environment to do anything with it
        if (obj.parentContainer == None):
            return "You don't currently have the " + obj.getReferents()[0] + " in your environment."

        # Take the object from it's current container, and put it in the inventory
        obsStr1, objRef, success = obj.parentContainer.takeObjectFromContainer(obj)
        if (success == False):
            return obsStr1

        # Add the object to the inventory
        self.agent.addObject(obj)
        return obsStr1 + " You put the " + obj.getReferents()[0] + " in your inventory."

    # Perform the "open" action.  Returns an observation string.
    def actionOpen(self, obj):
        # Check if the object is a container
        if (obj.getProperty("isContainer") == True):
            # This is handled by the object itself
            obsStr, success = obj.openContainer()
            return obsStr
        else:
            return "You can't open that."

    # Perform the "close" action.  Returns an observation string.
    def actionClose(self, obj):
        # Check if the object is a container
        if (obj.getProperty("isContainer") == True):
            # This is handled by the object itself
            obsStr, success = obj.closeContainer()
            return obsStr
        else:
            return "You can't close that."

    # Perform the "wear" action.  Returns an observation string.
    def actionWear(self, obj):
        # Check if the object is clothes
        if (obj.getProperty("isClothes") == True):
            # This is handled by the object itself
            obsStr, success = obj.wearClothes()
            return obsStr
        else:
            return "You can't wear that."

    # Perform the "unwear" action.  Returns an observation string.
    def actionUnwear(self, obj):
        # Check if the object is clothes
        if (obj.getProperty("isClothes") == True):
            # This is handled by the object itself
            obsStr, success = obj.unwearClothes()
            return obsStr
        else:
            return "You can't unwear that."

    # Perform the "put" action.  Returns an observation string.
    def actionPut(self, objToMove, newContainer):
        # Check that the destination container is a container
        if (newContainer.getProperty("isContainer") == False):
            return "You can't put things in the " + newContainer.getReferents()[0] + "."

        # Enforce that the object must be in the environment to do anything with it
        if (objToMove.parentContainer == None):
            return "You don't currently have the " + objToMove.getReferents()[0] + " in your environment."

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

    # Perform the "move" action.  Returns an observation string.
    def actionMove(self, objToMove, newContainer):
        # Check that the destination container is a container
        if (newContainer.getProperty("isContainer") == False):
            return "You can't move things to the " + newContainer.getReferents()[0] + "."

        # Enforce that the object must be in the environment to do anything with it
        if (objToMove.parentContainer == None):
            return "You don't currently have the " + objToMove.getReferents()[0] + " in your environment."

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
            self.observationStr = self.actionExamine(thingToExamine)
        elif (actionVerb == "take"):
            # Take an object from a container
            thingToTake = action[1]
            self.observationStr = self.actionTake(thingToTake)
        elif (actionVerb == "open"):
            # Open a container
            thingToOpen = action[1]
            self.observationStr = self.actionOpen(thingToOpen)
        elif (actionVerb == "close"):
            # Close a container
            thingToClose = action[1]
            self.observationStr = self.actionClose(thingToClose)
        elif (actionVerb == "wear"):
            # Wear clothes
            thingToWear = action[1]
            self.observationStr = self.actionWear(thingToWear)
        elif (actionVerb == "unwear"):
            # Unwear clothes
            thingToUnwear = action[1]
            self.observationStr = self.actionUnwear(thingToUnwear)

        elif (actionVerb == "put"):
            # Put an object in a container
            thingToMove = action[1]
            newContainer = action[2]
            self.observationStr = self.actionPut(thingToMove, newContainer)
        elif (actionVerb == "move"):
            # Move an object to a new location
            thingToMove = action[1]
            newContainer = action[2]
            self.observationStr = self.actionMove(thingToMove, newContainer)


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
        # Baseline score is negative one point per starting cold room
        self.score = 1

        # Subtract one point for every cold room in the environment
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        numColdRooms = 0
        for obj in allObjects:
            if (obj.name == "room"):
                if (obj.getProperty("cold") == True):
                    self.score -= 1
                    numColdRooms += 1

        # Add one point for every warm object in the environment
        numWarmObjects = 0
        for obj in allObjects:
            if (obj.getProperty("worn") == True):
                self.score += 1
                numWarmObjects += 1

        # Check if the game is complete
        if (numColdRooms == 0):
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
    while not game.gameOver:

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
