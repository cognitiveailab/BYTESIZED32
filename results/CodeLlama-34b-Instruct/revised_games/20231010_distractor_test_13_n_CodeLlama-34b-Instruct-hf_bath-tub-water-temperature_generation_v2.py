# A room in the house
class Room(Container):
    def __init__(self, name, connects=None):
        GameObject.__init__(self, name)
        Container.__init__(self, name)

        self.properties["isContainer"] = True
        self.properties["isOpenable"] = False  # A room is not openable
        self.properties["isOpen"] = True      # A room is always open
        self.properties["containerPrefix"] = "in" # The prefix to use when referring to the room (e.g. "in the room", "on the table", etc.)

        # A list of rooms that this room connects to
        self.properties["connects"] = connects

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        outStr = "a room"
        # Check if open
        if len(self.contains) == 0:
            outStr += " that is empty"
        else:
            outStr += " that contains the following items: \n"
            for obj in self.contains:
                outStr += '\n'.join(["\t" + desc for desc in obj.makeDescriptionStr().strip().split('\n')]) + '\n'

        return outStr

# A door that connects two rooms
class Door(GameObject):
    def __init__(self, name, is_locked=False, is_open=False, key=None):
        GameObject.__init__(self, name)

        self.properties["isActivatable"] = True # Can this device be turned on or off?
        self.properties["isOn"] = is_open         # Is the device currently on or off?
        self.properties["isMoveable"] = False   # A door is not moveable
        self.properties["is_locked"] = is_locked # Is the door locked?
        self.properties["is_open"] = is_open     # Is the door open or closed?
        self.properties["key"] = key           # The key that can be used to unlock the door

    # Try to open the door.
    # Returns an observation string, and a success flag (boolean)
    def openDoor(self):
        # If the door is locked, then return an error
        if self.properties["is_locked"]:
            return ("The " + self.getReferents()[0] + " is locked.", False)

        # If the door is already open, then return an error
        if self.properties["is_open"]:
            return ("The " + self.getReferents()[0] + " is already open.", False)

        # If the door is unlocked and closed, then open it
        self.properties["is_open"] = True
        return ("The " + self.getReferents()[0] + " is now open.", True)

    # Try to close the door.
    # Returns an observation string, and a success flag (boolean)
    def closeDoor(self):
        # If the door is locked, then return an error
        if not (self.properties["is_locked"] == True):
            return ("The " + self.getReferents()[0] + " is locked.", False)

        # If the door is already closed, then return an error
        if not (self.properties["is_open"] == True):
            return ("The " + self.getReferents()[0] + " is already closed.", False)

        # If the door is unlocked and open, then close it
        self.properties["is_open"] = False
        return ("The " + self.getReferents()[0] + " is now closed.", True)

    # Try to unlock the door with a key.
    # Returns an observation string, and a success flag (boolean)
    def unlockDoor(self, key):
        # If the door is not locked, then return an error
        if not self.properties["is_locked"]:
            return ("The " + self.getReferents()[0] + " is not locked.", False)

        # If the key is not the correct key, then return an error
        if key != self.properties["key"]:
            return ("The " + self.getReferents()[0] + " can't be unlocked with the " + key.getReferents()[0] + ".", False)

        # If the door is locked and the key is the correct key, then unlock it
        self.properties["is_locked"] = False
        return ("The " + self.getReferents()[0] + " is now unlocked.", True)

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        outStr = "a " + self.name + ", which is currently "
        if self.properties["is_locked"]:
            outStr += "locked."
        else:
            outStr += "unlocked."
        return outStr

# A drawer
class Drawer(Container):
    def __init__(self, name):
        GameObject.__init__(self, name)
        Container.__init__(self, name)

        self.properties["isContainer"] = True
        self.properties["isOpenable"] = True  # A drawer is openable
        self.properties["isOpen"] = False      # A drawer is closed by default
        self.properties["containerPrefix"] = "in" # The prefix to use when referring to the drawer (e.g. "in the drawer", "on the table", etc.)

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        outStr = "a drawer"
        # Check if open
        if len(self.contains) == 0:
            outStr += " that is empty"
        else:
            outStr += " that contains the following items: \n"
            for obj in self.contains:
                outStr += '\n'.join(["\t" + desc for desc in obj.makeDescriptionStr().strip().split('\n')]) + '\n'

        return outStr

# A key
class Key(GameObject):
    def __init__(self, name):
        GameObject.__init__(self, name)

        self.properties["isUsable"] = True # A key is usable

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "a key"

# A coin
class Coin(GameObject):
    def __init__(self, name):
        GameObject.__init__(self, name)

        self.properties["isUsable"] = True # A coin is usable

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "a coin"


