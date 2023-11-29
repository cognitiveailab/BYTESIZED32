# grill-food.py
# based on balance-scale-heaviest.py
# ruoyao wang (feb 13/2023)

# Task: Create a micro-simulation that models how to grill food.
# Environment: backyard
# Task-critical Objects: Grill, Food, Salt, Oil
# High-level object classes: Device (Grill), Container (Grill, Food) 
# Critical properties: is_grilled (Food)
# Actions: look, inventory, examine, take/put object, turn on/off device, add salt/oil to food, grill food, eat food
# Distractor Items: Food
# Distractor Actions: None
# High-level solution procedure: take food, add salt/oil to food based on task description, turn on grill, put food on grill, wait till food is cooked, eat food

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


# A grill
class Grill(GameObject):
    def __init__(self, name):
        GameObject.__init__(self, name)
        self.properties["isMoveable"] = False
        self.properties["isOn"] = False

    def makeDescriptionStr(self, makeDetailed=False):
        if self.getProperty("isOn"):
            return "a " + self.name + " that is on."
        else:
            return "a " + self.name + " that is off."

    # Turn the grill on
    # Returns an observation string, and a success flag (boolean)
    def turnOn(self):
        # First, check to see if the grill is already on
        if self.getProperty("isOn"):
            # If so, then it can't be turned on
            return ("The " + self.name + " is already on.", False)

        # If the grill is off, then turn it on
        self.properties["isOn"] = True
        return ("The " + self.name + " is now on.", True)

    # Turn the grill off
    # Returns an observation string, and a success flag (boolean)
    def turnOff(self):
        # First, check to see if the grill is already off
        if not self.getProperty("isOn"):
            # If so, then it can't be turned off
            return ("The " + self.name + " is already off.", False)

        # If the grill is on, then turn it off
        self.properties["isOn"] = False
        return ("The " + self.name + " is now off.", True)


# Food for testing grilling
class Food(GameObject):
    def __init__(self, name):
        GameObject.__init__(self, name)
        self.properties["isGrilled"] = False

    def makeDescriptionStr(self, makeDetailed=False):
        if self.getProperty("isGrilled"):
            return "a " + self.name + " that is grilled."
        else:
            return "a " + self.name + " that is not grilled."

    # Grill the food
    # Returns an observation string, and a success flag (boolean)
    def grill(self):
        # First, check to see if the food is already grilled
        if self.getProperty("isGrilled"):
            # If so, then it can't be grilled
            return ("The " + self.name + " is already grilled.", False)

        # If the food is not grilled, then grill it
        self.properties["isGrilled"] = True
        return ("The " + self.name + " is now grilled.", True)

# Salt for testing adding salt to food
class Salt(GameObject):
    def __init__(self, name):
        GameObject.__init__(self, name)
        self.properties["isMoveable"] = False

    def makeDescriptionStr(self, makeDetailed=False):
        return "a " + self.name

# Oil for testing adding oil to food
class Oil(GameObject):
    def __init__(self, name):
        GameObject.__init__(self, name)
        self.properties["isMoveable"] = False

    def makeDescriptionStr(self, makeDetailed=False):
        return "a " + self.name

