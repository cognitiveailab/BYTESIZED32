# keys.py
# based on volume.py
# ruoyao wang (Mar 6/2023)

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

#
#   Specific Game Objects
#

# A room that can be connected to other rooms
class Room(Container):
    def __init__(self, name):
        GameObject.__init__(self, name)
        Container.__init__(self, name)
        # We do not allow the room to be moved in this game
        self.properties['isMoveable'] = False
        self.properties["containerPrefix"] = "in"

    # Connect this room to another room
    def connectRoom(self, otherRoom):
        # Check to see if this room is already connected to the other room
        if otherRoom in self.properties["connects"]:
            return ("The " + self.name + " is already connected to the " + otherRoom.name + ".", False)

        # If not, then connect the rooms
        self.properties["connects"].append(otherRoom)
        return ("The " + self.name + " is now connected to the " + otherRoom.name + ".", True)

    # Disconnect this room from another room
    def disconnectRoom(self, otherRoom):
        # Check to see if this room is connected to the other room
        if otherRoom not in self.properties["connects"]:
            return ("The " + self.name + " is not connected to the " + otherRoom.name + ".", False)

        # If so, then disconnect the rooms
        self.properties["connects"].remove(otherRoom)
        return ("The " + self.name + " is no longer connected to the " + otherRoom.name + ".", True)

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        outStr = "You find yourself in a room. In the room, you see: \n"
        for obj in self.contains:
            outStr += "\t" + obj.makeDescriptionStr() + "\n"

        return outStr

# A door that can be locked and unlocked
class Door(Container):
    def __init__(self, name):
        GameObject.__init__(self, name)
        Container.__init__(self, name)
        # We do not allow the door to be moved in this game
        self.properties['isMoveable'] = False
        self.properties["containerPrefix"] = "on"
        self.properties["isLocked"] = False
        self.properties["key"] = None

    # Try to open the door
    # Returns an observation string, and a success flag (boolean)
    def openDoor(self):
        # First, check to see if the door is locked
        if self.getProperty("isLocked"):
            # If so, then it can't be opened
            return ("The " + self.name + " is locked.", False)

        # If the door is not locked, then open it
        self.properties["isOpen"] = True
        return ("The " + self.name + " is now open.", True)

    # Try to close the door
    # Returns an observation string, and a success flag (boolean)
    def closeDoor(self):
        # First, check to see if the door is locked
        if self.getProperty("isLocked"):
            # If so, then it can't be closed
            return ("The " + self.name + " is locked.", False)

        # If the door is not locked, then close it
        self.properties["isOpen"] = False
        return ("The " + self.name + " is now closed.", True)

    # Try to lock the door with a key
    # Returns an observation string, and a success flag (boolean)
    def lockDoorWithKey(self, key):
        # First, check to see if the door is already locked
        if self.getProperty("isLocked"):
            # If so, then it can't be locked
            return ("The " + self.name + " is already locked.", False)

        # If the door is not locked, then check to see if the key is the correct key
        if key != self.getProperty("key"):
            # If not, then it can't be locked
            return ("The " + self.name + " can't be locked with the " + key.name + ".", False)

        # If the door is not locked and the key is the correct key, then lock the door
        self.properties["isLocked"] = True
        return ("The " + self.name + " is now locked with the " + key.name + ".", True)

    # Try to unlock the door with a key
    # Returns an observation string, and a success flag (boolean)
    def unlockDoorWithKey(self, key):
        # First, check to see if the door is already unlocked
        if not self.getProperty("isLocked"):
            # If so, then it can't be unlocked
            return ("The " + self.name + " is already unlocked.", False)

        # If the door is locked, then check to see if the key is the correct key
        if key != self.getProperty("key"):
            # If not, then it can't be unlocked
            return ("The " + self.name + " can't be unlocked with the " + key.name + ".", False)

        # If the door is locked and the key is the correct key, then unlock the door
        self.properties["isLocked"] = False
        return ("The " + self.name + " is now unlocked with the " + key.name + ".", True)

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        if self.getProperty("isLocked"):
            return "a locked " + self.name
        else:
            return "an unlocked " + self.name

# A drawer that can be opened and closed
class Drawer(Container):
    def __init__(self, name):
        GameObject.__init__(self, name)
        Container.__init__(self, name)
        # We do not allow the drawer to be moved in this game
        self.properties['isMoveable'] = False
        self.properties["containerPrefix"] = "in"

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "a drawer"

# A key that can be used to unlock doors
class Key(GameObject):
    def __init__(self, name):
        GameObject.__init__(self, name)
        # We do not allow the key to be moved in this game
        self.properties['isMoveable'] = False

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "a key"

