#
#   Abstract Device Classes
#

# Abstract class for things that can be considered 'devices' (e.g. a stove, a light, a computer, etc.)
class Device(GameObject):
    def __init__(self, name):
        # Prevent this constructor from running if it's already been run during multiple inheritance
        if hasattr(self, "constructorsRun"):
            if "Device" in self.constructorsRun:
                return

        GameObject.__init__(self, name)
        # Otherwise, mark this constructor as having been run
        self.constructorsRun.append("Device")

        self.properties["isDevice"] = True
        self.properties["isOn"] = False      # Is the device on or off (if it is on/offable)
        self.properties["isOnable"] = False  # Can the device be turned on or off (e.g. a light, a stove, etc.), or is it always 'on' (e.g. a computer, etc.)

    # Try to turn the device on
    # Returns an observation string, and a success flag (boolean)
    def turnOnDevice(self):
        # First, check to see if this object is onable
        if not self.getProperty("isOnable"):
            # If not, then it can't be turned on
            return ("The " + self.name + " can't be turned on.", False)

        # If this object is onable, then check to see if it is already on
        if self.getProperty("isOn"):
            # If so, then it can't be turned on
            return ("The " + self.name + " is already on.", False)

        # If this object is onable and it is off, then turn it on
        self.properties["isOn"] = True
        return ("The " + self.name + " is now on.", True)

    # Try to turn the device off
    # Returns an observation string, and a success flag (boolean)
    def turnOffDevice(self):
        # First, check to see if this object is onable
        if not (self.getProperty("isOnable") == True):
            # If not, then it can't be turned off
            return ("The " + self.name + " can't be turned off.", False)

        # If this object is onable, then check to see if it is already off
        if not (self.getProperty("isOn") == True):
            # If so, then it can't be turned off
            return ("The " + self.name + " is already off.", False)

        # If this object is onable and it is on, then turn it off
        self.properties["isOn"] = False
        return ("The " + self.name + " is now off.", True)

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

#
#   Specific Game Objects
#

# A device that can heat objects
class Stove(Device):
    def __init__(self):
        GameObject.__init__(self, "stove")
        Device.__init__(self, "stove")
        # We do not allow the stove to be moved in this game
        self.properties['isMoveable'] = False
        self.properties["isOnable"] = True
        self.properties["temperature_increase_per_tick"] = 10
        self.properties["max_temperature"] = 100

    def makeDescriptionStr(self, makeDetailed=False):
        if self.getProperty("isOn"):
            return "a stove that is on."
        else:
            return "a stove that is off."

# A device that can cool objects
class Fridge(Device):
    def __init__(self):
        GameObject.__init__(self, "fridge")
        Device.__init__(self, "fridge")
        # We do not allow the fridge to be moved in this game
        self.properties['isMoveable'] = False
        self.properties["isOnable"] = True
        self.properties["temperature_decrease_per_tick"] = 10
        self.properties["min_temperature"] = 0

    def makeDescriptionStr(self, makeDetailed=False):
        if self.getProperty("isOn"):
            return "a fridge that is on."
        else:
            return "a fridge that is off."

# A device that can measure the temperature of objects
class Thermometer(Device):
    def __init__(self):
        GameObject.__init__(self, "thermometer")
        Device.__init__(self, "thermometer")
        # We do not allow the thermometer to be moved in this game
        self.properties['isMoveable'] = False
        self.properties["isOnable"] = False

    def makeDescriptionStr(self, makeDetailed=False):
        return "a thermometer."

# An object that can be heated
class Milk(GameObject):
    def __init__(self, name, temperature):
        GameObject.__init__(self, name)
        self.properties["temperature"] = temperature

    def makeDescriptionStr(self, makeDetailed=False):
        return "a " + self.name + " that is " + str(self.getProperty("temperature")) + " degrees Celsius."

# A container that can hold objects
class Pot(Container):
    def __init__(self, name):
        GameObject.__init__(self, name)
        Container.__init__(self, name)
        # We do not allow the pot to be moved in this game
        self.properties['isMoveable'] = False

    def makeDescriptionStr(self, makeDetailed=False):
        if len(self.contains) == 0:
            return "an empty pot."
        else:
            return "a pot containing " + self.contains[0].makeDescriptionStr() + "."

