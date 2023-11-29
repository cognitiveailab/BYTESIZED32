#
#   Specific Game Objects
#


# A stone
class Stone(GameObject):
    def __init__(self, name, weight):
        GameObject.__init__(self, name)

        self.properties["isMoveable"] = True # A stone is moveable
        self.properties["weight"] = weight # The weight of the stone

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        outStr = "a " + self.name + " that weighs " + str(self.properties["weight"]) + " grams."
        return outStr

# A measuring cup
class MeasuringCup(GameObject):
    def __init__(self, name, volume, containedVolume=0, containsLiquid=False):
        GameObject.__init__(self, name)

        self.properties["isContainer"] = True # A measuring cup is a container
        self.properties["isOpenable"] = False # A measuring cup is not openable
        self.properties["isOpen"] = True # A measuring cup is always open
        self.properties["containerPrefix"] = "in" # The prefix to use when referring to the measuring cup (e.g. "in the measuring cup")
        self.properties["volume"] = volume # The volume of the measuring cup
        self.properties["containedVolume"] = containedVolume # The volume of the liquid in the measuring cup
        self.properties["containsLiquid"] = containsLiquid # Whether the measuring cup contains liquid

    # Try to put an object in the measuring cup.
    # Returns an observation string, and a success flag (boolean)
    def putObjectInMeasuringCup(self, obj):
        # First, check to see if this object is a measuring cup
        if not self.getProperty("isContainer"):
            # If not, then it can't be placed in a measuring cup
            return ("The " + self.name + " is not a measuring cup, so things can't be placed there.", False)

        # Check to see if the object is moveable
        if not obj.getProperty("isMoveable"):
            # If not, then it can't be removed from a measuring cup
            return ("The " + obj.name + " is not moveable.", None, False)

        # If this object is a measuring cup, then check to see if it is open
        if not self.getProperty("isOpen"):
            # If not, then it can't be placed in a measuring cup
            return ("The " + self.name + " is closed, so things can't be placed there.", False)

        # If this object is a measuring cup and it is open, then put the object in the measuring cup
        self.addObject(obj)
        return ("The " + obj.getReferents()[0] + " is placed in the " + self.name + ".", True)

    # Try to take an object from the measuring cup.
    # Returns an observation string, a reference to the object being taken, and a success flag (boolean)
    def takeObjectFromMeasuringCup(self, obj):
        # First, check to see if this object is a measuring cup
        if not self.getProperty("isContainer"):
            # If not, then it can't be removed from a measuring cup
            return ("The " + self.name + " is not a measuring cup, so things can't be removed from it.", None, False)

        # Check to see if the object is moveable
        if not obj.getProperty("isMoveable"):
            # If not, then it can't be removed from a measuring cup
            return ("The " + obj.name + " is not moveable.", None, False)

        # If this object is a measuring cup, then check to see if it is open
        if not self.getProperty("isOpen"):
            # If not, then it can't be removed from a measuring cup
            return ("The " + self.name + " is closed, so things can't be removed from it.", None, False)

        # Check to make sure that the object is contained in this measuring cup
        if obj not in self.contains:
            return ("The " + obj.name + " is not contained in the " + self.name + ".", None, False)

        # If this object is a measuring cup and it is open, then remove the object from the measuring cup
        obj.removeSelfFromContainer()
        return ("The " + obj.getReferents()[0] + " is removed from the " + self.name + ".", obj, True)

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        outStr = "a " + self.name + " that contains " + str(self.properties["containedVolume"]) + " milliliters of liquid."
        return outStr

