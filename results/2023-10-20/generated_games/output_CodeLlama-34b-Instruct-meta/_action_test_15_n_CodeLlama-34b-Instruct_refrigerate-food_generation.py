# keep_warm.py
# based on refridgerate-food.py
### peter jansen (feb 15/2023)

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
        # First, check to see if this object is a container
        if not (self.getProperty("isContainer") == True):
            # If not, then it can't be placed in a container
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
        # First, check to see if this object is a container
        if not (self.getProperty("isContainer") == True):
            # If not, then it can't be placed in a container
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
            return ("The " + self.name + " can't be placed in a container.", False)

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
            return ("The " + self.name + " can't be removed from a container.", None, False)

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
#   Specific Game Objects
#

# A room, which is a type of container that can be used to put things on
class Room(Container):
    # Constructor.
    def __init__(self):
        GameObject.__init__(self, "room")
        Container.__init__(self, "room")

    def makeDescriptionStr(self, makeDetailed=False):
        outStr = "You find yourself in a room.  In the room, you see: \n"
        for obj in self.contains:
            outStr += "\t" + obj.makeDescriptionStr() + "\n"

        return outStr


# A clothes, which is a type of object that can be worn to keep warm
class Clothes(GameObject):
    def __init__(self, clothesPrefix, clothesName, cold_resistance=10):
        GameObject.__init__(self, clothesName)
        self.properties["clothesPrefix"] = clothesPrefix  # The prefix to use when referring to the clothes item (e.g. "a", "some", "the", etc.)

        self.properties["isClothes"] = True
        self.properties["cold_resistance"] = cold_resistance    # How much the clothes item can resist cold (in degrees Celsius)

    # Get a list of referents (i.e. names that this object can be called by)
    def getReferents(self):
        referents = []
        # Add the clothes item's potentially spoiled property as a prefix
        referents.append(self.name)
        return referents

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        outStr = self.properties["clothesPrefix"] + " "
        outStr += self.name

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
        world = Room()

        # Add the agent
        world.addObject(self.agent)

        # Create clothes
        possibleClothes = []
        possibleClothes.append(Clothes("a", "coat", cold_resistance=10))
        possibleClothes.append(Clothes("a", "down coat", cold_resistance=20))
        possibleClothes.append(Clothes("a", "hat", cold_resistance=5))
        possibleClothes.append(Clothes("a", "gloves", cold_resistance=10))
        possibleClothes.append(Clothes("a", "scarf", cold_resistance=15))

        # Randomly shuffle the clothes
        self.random.shuffle(possibleClothes)

        # Add a few random clothes
        numClothes = self.random.randint(1, 3)
        for i in range(numClothes):
            # Choose the next clothes
            clothes = possibleClothes[i % len(possibleClothes)]
            # Add the clothes to the room
            world.addObject(clothes)

        # Store the number of clothes that need to be put on, for scoring
        self.numClothesToPutOn = numClothes

        # Return the world
        return world

    # Get the task description for this game
    def getTaskDescription(self):
        return "Your task is to keep warm and navigate to another house."

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
        # (1-arg) Take
        for objReferent, objs in allObjects.items():
            for obj in objs:
                self.addAction("take " + objReferent, ["take", obj])
                self.addAction("take " + objReferent + " from " + obj.parentContainer.getReferents()[0], ["take", obj])

        # (1-arg) Put on clothes
        for objReferent, objs in allObjects.items():
            for obj in objs:
                self.addAction("put on " + objReferent, ["put on", obj])

        # (1-arg) Move
        for objReferent, objs in allObjects.items():
            for obj in objs:
                self.addAction("move " + objReferent, ["move", obj])

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

    # Perform the "take" action.  Returns an observation string.
    def actionTake(self, obj):
        # Enforce that the object must be in the inventory to do anything with it
        if (obj.parentContainer != self.agent):
            return "You don't currently have the " + obj.getReferents()[0] + " in your inventory."

        # Take the object from it's current container, and put it in the inventory
        obsStr1, objRef, success = obj.parentContainer.takeObjectFromContainer(obj)
        if (success == False):
            return obsStr1

        # Add the object to the inventory
        self.agent.addObject(obj)
        return obsStr1 + " You put the " + obj.getReferents()[0] + " in your inventory."

    # Perform the "put on" action.  Returns an observation string.
    def actionPutOn(self, obj):
        # Enforce that the object must be in the inventory to do anything with it
        if (obj.parentContainer != self.agent):
            return "You don't currently have the " + obj.getReferents()[0] + " in your inventory."

        # Check if the object is clothes
        if (obj.getProperty("isClothes") == True):
            # Try to put on the clothes
            obsStr = "You put on the " + obj.name + "."
            # Add the clothes to the agent
            self.agent.addObject(obj)
            return obsStr
        else:
            return "You can't put on that."

    # Perform the "move" action.  Returns an observation string.
    def actionMove(self, obj):
        # Enforce that the object must be in the inventory to do anything with it
        if (obj.parentContainer != self.agent):
            return "You don't currently have the " + obj.getReferents()[0] + " in your inventory."

        # Check if the object is a room
        if (obj.getProperty("isContainer") == True):
            # This is handled by the object itself
            obsStr, success = obj.openContainer()
            return obsStr
        else:
            return "You can't move that."


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

        elif (actionVerb == "take"):
            # Take an object from a container
            thingToTake = action[1]
            self.observationStr = self.actionTake(thingToTake)
        elif (actionVerb == "put on"):
            # Put an object in a container
            thingToPutOn = action[1]
            self.observationStr = self.actionPutOn(thingToPutOn)
        elif (actionVerb == "move"):
            # Move to a new room
            thingToMove = action[1]
            self.observationStr = self.actionMove(thingToMove)

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

        # Give a positive score for each clothes that's put on, and a negative score for each clothes that's missing (e.g. it's been eaten)
        # Also, give a negative score for each clothes that's not put on (e.g. it's in the inventory)
        numClothesFound = 0
        numClothesChanged = 0     # Clothes modified (e.g. put on or taken off)
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        for obj in allObjects:
            # Check if the object is a clothes (i.e. an instance of the Clothes class)
            if (isinstance(obj, Clothes)):
                # Check if the clothes is put on
                if (obj.parentContainer == self.agent):
                    self.score += 1
                    numClothesChanged += 1
                # Otherwise, check if the clothes is in the inventory
                elif (obj.parentContainer == self.agent):
                    self.score -= 1
                    numClothesChanged += 1

                numClothesFound += 1

        # Give a negative score for each clothes that's missing (e.g. it's been eaten)
        numClothesMissing = self.numClothesToPutOn - numClothesFound
        self.score -= numClothesMissing

        # Check if the game is over
        # Check for winning condition -- score is the same as the number of clothes to put on
        if (self.score == self.numClothesToPutOn):
            self.gameOver = True
            self.gameWon = True
        # Check for losing condition -- all clothes changed, one or more clothes are not put on
        elif ((numClothesChanged + numClothesMissing) >= self.numClothesToPutOn):
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