# The world is the root object of the game object tree.  In single room environments, it's where all the objects are located.
class World(Container):
    def __init__(self):
        Container.__init__(self, "backyard")

    def makeDescriptionStr(self, makeDetailed=False):
        outStr = "You find yourself in a backyard.  In the backyard, you see: \n"
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
        # Max mass we can weigh
        self.max_mass = 19
        # Initialize the variable to save the player's answer
        self.answer_mass = None
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

        # Add a grill
        grill = Grill("grill")
        world.addObject(grill)

        # Add food
        food = Food("food")
        world.addObject(food)

        # Add salt
        salt = Salt("salt")
        world.addObject(salt)

        # Add oil
        oil = Oil("oil")
        world.addObject(oil)

        # Return the world
        return world

    # Get the task description for this game
    def getTaskDescription(self):
        return "Your task is to grill the food. Use the grill action to grill the food."

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
                self.addAction("take " + objReferent + " from " + obj.parent.getReferents()[0], ["take", obj])

        # (1-arg) Examine
        for objReferent, objs in allObjects.items():
            for obj in objs:
                self.addAction("examine " + objReferent, ["examine", obj])
                self.addAction("examine " + objReferent + " in " + obj.parent.getReferents()[0], ["examine", obj])

        # (1-arg) Turn on device
        for objReferent, objs in allObjects.items():
            for obj in objs:
                if obj.getProperty("isOn"):
                    self.addAction("turn on " + objReferent, ["turn on", obj])
                    self.addAction("turn on " + objReferent + " in " + obj.parent.getReferents()[0], ["turn on", obj])

        # (1-arg) Turn off device
        for objReferent, objs in allObjects.items():
            for obj in objs:
                if not obj.getProperty("isOn"):
                    self.addAction("turn off " + objReferent, ["turn off", obj])
                    self.addAction("turn off " + objReferent + " in " + obj.parent.getReferents()[0], ["turn off", obj])

        # (1-arg) Add salt to food
        for objReferent, objs in allObjects.items():
            for obj in objs:
                if obj.getProperty("isGrilled"):
                    self.addAction("add salt to " + objReferent, ["add salt to", obj])
                    self.addAction("add salt to " + objReferent + " in " + obj.parent.getReferents()[0], ["add salt to", obj])

        # (1-arg) Add oil to food
        for objReferent, objs in allObjects.items():
            for obj in objs:
                if obj.getProperty("isGrilled"):
                    self.addAction("add oil to " + objReferent, ["add oil to", obj])
                    self.addAction("add oil to " + objReferent + " in " + obj.parent.getReferents()[0], ["add oil to", obj])

        # (1-arg) Grill food
        for objReferent, objs in allObjects.items():
            for obj in objs:
                if not obj.getProperty("isGrilled"):
                    self.addAction("grill " + objReferent, ["grill", obj])
                    self.addAction("grill " + objReferent + " in " + obj.parent.getReferents()[0], ["grill", obj])

        # (1-arg) Eat food
        for objReferent, objs in allObjects.items():
            for obj in objs:
                if obj.getProperty("isGrilled"):
                    self.addAction("eat " + objReferent, ["eat", obj])
                    self.addAction("eat " + objReferent + " in " + obj.parent.getReferents()[0], ["eat", obj])

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

        # (2-arg) Add to
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2):
                            containerPrefix = "in"
                            if obj2.properties["isContainer"]:
                                containerPrefix = obj2.properties["containerPrefix"]
                            self.addAction("add " + objReferent1 + " to " + objReferent2, ["add", obj1, obj2])

        return self.possibleActions

    #
    #   Interpret actions
    #

    # Take an object from a container
    def actionTake(self, obj):
        # If the object doesn't have a parent container, then it's dangling and something has gone wrong
        if (obj.parent == None):
            return "Something has gone wrong -- that object is dangling in the void.  You can't take that."

        # Take the object from the parent container, and put it in the inventory
        obsStr, objRef, success = obj.parent.takeObjectFromContainer(obj)
        if (success == False):
            return obsStr

        # Add the object to the inventory
        self.agent.addObject(obj)
        return obsStr + " You put the " + obj.getReferents()[0] + " in your inventory."

    # Examine an object
    def actionExamine(self, obj):
        return obj.makeDescriptionStr()

    # Turn on a device
    def actionTurnOn(self, obj):
        # Check that the object is a device
        if (obj.getProperty("isOn") == True):
            return "The " + obj.name + " is already on."

        # Turn the device on
        obsStr, success = obj.turnOn()
        if (success == False):
            return obsStr

        return obsStr + " You turn on the " + obj.name + "."

    # Turn off a device
    def actionTurnOff(self, obj):
        # Check that the object is a device
        if (obj.getProperty("isOn") == False):
            return "The " + obj.name + " is already off."

        # Turn the device off
        obsStr, success = obj.turnOff()
        if (success == False):
            return obsStr

        return obsStr + " You turn off the " + obj.name + "."

    # Add salt to food
    def actionAddSalt(self, obj):
        # Check that the object is food
        if (obj.getProperty("isGrilled") == True):
            return "The " + obj.name + " is already grilled."

        # Add salt to the food
        obsStr, success = obj.addSalt()
        if (success == False):
            return obsStr

        return obsStr + " You add salt to the " + obj.name + "."

    # Add oil to food
    def actionAddOil(self, obj):
        # Check that the object is food
        if (obj.getProperty("isGrilled") == True):
            return "The " + obj.name + " is already grilled."

        # Add oil to the food
        obsStr, success = obj.addOil()
        if (success == False):
            return obsStr

        return obsStr + " You add oil to the " + obj.name + "."

    # Grill food
    def actionGrill(self, obj):
        # Check that the object is food
        if (obj.getProperty("isGrilled") == True):
            return "The " + obj.name + " is already grilled."

        # Grill the food
        obsStr, success = obj.grill()
        if (success == False):
            return obsStr

        return obsStr + " You grill the " + obj.name + "."

    # Eat food
    def actionEat(self, obj):
        # Check that the object is food
        if (obj.getProperty("isGrilled") == False):
            return "The " + obj.name + " is not grilled."

        # Eat the food
        obsStr, success = obj.eat()
        if (success == False):
            return obsStr

        return obsStr + " You eat the " + obj.name + "."

    # Put an object in a container
    def actionPut(self, objToMove, newContainer):
        # Check that the destination container is a container
        if (newContainer.getProperty("isContainer") == False):
            return "You can't put things in the " + newContainer.getReferents()[0] + "."

        # Enforce that the object must be in the inventory to do anything with it
        if (objToMove.parent != self.agent):
            return "You don't currently have the " + objToMove.getReferents()[0] + " in your inventory."

        # Take the object from it's current container, and put it in the new container.
        # Deep copy the reference to the original parent container, because the object's parent container will be changed when it's taken from the original container
        originalContainer = objToMove.parent
        obsStr1, objRef, success = objToMove.parent.takeObjectFromContainer(objToMove)
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

    # Add an object to another object
    def actionAdd(self, objToMove, newContainer):
        # Check that the destination container is a container
        if (newContainer.getProperty("isContainer") == False):
            return "You can't add things to the " + newContainer.getReferents()[0] + "."

        # Enforce that the object must be in the inventory to do anything with it
        if (objToMove.parent != self.agent):
            return "You don't currently have the " + objToMove.getReferents()[0] + " in your inventory."

        # Take the object from it's current container, and put it in the new container.
        # Deep copy the reference to the original parent container, because the object's parent container will be changed when it's taken from the original container
        originalContainer = objToMove.parent
        obsStr1, objRef, success = objToMove.parent.takeObjectFromContainer(objToMove)
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

        elif (actionVerb == "take"):
            # Take an object from a container
            thingToTake = action[1]
            self.observationStr = self.actionTake(thingToTake)
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
        elif (actionVerb == "add salt to"):
            # Add salt to food
            foodToAddSalt = action[1]
            self.observationStr = self.actionAddSalt(foodToAddSalt)
        elif (actionVerb == "add oil to"):
            # Add oil to food
            foodToAddOil = action[1]
            self.observationStr = self.actionAddOil(foodToAddOil)
        elif (actionVerb == "grill"):
            # Grill food
            foodToGrill = action[1]
            self.observationStr = self.actionGrill(foodToGrill)
        elif (actionVerb == "eat"):
            # Eat food
            foodToEat = action[1]
            self.observationStr = self.actionEat(foodToEat)

        elif (actionVerb == "put"):
            # Put an object in a container
            thingToMove = action[1]
            newContainer = action[2]
            self.observationStr = self.actionPut(thingToMove, newContainer)
        elif (actionVerb == "add"):
            # Add an object to another object
            thingToMove = action[1]
            newContainer = action[2]
            self.observationStr = self.actionAdd(thingToMove, newContainer)
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

        if self.answer_mass is not None:
            if self.cube_weight == self.answer_mass:
                self.score += 1
                self.gameOver = True
                self.gameWon = True
            else:
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