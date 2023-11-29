# keys_and_doors.py
# based on find_keys.py
# ruoyao wang (apr 26/2023)

# Task: Create a micro-simulation that models how to find keys, use keys to open doors to go to another room and collect a coin
# Environment: house
# Task-critical Objects: Room, Door, Key, Drawer, Coin
# High-level object classes: Container (Room, Drawer)
# Critical properties: connects (Room), is_locked (Door), is_open (Door), key (Door)
# Actions: look, inventory, examine, take/put object, open/close container, open/close door, unlock door with key, move to room
# Distractor Items: Key, Room, Door
# Distractor Actions: None
# High-level solution procedure: find the keys and open corresponding doors, move to the coin room and take coin.

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
        return f"the {self.name}"

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

# A room
class Room(Container):
    def __init__(self, name):
        Container.__init__(self, name)
        self.properties["isMoveable"] = False
        self.properties["connects"] = [] # list of rooms that this room connects to

    def makeDescriptionStr(self, makeDetailed=False):
        outStr = "You find yourself in " + self.name + "."
        if len(self.contains) > 0:
            outStr += " In the room, you see: \n"
            for obj in self.contains:
                outStr += "\t" + obj.makeDescriptionStr() + "\n"
        return outStr

# A door
class Door(GameObject):
    def __init__(self, name):
        GameObject.__init__(self, name)
        self.properties["isMoveable"] = False
        self.properties["is_locked"] = False
        self.properties["is_open"] = False
        self.properties["key"] = None # the key that unlocks this door

    def makeDescriptionStr(self, makeDetailed=False):
        if self.properties["is_locked"]:
            return "the locked " + self.name
        else:
            return "the unlocked " + self.name

# A key
class Key(GameObject):
    def __init__(self, name):
        GameObject.__init__(self, name)
        self.properties["isMoveable"] = True

    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name

# A drawer
class Drawer(Container):
    def __init__(self, name):
        Container.__init__(self, name)
        self.properties["isMoveable"] = False

    def makeDescriptionStr(self, makeDetailed=False):
        outStr = "You find yourself in " + self.name + "."
        if len(self.contains) > 0:
            outStr += " In the drawer, you see: \n"
            for obj in self.contains:
                outStr += "\t" + obj.makeDescriptionStr() + "\n"
        return outStr

# A coin
class Coin(GameObject):
    def __init__(self, name):
        GameObject.__init__(self, name)
        self.properties["isMoveable"] = True

    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name