# A coin that can be taken
class Coin(GameObject):
    def __init__(self, name):
        GameObject.__init__(self, name)
        # We do not allow the coin to be moved in this game
        self.properties['isMoveable'] = False

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "a coin"

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
        # Variable to store the answer
        self.answer_weight = None
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
        world = Room("house")

        # Add the agent
        world.addObject(self.agent)

        # possible rooms to connect
        possible_rooms = ['kitchen', 'living room', 'bedroom', 'bathroom']
        self.random.shuffle(possible_rooms)

        # generate 2-5 rooms
        # one room is the target room and the others are distractors
        num_rooms = self.random.randint(2,5)
        for i in range(num_rooms):
            room = Room(possible_rooms[i])
            world.addObject(room)

        # record the target room name
        self.target_room = possible_rooms[0]

        # possible doors to connect
        possible_doors = ['front door', 'back door', 'side door']
        self.random.shuffle(possible_doors)

        # generate 2-5 doors
        # one door is the target door and the others are distractors
        num_doors = self.random.randint(2,5)
        for i in range(num_doors):
            door = Door(possible_doors[i])
            world.addObject(door)

        # record the target door name
        self.target_door = possible_doors[0]

        # possible keys to unlock the door
        possible_keys = ['key1', 'key2', 'key3']
        self.random.shuffle(possible_keys)

        # generate 2-5 keys
        # one key is the target key and the others are distractors
        num_keys = self.random.randint(2,5)
        for i in range(num_keys):
            key = Key(possible_keys[i])
            world.addObject(key)

        # record the target key name
        self.target_key = possible_keys[0]

        # possible coins to take
        possible_coins = ['coin1', 'coin2', 'coin3']
        self.random.shuffle(possible_coins)

        # generate 2-5 coins
        # one coin is the target coin and the others are distractors
        num_coins = self.random.randint(2,5)
        for i in range(num_coins):
            coin = Coin(possible_coins[i])
            world.addObject(coin)

        # record the target coin name
        self.target_coin = possible_coins[0]

        # Add a drawer
        drawer = Drawer("drawer")
        world.addObject(drawer)

        # Return the world
        return world

    # Get the task description for this game
    def getTaskDescription(self):
        return f"Your task is to find the {self.target_key}, unlock the {self.target_door}, move to the {self.target_room}, and take the {self.target_coin}."

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

        # (1-arg) Detailed look/examine
        for objReferent, objs in allObjects.items():
            for obj in objs:
                self.addAction("examine " + objReferent, ["examine", obj])

        # (1-arg) Open/close container
        for objReferent, objs in allObjects.items():
            for obj in objs:
                if obj.getProperty("isContainer"):
                    self.addAction("open " + objReferent, ["open", obj])
                    self.addAction("close " + objReferent, ["close", obj])

        # (1-arg) Open/close door
        for objReferent, objs in allObjects.items():
            for obj in objs:
                if obj.getProperty("isDoor"):
                    self.addAction("open " + objReferent, ["open", obj])
                    self.addAction("close " + objReferent, ["close", obj])

        # (1-arg) Unlock door with key
        for objReferent, objs in allObjects.items():
            for obj in objs:
                if obj.getProperty("isDoor"):
                    self.addAction("unlock " + objReferent + " with " + self.target_key, ["unlock", obj, self.target_key])

        # (1-arg) Move to room
        for objReferent, objs in allObjects.items():
            for obj in objs:
                if obj.getProperty("isRoom"):
                    self.addAction("move to " + objReferent, ["move to", obj])

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

    # Open/close a container
    def actionOpenCloseContainer(self, obj):
        # Check that the object is a container
        if (obj.getProperty("isContainer") == False):
            return "You can't open or close the " + obj.getReferents()[0] + "."

        # Open/close the container
        if obj.getProperty("isOpen"):
            obsStr, success = obj.closeContainer()
        else:
            obsStr, success = obj.openContainer()
        if (success == False):
            return obsStr

        # Success -- show the observation
        return obsStr

    # Open/close a door
    def actionOpenCloseDoor(self, obj):
        # Check that the object is a door
        if (obj.getProperty("isDoor") == False):
            return "You can't open or close the " + obj.getReferents()[0] + "."

        # Open/close the door
        if obj.getProperty("isOpen"):
            obsStr, success = obj.closeDoor()
        else:
            obsStr, success = obj.openDoor()
        if (success == False):
            return obsStr

        # Success -- show the observation
        return obsStr

    # Unlock a door with a key
    def actionUnlockDoorWithKey(self, obj, key):
        # Check that the object is a door
        if (obj.getProperty("isDoor") == False):
            return "You can't unlock the " + obj.getReferents()[0] + "."

        # Unlock the door with the key
        obsStr, success = obj.unlockDoorWithKey(key)
        if (success == False):
            return obsStr

        # Success -- show the observation
        return obsStr

    # Move to a room
    def actionMoveToRoom(self, room):
        # Check that the object is a room
        if (room.getProperty("isRoom") == False):
            return "You can't move to the " + room.getReferents()[0] + "."

        # Move to the room
        obsStr = "You move to the " + room.getReferents()[0] + "."
        self.rootObject = room

        # Do one tick of the environment
        self.doWorldTick()

        # Return the observation
        return obsStr

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
        elif (actionVerb == "examine"):
            # Examine an object
            thingToExamine = action[1]
            self.observationStr = thingToExamine.makeDescriptionStr(makeDetailed = True)
        elif (actionVerb == "take"):
            # Take an object from a container
            thingToTake = action[1]
            self.observationStr = self.actionTake(thingToTake)
        elif (actionVerb == "put"):
            # Put an object in a container
            thingToMove = action[1]
            newContainer = action[2]
            self.observationStr = self.actionPut(thingToMove, newContainer)
        elif (actionVerb == "open"):
            # Open a container
            thingToOpen = action[1]
            self.observationStr = self.actionOpenCloseContainer(thingToOpen)
        elif (actionVerb == "close"):
            # Close a container
            thingToClose = action[1]
            self.observationStr = self.actionOpenCloseContainer(thingToClose)
        elif (actionVerb == "unlock"):
            # Unlock a door with a key
            thingToUnlock = action[1]
            key = action[2]
            self.observationStr = self.actionUnlockDoorWithKey(thingToUnlock, key)
        elif (actionVerb == "move to"):
            # Move to a room
            roomToMoveTo = action[1]
            self.observationStr = self.actionMoveToRoom(roomToMoveTo)
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

        # Check if the agent is in the target room
        if self.rootObject.name == self.target_room:
            # Check if the target coin is in the inventory
            if self.agent.containsItemWithName(self.target_coin):
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
    randomSeed = 1

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