# The world is the root object of the game object tree.  In single room environments, it's where all the objects are located.
class World(Container):
    def __init__(self):
        Container.__init__(self, "house")

    def makeDescriptionStr(self, makeDetailed=False):
        outStr = "You find yourself in a house.  In the house, you see: \n"
        for obj in self.contains:
            outStr += '\n'.join(["\t" + desc for desc in obj.makeDescriptionStr().strip().split('\n')]) + '\n'

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
        # A flag of whether the action bath is taken by the agent
        self.coin = False
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
        room1 = Room("room1", connects=["room2"])
        world.addObject(room1)

        # Add a door
        door = Door("door")
        room1.addObject(door)

        # Add a drawer
        drawer = Drawer("drawer")
        room1.addObject(drawer)

        # Add a key
        key = Key("key")
        drawer.addObject(key)

        # Add a room
        room2 = Room("room2", connects=["room1"])
        world.addObject(room2)

        # Add a coin
        coin = Coin("coin")
        room2.addObject(coin)

        # Return the world
        return world

    # Get the task description for this game
    def getTaskDescription(self):
        return 'Your task is to find the keys, unlock the doors, and collect the coin. When you are done, take the action "coin".'

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

        # (0-arg) coin
        self.addAction("coin", ["coin"])

        # Actions with one object argument
        # (1-arg) Take
        for objReferent, objs in allObjects.items():
            for obj in objs:
                self.addAction("take " + objReferent, ["take", obj])
                self.addAction("take " + objReferent + " from " + obj.parentContainer.getReferents()[0], ["take", obj])

        # (1-arg) Turn on/Turn off device
        for objReferent, objs in allObjects.items():
            for obj in objs:
                self.addAction("turn on " + objReferent, ["turn on", obj])
                self.addAction("turn off " + objReferent, ["turn off", obj])

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

        # (2-arg) Use
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if (obj1 != obj2):
                            self.addAction("use " + objReferent1 + " on " + objReferent2, ["use", obj1, obj2])

        # Actions with three object arguments
        # (3-arg) Move
        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for objReferent3, objs3 in allObjects.items():
                    for obj1 in objs1:
                        for obj2 in objs2:
                            for obj3 in objs3:
                                if (obj1 != obj2) and (obj1 != obj3) and (obj2 != obj3):
                                    self.addAction("move " + objReferent1 + " from " + objReferent2 + " to " + objReferent3, ["move", obj1, obj2, obj3])

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

    def actionTurnOn(self, obj):
        # Check if the object is activatable
        if obj.getProperty("isActivatable"):
            # This is handled by the object itself
            obsStr, success = obj.turnOn()
            return obsStr
        else:
            return "You can't turn on that."

    def actionTurnOff(self, obj):
        # Check if the object is activatable
        if obj.getProperty("isActivatable"):
            # This is handled by the object itself
            obsStr, success = obj.turnOff()
            return obsStr
        else:
            return "You can't turn off that."

    def actionUse(self, deviceObj, patientObject):
        # Check if the object is usable
        if deviceObj.getProperty("isUsable"):
            # This is handled by the object itself
            obsStr, _ = deviceObj.useWithObject(patientObject)
            return obsStr
        else:
            return "You can't use that."

    def actionCoin(self):
        self.coin = True
        return "You take the coin."

    def actionMove(self, objToMove, oldContainer, newContainer):
        # Check that the object is in the old container
        if (objToMove.parentContainer != oldContainer):
            return "You don't currently have the " + objToMove.getReferents()[0] + " in your inventory."

        # Take the object from the old container
        obsStr1, objRef, success = objToMove.parentContainer.takeObjectFromContainer(objToMove)
        if (success == False):
            return obsStr1

        # Put the object in the new container
        obsStr2, success = newContainer.placeObjectInContainer(objToMove)
        if (success == False):
            # For whatever reason, the object can't be moved into the new container. Put the object back into the original container
            oldContainer.addObject(objToMove)
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
        elif (actionVerb == "coin"):
            # Take a bath
            self.observationStr = self.actionCoin()
        elif (actionVerb == "take"):
            # Take an object from a container
            thingToTake = action[1]
            self.observationStr = self.actionTake(thingToTake)
        elif (actionVerb == "turn on"):
            # Turn on a device
            thingToTurnOn = action[1]
            self.observationStr = self.actionTurnOn(thingToTurnOn)
        elif (actionVerb == "turn off"):
            # Turn off a device
            thingToTurnOff = action[1]
            self.observationStr = self.actionTurnOff(thingToTurnOff)

        elif (actionVerb == "put"):
            # Put an object in a container
            thingToMove = action[1]
            newContainer = action[2]
            self.observationStr = self.actionPut(thingToMove, newContainer)

        elif (actionVerb == "use"):
            # Use a device on an object
            deviceObj = action[1]
            patientObj = action[2]
            self.observationStr = self.actionUse(deviceObj, patientObj)

        elif (actionVerb == "move"):
            # Move an object from one container to another
            thingToMove = action[1]
            oldContainer = action[2]
            newContainer = action[3]
            self.observationStr = self.actionMove(thingToMove, oldContainer, newContainer)

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

        # Check the coin when the agent takes the coin
        if self.coin:
            allObjects = self.rootObject.getAllContainedObjectsRecursive()
            for obj in allObjects:
                if obj.name == "coin" and obj.parentContainer.name == "room2":
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