# The world is the root object of the game object tree.  In single room environments, it's where all the objects are located.
class World(Container):
    def __init__(self):
        Container.__init__(self, "house")

    def makeDescriptionStr(self, makeDetailed=False):
        outStr = "You find yourself in a house.  In the house, you see: \n"
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
        # Number of actions that can earn a reward
        self.full_mark = 0
        # Game Object Tree
        self.rootObject = self.initializeWorld()
        # Game score
        self.score = 0
        self.numSteps = 0
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

        # Add some rooms
        room1 = Room("living room")
        room2 = Room("bedroom")
        room3 = Room("kitchen")
        world.addObject(room1)
        world.addObject(room2)
        world.addObject(room3)

        # Add some doors
        door1 = Door("door")
        door2 = Door("door")
        door3 = Door("door")
        world.addObject(door1)
        world.addObject(door2)
        world.addObject(door3)

        # Add some keys
        key1 = Key("key")
        key2 = Key("key")
        key3 = Key("key")
        world.addObject(key1)
        world.addObject(key2)
        world.addObject(key3)

        # Add some drawers
        drawer1 = Drawer("drawer")
        drawer2 = Drawer("drawer")
        drawer3 = Drawer("drawer")
        world.addObject(drawer1)
        world.addObject(drawer2)
        world.addObject(drawer3)

        # Add some coins
        coin1 = Coin("coin")
        coin2 = Coin("coin")
        coin3 = Coin("coin")
        world.addObject(coin1)
        world.addObject(coin2)
        world.addObject(coin3)

        # Connect the rooms
        room1.properties["connects"].append(room2)
        room1.properties["connects"].append(room3)
        room2.properties["connects"].append(room1)
        room2.properties["connects"].append(room3)
        room3.properties["connects"].append(room1)
        room3.properties["connects"].append(room2)

        # Lock the doors
        door1.properties["is_locked"] = True
        door2.properties["is_locked"] = True
        door3.properties["is_locked"] = True

        # Set the keys for the doors
        door1.properties["key"] = key1
        door2.properties["key"] = key2
        door3.properties["key"] = key3

        # Place the keys in the drawers
        drawer1.addObject(key1)
        drawer2.addObject(key2)
        drawer3.addObject(key3)

        # Place the coins in the rooms
        room1.addObject(coin1)
        room2.addObject(coin2)
        room3.addObject(coin3)

        # Return the world
        return world

    # Get the task description for this game
    def getTaskDescription(self):
        return "Your task is to find the keys, unlock the doors, and collect the coins."

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

        # (1-arg) read
        for objReferent, objs in allObjects.items():
            for obj in objs:
                self.addAction("read " + objReferent, ["read", obj])

        # (1-arg) open/close container
        for objReferent, objs in allObjects.items():
            for obj in objs:
                if obj.getProperty("isContainer"):
                    self.addAction("open " + objReferent, ["open", obj])
                    self.addAction("close " + objReferent, ["close", obj])

        # (1-arg) open/close door
        for objReferent, objs in allObjects.items():
            for obj in objs:
                if obj.getProperty("is_locked"):
                    self.addAction("unlock " + objReferent, ["unlock", obj])

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

        # (2-arg) unlock door with key
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2):
                            self.addAction("unlock " + objReferent1 + " with " + objReferent2, ["unlock", obj1, obj2])

        # (2-arg) move to room
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2):
                            self.addAction("move to " + objReferent1 + " from " + objReferent2, ["move", obj1, obj2])

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

    # read the object
    def actionRead(self, obj):
        # Check the type of the object
        if type(obj) != Room:
            return f"You can't read the {obj.name}."

        # Check if the agent has the object in inventory
        if type(obj.parentContainer) != Agent:
            return f"You should take the {obj.name} first."

        return "You read the " + obj.name + "."

    # open/close container
    def actionOpenCloseContainer(self, container, action):
        # Check if the object is a container
        if (container.getProperty("isContainer") == False):
            return "You can't open/close the " + container.getReferents()[0] + "."

        # Enforce that the object must be in the inventory to do anything with it
        if (container.parentContainer != self.agent):
            return "You don't currently have the " + container.getReferents()[0] + " in your inventory."

        # Open/close the container
        if action == "open":
            obsStr, success = container.openContainer()
        else:
            obsStr, success = container.closeContainer()
        if (success == False):
            return obsStr

        return obsStr

    # unlock door with key
    def actionUnlockDoor(self, door, key):
        # Check if the object is a door
        if type(door) != Door:
            return f"You can't unlock the {door.name}."

        # Check if the object is a key
        if type(key) != Key:
            return f"You can't unlock the {door.name} with the {key.name}."

        # The agent must have the key in inventory
        if type(key.parentContainer) != Agent:
            return f"You should take the {key.name} first."

        # The agent must have the door in inventory
        if type(door.parentContainer) != Agent:
            return f"You should take the {door.name} first."

        # Check if the key is the correct key for the door
        if key != door.properties["key"]:
            return f"The {key.name} doesn't fit the {door.name}."

        # Unlock the door
        door.properties["is_locked"] = False
        return f"You unlock the {door.name} with the {key.name}."

    # move to room
    def actionMoveToRoom(self, room, currentRoom):
        # Check if the object is a room
        if type(room) != Room:
            return f"You can't move to the {room.name}."

        # Check if the agent has the room in inventory
        if type(room.parentContainer) != Agent:
            return f"You should take the {room.name} first."

        # Check if the agent is in the current room
        if type(currentRoom.parentContainer) != Agent:
            return f"You should take the {currentRoom.name} first."

        # Move the agent to the new room
        currentRoom.removeObject(self.agent)
        room.addObject(self.agent)
        return f"You move to the {room.name}."


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


        if actionVerb == "look around":
            # Look around the environment -- i.e. show the description of the world.
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif actionVerb == "inventory":
            # Display the agent's inventory
            self.observationStr = self.actionInventory()

        elif actionVerb == "take":
            # Take an object from a container
            thingToTake = action[1]
            self.observationStr = self.actionTake(thingToTake)

        elif actionVerb == "read":
            # read
            obj = action[1]
            self.observationStr = self.actionRead(obj)

        elif actionVerb == "open":
            # open container
            container = action[1]
            self.observationStr = self.actionOpenCloseContainer(container, "open")

        elif actionVerb == "close":
            # close container
            container = action[1]
            self.observationStr = self.actionOpenCloseContainer(container, "close")

        elif actionVerb == "unlock":
            # unlock door with key
            door = action[1]
            key = action[2]
            self.observationStr = self.actionUnlockDoor(door, key)

        elif actionVerb == "move":
            # move to room
            room = action[1]
            currentRoom = action[2]
            self.observationStr = self.actionMoveToRoom(room, currentRoom)

        # Catch-all
        else:
            self.observationStr = "ERROR: Unknown action."

        # Do one tick of the environment
        self.doWorldTick()

        # Calculate the score
        lastScore = self.score
        self.calculateScore()
        reward = round(self.score - lastScore, 2)

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

        # Check if the agent has all the coins
        for obj in self.rootObject.contains:
            if type(obj) == Coin:
                if type(obj.parentContainer) == Agent:
                    self.score += 1

        # Check if all doors are unlocked
        for obj in self.rootObject.contains:
            if type(obj) == Door:
                if obj.properties["is_locked"]:
                    self.score += 1

        # Check if the agent is in the last room
        if type(self.agent.parentContainer) == Room:
            if self.agent.parentContainer.name == "bedroom":
                self.score += 1

        self.score /= 4
        self.score = round(self.score, 2)





# Main Program
def main():
    # Random seed
    randomSeed = 10

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