# A scale
class Scale(GameObject):
    def __init__(self, name):
        GameObject.__init__(self, name)

        self.properties["isActivatable"] = True # Can this device be turned on or off?
        self.properties["isOn"] = False # Is the device currently on or off?
        self.properties["isMoveable"] = False # A scale is not moveable

    # Try to turn on the device.
    # Returns an observation string, and a success flag (boolean)
    def turnOn(self):
        # If the device isn't activatable, then return an error
        if not self.getProperty("isActivatable"):
            return ("It's not clear how the " + self.getReferents()[0] + " could be turned on.", False)

        # If the device is already on, then return an error
        if self.properties["isOn"]:
            return ("The " + self.getReferents()[0] + " is already on.", False)
        else:
            self.properties["isOn"] = True
            return ("The " + self.getReferents()[0] + " is now turned on.", True)

    # Try to turn off the device.
    # Returns an observation string, and a success flag (boolean)
    def turnOff(self):
        # If the device isn't activatable, then return an error
        if not self.getProperty("isActivatable"):
            return ("It's not clear how the " + self.getReferents()[0] + " could be turned off.", False)

        # If the device is already off, then return an error
        if not self.properties["isOn"]:
            return ("The " + self.getReferents()[0] + " is already off.", False)
        else:
            self.properties["isOn"] = False
            return ("The " + self.getReferents()[0] + " is now turned off.", True)

    # If the scale has a parent bath tub, change the water in the bath tub per tick
    def tick(self):
        if self.properties["isOn"] and self.parentContainer is not None and type(self.parentContainer) == Sink:
            water_list = self.parentContainer.containsItemWithName("water")
            # If there is no water in the sink now, add water
            if len(water_list) == 0:
                water = Water(self.properties["water_out_per_tick"])
                self.parentContainer.addObject(water)
            else:
                water = water_list[0]
                # If the water in the sink is hotter than the water from the tap, decrease the temperature of the water in the sink
                if self.properties["water_out_per_tick"] < water.properties["volume"]:
                    water.properties["volume"] = max(water.properties["volume"]-5, self.properties["water_out_per_tick"])
                # if the water in the sink is cooler than the water from the tap, increase the temperature of the water in the sink
                else:
                    water.properties["volume"] = min(water.properties["volume"]+5, self.properties["water_out_per_tick"])

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        outStr = "a " + self.name + ", which is currently "
        if self.properties["isOn"]:
            outStr += "on."
        else:
            outStr += "off."
        return outStr

# A sink
class Sink(Container):
    def __init__(self):
        GameObject.__init__(self, "sink")
        Container.__init__(self, "sink")

        self.properties["containerPrefix"] = "in"
        self.properties["isMoveable"] = False

    def makeDescriptionStr(self, makeDetailed=False):
        outStr = "a sink"
        # Check if open
        if len(self.contains) == 0:
            outStr += " that is empty"
        else:
            outStr += " that contains the following items: \n"
            for obj in self.contains:
                outStr += '\n'.join(["\t" + desc for desc in obj.makeDescriptionStr().strip().split('\n')]) + '\n'

        return outStr

# A water
class Water(GameObject):
    def __init__(self, volume):
        GameObject.__init__(self, "water")

        self.properties["isMoveable"] = False # Water is liquid so we don't allow it to be moved
        self.properties["volume"] = volume

# The world is the root object of the game object tree.  In single room environments, it's where all the objects are located.
class World(Container):
    def __init__(self):
        Container.__init__(self, "room")

    def makeDescriptionStr(self, makeDetailed=False):
        outStr = "You find yourself in a room.  In the room, you see: \n"
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
        self.bath = False
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

        # Add a sink
        sink = Sink()
        world.addObject(sink)

        # Add some water to the sink
        water = Water(self.random.randint(0, 100))
        sink.addObject(water)

        # Add a scale
        scale = Scale("scale")
        world.addObject(scale)

        # Add a stone
        stone = Stone("stone", self.random.randint(100, 1000))
        world.addObject(stone)

        # Add a measuring cup
        measuring_cup = MeasuringCup("measuring cup", 100)
        world.addObject(measuring_cup)

        # Return the world
        return world

    # Get the task description for this game
    def getTaskDescription(self):
        return 'Your task is to measure the density of the stone by putting it on the scale and comparing its weight to the weight of the water in the measuring cup. When you are done, take the action "answer".'

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

        # (0-arg) answer
        self.addAction("answer", ["answer"])

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

    def actionAnswer(self):
        self.bath = True
        return "You answer the question."

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
        elif (actionVerb == "answer"):
            # Answer the question
            self.observationStr = self.actionAnswer()
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

        # Check the water temperature when the agent takes a bath
        if self.bath:
            allObjects = self.rootObject.getAllContainedObjectsRecursive()
            for obj in allObjects:
                if obj.name == "water" and obj.parentContainer.name == "measuring cup":
                    if obj.getProperty("volume") >= 35 and obj.getProperty("volume") <= 40:
                        self.score = 1
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
