# The base class for all game objects
class GameObject:
    def __init__(self, name):
        self.name = name
        self.properties = {}
        self.contains = []

    def getProperty(self, propertyName):
        if propertyName in self.properties:
            return self.properties[propertyName]
        else:
            return None

    def setProperty(self, propertyName, propertyValue):
        self.properties[propertyName] = propertyValue

    def addObject(self, obj):
        self.contains.append(obj)

    def removeObject(self, obj):
        self.contains.remove(obj)

    def getAllContainedObjectsRecursive(self):
        containedObjects = []
        for obj in self.contains:
            containedObjects.append(obj)
            containedObjects += obj.getAllContainedObjectsRecursive()
        return containedObjects

    def makeDescriptionStr(self, makeDetailed=False):
        return self.name

    def tick(self):
        pass

# A container is a game object that can contain other game objects
class Container(GameObject):
    def __init__(self, name):
        GameObject.__init__(self, name)
        self.properties["isContainer"] = True
        self.properties["isOpenable"] = True
        self.properties["isOpen"] = True
        self.properties["containerPrefix"] = "in"

    def placeObjectInContainer(self, obj):
        if self.properties["isOpen"]:
            self.contains.append(obj)
            return "You put the " + obj.makeDescriptionStr() + " in the " + self.makeDescriptionStr() + ".", True
        else:
            return "You can't put things in the " + self.makeDescriptionStr() + " because it is closed.", False

    def takeObjectFromContainer(self, obj):
        if self.properties["isOpen"]:
            self.contains.remove(obj)
            return "You took the " + obj.makeDescriptionStr() + " out of the " + self.makeDescriptionStr() + ".", obj, True
        else:
            return "You can't take things out of the " + self.makeDescriptionStr() + " because it is closed.", None, False

    def makeDescriptionStr(self, makeDetailed=False):
        if self.properties["isOpen"]:
            return "an open " + self.name
        else:
            return "a closed " + self.name

# A liquid is a game object that can be poured into a measuring cup
class Liquid(GameObject):
    def __init__(self, name, volume):
        GameObject.__init__(self, name)
        self.properties["volume"] = volume

    def makeDescriptionStr(self, makeDetailed=False):
        return "a liquid"

# A water is a game object that can be poured into a measuring cup
class Water(Liquid):
    def __init__(self, name, volume):
        Liquid.__init__(self, name, volume)
        self.properties["isLiquid"] = True

    def makeDescriptionStr(self, makeDetailed=False):
        return "water"

# A stone is a game object that can be put on a scale
class Stone(GameObject):
    def __init__(self, name, weight):
        GameObject.__init__(self, name)
        self.properties["weight"] = weight

    def makeDescriptionStr(self, makeDetailed=False):
        if self.name[0].lower() in ['a','e','i','o','u']:
            det = 'an'
        else:
            det = 'a'
        return f"{det} {self.name}"

# A measuring cup is a container that can be used to measure the volume of a liquid
class MeasuringCup(Container):
    def __init__(self, name):
        Container.__init__(self, name)
        self.properties["isMeasuringCup"] = True
        self.properties["containsLiquid"] = False
        self.properties["containedVolume"] = 0

    def makeDescriptionStr(self, makeDetailed=False):
        if self.properties["containsLiquid"]:
            return "a measuring cup containing " + str(self.properties["containedVolume"]) + "ml of liquid."
        else:
            return "an empty measuring cup."

# A scale is a container that measures the total weight of the objects on it
class Scale(Container):
    def __init__(self):
        Container.__init__(self, "scale")
        # We do not allow the scale to be moved in this game
        self.properties['isMoveable'] = False
        self.properties["containerPrefix"] = "on"

    def makeDescriptionStr(self, makeDetailed=False):
        if len(self.contains) == 0:
            return "a scale which reads 0g"
        else:
            total_weights = 0
            outStr = "contains "
            for i in range(len(self.contains)):
                if (i == len(self.contains) - 1) and (len(self.contains) > 1):
                    outStr += "and "
                outStr += self.contains[i].makeDescriptionStr() + ", "
                total_weights += self.contains[i].getProperty("weight")

            outStr = outStr[:-2]
            return f"a scale which reads {total_weights}g and {outStr}"

# A sink is a container that can be turned on and off, and which has a certain amount of water that flows out per tick
class Sink(Container):
    def __init__(self, name, water_out_per_tick):
        Container.__init__(self, name)
        self.properties["isSink"] = True
        self.properties["water_out_per_tick"] = water_out_per_tick
        self.properties["containsLiquid"] = True
        self.properties["containedVolume"] = 0

    def makeDescriptionStr(self, makeDetailed=False):
        if self.properties["isOpen"]:
            return "a sink with water flowing out of it."
        else:
            return "a sink with water flowing out of it, but it is turned off."

    def tick(self):
        if self.properties["isOpen"]:
            self.properties["containedVolume"] += self.properties["water_out_per_tick"]

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
        self.answer_density = None
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

        # possible objects to measure
        possible_objects = ['stone', 'measuring cup', 'scale', 'sink', 'water']
        self.random.shuffle(possible_objects)

        # generate 2-5 objects
        # one object is the target object and the others are distractors
        num_objects = self.random.randint(2,5)
        weights = self.random.choices(range(150, 300), k=num_objects)
        target_id = self.random.randint(0, num_objects-1)

        for i in range(num_objects):
            obj = Stone(possible_objects[i],weights[i])
            world.addObject(obj)

        # record the target object name weight
        self.target_object = possible_objects[target_id]
        self.target_weight = weights[target_id]

        # Add a measuring cup
        measuring_cup = MeasuringCup("measuring cup")
        world.addObject(measuring_cup)

        # Add a scale
        scale = Scale()
        world.addObject(scale)

        # Add a sink
        sink = Sink("sink", 10)
        world.addObject(sink)

        # Add water
        water = Water("water", 100)
        world.addObject(water)

        # Return the world
        return world

    # Get the task description for this game
    def getTaskDescription(self):
        return f"Your task is to figure out the density of the {self.target_object}."

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

        # (1-arg) Answer
        for i in range(150, 300):
            self.addAction(f"answer {i}g/cm^3", ["answer", i])

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

        # (2-arg) Turn on/off
        for objReferent, objs in allObjects.items():
            for obj in objs:
                if obj.properties["isOpenable"]:
                    self.addAction("turn on " + objReferent, ["turn on", obj])
                    self.addAction("turn off " + objReferent, ["turn off", obj])

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

    # Turn on/off
    def actionTurnOnOff(self, obj):
        # Check that the object is openable
        if (obj.getProperty("isOpenable") == False):
            return "You can't turn the " + obj.getReferents()[0] + " on or off."

        # Toggle the isOpen property
        obj.properties["isOpen"] = not obj.properties["isOpen"]
        return "You turn the " + obj.getReferents()[0] + " " + ("on" if obj.properties["isOpen"] else "off") + "."

    # Answer
    def actionAnswer(self, density):
        self.answer_density = density
        return f"You believe the density of the {self.target_object} is {density}g/cm^3."

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
        elif (actionVerb == "turn on"):
            # Turn on an object
            thingToTurnOn = action[1]
            self.observationStr = self.actionTurnOnOff(thingToTurnOn)
        elif (actionVerb == "turn off"):
            # Turn off an object
            thingToTurnOff = action[1]
            self.observationStr = self.actionTurnOnOff(thingToTurnOff)
        elif (actionVerb == "answer"):
            # Answer the density
            answer = action[1]
            self.observationStr = self.actionAnswer(answer)
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

        if self.answer_density is not None:
            if self.target_density == self.answer_density:
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