# The world is the root object of the game object tree.  In single room environments, it's where all the objects are located.
class World(Container):
    def __init__(self):
        Container.__init__(self, "room")

    def makeDescriptionStr(self, makeDetailed=False):
        outStr = "You find yourself in a room. In the room, you see: \n"
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
        world = World()

        # Add the agent
        world.addObject(self.agent)

        # possible objects to heat
        possible_objects = ['milk']
        self.random.shuffle(possible_objects)

        # generate 1 object
        # one object is the target object and the others are distractors
        num_objects = 1
        temperatures = self.random.choices(range(0, 100), k=num_objects)
        target_id = self.random.randint(0, num_objects-1)

        for i in range(num_objects):
            obj = Milk(possible_objects[i],temperatures[i])
            world.addObject(obj)

        # record the target object name weight
        self.target_object = possible_objects[target_id]
        self.target_temperature = temperatures[target_id]

        # Add a stove
        stove = Stove()
        world.addObject(stove)

        # Add a fridge
        fridge = Fridge()
        world.addObject(fridge)

        # Add a thermometer
        thermometer = Thermometer()
        world.addObject(thermometer)

        # Add a pot
        pot = Pot("pot")
        world.addObject(pot)

        # Return the world
        return world

    # Get the task description for this game
    def getTaskDescription(self):
        return f"Your task is to heat the {self.target_object} to a temperature that is suitable for a baby."

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

        # (1-arg) Open
        for objReferent, objs in allObjects.items():
            for obj in objs:
                self.addAction("open " + objReferent, ["open", obj])

        # (1-arg) Close
        for objReferent, objs in allObjects.items():
            for obj in objs:
                self.addAction("close " + objReferent, ["close", obj])

        # (1-arg) Turn on
        for objReferent, objs in allObjects.items():
            for obj in objs:
                self.addAction("turn on " + objReferent, ["turn on", obj])

        # (1-arg) Turn off
        for objReferent, objs in allObjects.items():
            for obj in objs:
                self.addAction("turn off " + objReferent, ["turn off", obj])

        # (1-arg) Use thermometer on object
        for objReferent, objs in allObjects.items():
            for obj in objs:
                self.addAction("use thermometer on " + objReferent, ["use thermometer on", obj])

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

    # Open a container
    def actionOpen(self, obj):
        # Check that the object is a container
        if (obj.getProperty("isContainer") == False):
            return "You can't open the " + obj.getReferents()[0] + "."

        # Open the container
        obsStr, success = obj.openContainer()
        if (success == False):
            return obsStr

        # Success -- show the observation
        return obsStr

    # Close a container
    def actionClose(self, obj):
        # Check that the object is a container
        if (obj.getProperty("isContainer") == False):
            return "You can't close the " + obj.getReferents()[0] + "."

        # Close the container
        obsStr, success = obj.closeContainer()
        if (success == False):
            return obsStr

        # Success -- show the observation
        return obsStr

    # Turn on a device
    def actionTurnOn(self, obj):
        # Check that the object is a device
        if (obj.getProperty("isDevice") == False):
            return "You can't turn on the " + obj.getReferents()[0] + "."

        # Turn on the device
        obsStr, success = obj.turnOnDevice()
        if (success == False):
            return obsStr

        # Success -- show the observation
        return obsStr

    # Turn off a device
    def actionTurnOff(self, obj):
        # Check that the object is a device
        if (obj.getProperty("isDevice") == False):
            return "You can't turn off the " + obj.getReferents()[0] + "."

        # Turn off the device
        obsStr, success = obj.turnOffDevice()
        if (success == False):
            return obsStr

        # Success -- show the observation
        return obsStr

    # Use a thermometer on an object
    def actionUseThermometerOn(self, obj):
        # Check that the object is a thermometer
        if (obj.getProperty("isDevice") == False):
            return "You can't use the " + obj.getReferents()[0] + "."

        # Check that the object is a thermometer
        if (obj.getProperty("isOn") == False):
            return "The " + obj.getReferents()[0] + " is not on."

        # Use the thermometer on the object
        obsStr = "The " + obj.getReferents()[0] + " reads " + str(obj.getProperty("temperature")) + " degrees Celsius."
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
            self.observationStr = self.actionOpen(thingToOpen)
        elif (actionVerb == "close"):
            # Close a container
            thingToClose = action[1]
            self.observationStr = self.actionClose(thingToClose)
        elif (actionVerb == "turn on"):
            # Turn on a device
            thingToTurnOn = action[1]
            self.observationStr = self.actionTurnOn(thingToTurnOn)
        elif (actionVerb == "turn off"):
            # Turn off a device
            thingToTurnOff = action[1]
            self.observationStr = self.actionTurnOff(thingToTurnOff)
        elif (actionVerb == "use thermometer on"):
            # Use a thermometer on an object
            thingToUseThermometerOn = action[1]
            self.observationStr = self.actionUseThermometerOn(thingToUseThermometerOn)
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

        if self.answer_weight is not None:
            if self.target_weight == self.answer_weight:
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
