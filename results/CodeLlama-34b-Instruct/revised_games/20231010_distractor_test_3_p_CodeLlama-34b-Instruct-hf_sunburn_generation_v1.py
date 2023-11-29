# grill_food.py
# based on boil-water.py
# ruoyao wang (feb 13/2023)

# Task Description: Create a micro-simulation that models how to grill food.
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

# A device that can be turned on or off
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
        return "a " + self.name

# The agent (just a placeholder for a container for the inventory)
class Agent(Container):
    def __init__(self):
        Container.__init__(self, "agent")

    # Get a list of referents (i.e. names that this object can be called by)
    def getReferents(self):
        return ["yourself"]

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "yourself"

# The world is the root object of the game object tree.
class World(Container):
    def __init__(self):
        Container.__init__(self, "world")

    # Describe the a room
    def makeDescriptionStr(self, room, makeDetailed=False):
        outStr = f"You find yourself in a {room.name}.  In the {room.name}, you see: \n"
        for obj in room.contains:
            outStr += "\t" + obj.makeDescriptionStr() + "\n"
        # describe room connection information
        outStr += "You also see:\n"
        for connected_room in room.connects:
            outStr += f"\t a way to the {connected_room.name}\n"

        return outStr

# The grill
class Grill(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isGrill"] = True

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "a " + self.name

# The food
class Food(GameObject):
    def __init__(self, name):
        GameObject.__init__(self, name)
        self.properties["isFood"] = True
        self.properties["isGrilled"] = False

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "a " + self.name

# The salt
class Salt(GameObject):
    def __init__(self, name):
        GameObject.__init__(self, name)
        self.properties["isSalt"] = True

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "a " + self.name

# The oil
class Oil(GameObject):
    def __init__(self, name):
        GameObject.__init__(self, name)
        self.properties["isOil"] = True

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "a " + self.name

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
        self.observationStr = self.rootObject.makeDescriptionStr(self.agent.parentContainer)
        # Do calculate initial scoring
        self.calculateScore()

    # Create/initialize the world/environment for this game
    def initializeWorld(self):
        world = World()

        # Add two "rooms": a backyard and a kitchen
        backyard = Room("backyard")
        kitchen = Room("kitchen")
        world.addObject(backyard)
        world.addObject(kitchen)
        # Connects two rooms
        backyard.connects.append(kitchen)
        kitchen.connects.append(backyard)

        # Add objects into the backyard
        # Add the agent
        backyard.addObject(self.agent)
        # Add the grill
        grill = Grill("grill")
        backyard.addObject(grill)
        # Add some food
        steak = Food("steak")
        backyard.addObject(steak)
        # Add some salt
        salt = Salt("salt")
        backyard.addObject(salt)
        # Add some oil
        oil = Oil("oil")
        backyard.addObject(oil)

        # Add objects to the kitchen
        # Add a plate
        plate = Container("plate")
        kitchen.addObject(plate)

        # Return the world
        return world

    # Get the task description for this game
    def getTaskDescription(self):
        return "Your task is to grill the steak.  You must add salt and oil to the steak before grilling it.  You must also put the cooked steak on the plate."

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

        # (1-arg) Use
        for objReferent, objs in allObjects.items():
                for obj in objs:
                    self.addAction("use " + objReferent, ["use", obj])

        # (1-arg) Move
        for objReferent, objs in allObjects.items():
            for obj in objs:
                self.addAction("move to " + objReferent, ["move", obj])

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


    ## Use items to the agent
    def actionUse(self, obj):
        # Check if the object is a device
        if obj.getProperty("isDevice"):
            # If the object is a device, then try to turn it on or off
            if obj.getProperty("isOn"):
                return self.actionTurnOff(obj)
            else:
                return self.actionTurnOn(obj)
        # Check if the object is food
        elif obj.getProperty("isFood"):
            # If the object is food, then try to grill it
            return self.actionGrill(obj)
        # Check if the object is salt
        elif obj.getProperty("isSalt"):
            # If the object is salt, then try to add it to the food
            return self.actionAddSalt(obj)
        # Check if the object is oil
        elif obj.getProperty("isOil"):
            # If the object is oil, then try to add it to the food
            return self.actionAddOil(obj)
        # Catch-all
        else:
            return "You can't use that."

    def actionMove(self, room):
        # Check if the target is a room
        if type(room) != Room:
            return f"Cannot move to the {room.name}"
        # Check if two rooms are connected
        elif not self.agent.parentContainer.connectsTo(room):
            return f"There is no way from {self.agent.parentContainer.name} to {room.name}."
        else:
            current_location = self.agent.parentContainer.name
            self.agent.removeSelfFromContainer()
            room.addObject(self.agent)
            return f"You move from {current_location} to {room.name}."

    # Turn on a device
    def actionTurnOn(self, device):
        # Check if the object is a device
        if device.getProperty("isDevice"):
            # If the object is a device, then try to turn it on
            obsStr, success = device.turnOn()
            if (success == False):
                return obsStr
            else:
                return obsStr + " You turn on the " + device.getReferents()[0] + "."
        else:
            return "You can't turn on that."

    # Turn off a device
    def actionTurnOff(self, device):
        # Check if the object is a device
        if device.getProperty("isDevice"):
            # If the object is a device, then try to turn it off
            obsStr, success = device.turnOff()
            if (success == False):
                return obsStr
            else:
                return obsStr + " You turn off the " + device.getReferents()[0] + "."
        else:
            return "You can't turn off that."

    # Grill food
    def actionGrill(self, food):
        # Check if the object is food
        if food.getProperty("isFood"):
            # If the object is food, then try to grill it
            if food.getProperty("isGrilled"):
                return "The " + food.getReferents()[0] + " is already grilled."
            else:
                # Check if the grill is on
                if self.rootObject.containsItemWithName("grill").getProperty("isOn"):
                    # If the grill is on, then grill the food
                    food.properties["isGrilled"] = True
                    return "You grill the " + food.getReferents()[0] + "."
                else:
                    return "The grill is not on.  You can't grill the " + food.getReferents()[0] + "."
        else:
            return "You can't grill that."

    # Add salt to food
    def actionAddSalt(self, salt):
        # Check if the object is salt
        if salt.getProperty("isSalt"):
            # If the object is salt, then try to add it to the food
            if self.agent.containsItemWithName("food"):
                # If the agent has food, then add the salt to the food
                food = self.agent.containsItemWithName("food")
                food.addObject(salt)
                return "You add the " + salt.getReferents()[0] + " to the " + food.getReferents()[0] + "."
            else:
                return "You don't have any food to add the " + salt.getReferents()[0] + " to."
        else:
            return "You can't add the " + salt.getReferents()[0] + " to the food."

    # Add oil to food
    def actionAddOil(self, oil):
        # Check if the object is oil
        if oil.getProperty("isOil"):
            # If the object is oil, then try to add it to the food
            if self.agent.containsItemWithName("food"):
                # If the agent has food, then add the oil to the food
                food = self.agent.containsItemWithName("food")
                food.addObject(oil)
                return "You add the " + oil.getReferents()[0] + " to the " + food.getReferents()[0] + "."
            else:
                return "You don't have any food to add the " + oil.getReferents()[0] + " to."
        else:
            return "You can't add the " + oil.getReferents()[0] + " to the food."

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
        elif (actionVerb == "use"):
            # Use an item on the agent
            item = action[1]
            self.observationStr = self.actionUse(item)
        elif (actionVerb == "move"):
            # move to a new location
            target_location = action[1]
            self.observationStr = self.actionMove(target_location)
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

        # Lose if the agent gets sunburn
        if self.agent.properties["sunburn"]:
            self.score = 0
            self.gameOver = True
            self.gameWon = False
        else:
            # If there is any steam in the environment, then add a point.
            allObjects = self.rootObject.getAllContainedObjectsRecursive()
            for obj in allObjects:
                if (obj.name == "plate"):
                    for plate_obj in obj.contains:
                        if plate_obj.name == 'steak':
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
