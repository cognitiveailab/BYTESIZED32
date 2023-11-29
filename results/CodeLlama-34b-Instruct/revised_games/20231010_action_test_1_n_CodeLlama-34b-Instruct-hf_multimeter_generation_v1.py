#
#   Action generation
#

def addAction(self, actionStr, actionArgs):
    # Check whether the action string key already exists -- if not, add a blank list
    if not (actionStr in self.possibleActions):
        self.possibleActions[actionStr] = []
    # Add the action arguments to the list
    self.possibleActions[actionStr].append(actionArgs)

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

    # (1-arg) Open
    for objReferent, objs in allObjects.items():
        for obj in objs:
            if obj.getProperty("isContainer"):
                self.addAction("open " + objReferent, ["open", obj])

    # (1-arg) Close
    for objReferent, objs in allObjects.items():
        for obj in objs:
            if obj.getProperty("isContainer"):
                self.addAction("close " + objReferent, ["close", obj])

    # (1-arg) Turn on
    for objReferent, objs in allObjects.items():
        for obj in objs:
            if obj.getProperty("isDevice"):
                self.addAction("turn on " + objReferent, ["turn on", obj])

    # (1-arg) Turn off
    for objReferent, objs in allObjects.items():
        for obj in objs:
            if obj.getProperty("isDevice"):
                self.addAction("turn off " + objReferent, ["turn off", obj])

    # (1-arg) Use
    for objReferent, objs in allObjects.items():
        for obj in objs:
            if obj.getProperty("isThermometer"):
                for obj2Referent, objs2 in allObjects.items():
                    for obj2 in objs2:
                        if obj2.getProperty("isTemperatureObject"):
                            self.addAction("use " + objReferent + " on " + obj2Referent, ["use", obj, obj2])

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

    # Actions with three object arguments
    # (3-arg) Connect
    for objReferent1, objs1 in allObjects.items():
        for objReferent2, objs2 in allObjects.items():
            for objReferent3, objs3 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        for obj3 in objs3:
                            if (obj1 != obj2 and obj1.getProperty("is_temperature_object") and obj2.getProperty("is_temperature_object") and obj3.getProperty("is_temperature_object")):
                                self.addAction("connect " + objReferent1 + " to " + objReferent2 + " to " + objReferent3, ["connect", obj1, obj2, obj3])

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

# Open a container
def actionOpen(self, obj):
    # Check that the object is a container
    if (obj.getProperty("isContainer") == False):
        return "You can't open the " + obj.getReferents()[0] + "."

    # Open the container
    obsStr, success = obj.openContainer()
    if (success == False):
        return obsStr

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

    return obsStr

# Turn on a device
def actionTurnOn(self, obj):
    # Check that the object is a device
    if (obj.getProperty("isDevice") == False):
        return "You can't turn on the " + obj.getReferents()[0] + "."

    # Turn on the device
    obsStr = obj.turnOn()
    return obsStr

# Turn off a device
def actionTurnOff(self, obj):
    # Check that the object is a device
    if (obj.getProperty("isDevice") == False):
        return "You can't turn off the " + obj.getReferents()[0] + "."

    # Turn off the device
    obsStr = obj.turnOff()
    return obsStr

# Use a thermometer on an object
def actionUse(self, thermometer, obj):
    # Check that the object is a thermometer
    if (thermometer.getProperty("isThermometer") == False):
        return "You can't use the " + thermometer.getReferents()[0] + " on the " + obj.getReferents()[0] + "."

    # Check that the object is a temperature object
    if (obj.getProperty("isTemperatureObject") == False):
        return "The " + obj.getReferents()[0] + " does not have a temperature."

    # Use the thermometer on the object
    obsStr = thermometer.measureTemperature(obj)
    return obsStr

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

# Connects two temperature objects
def actionConnect(self, obj1, obj2, obj3):
    # at least one of the two objects should be a stove or a fridge
    if not (obj1.getProperty("is_temperature_object") and obj2.getProperty("is_temperature_object") and obj3.getProperty("is_temperature_object")):
        return "You cannot connect to devices directly."
    # disconnect the terminal if the terminal is already connected to other objects
    if obj1.connects[terminal_1]:
        obj1.disconnect(terminal_1)
    if obj2.connects[terminal_2]:
        obj2.disconnect(terminal_2)
    obj1.connects[terminal_1] = (obj2, terminal_2)
    obj2.connects[terminal_2] = (obj1, terminal_1)
    return f"Successfully connect {obj1.name} to {obj2.name} to {obj3.name}"

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
    elif (actionVerb == "use"):
        # Use a thermometer on an object
        thermometer = action[1]
        obj = action[2]
        self.observationStr = self.actionUse(thermometer, obj)
    elif (actionVerb == "put"):
        # Put an object in a container
        thingToMove = action[1]
        newContainer = action[2]
        self.observationStr = self.actionPut(thingToMove, newContainer)
    elif (actionVerb == "connect"):
        # connect two temperature objects
        obj1, obj2, obj3 = action[1:]
        self.observationStr = self.actionConnect(obj1, obj2, obj3)

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

    if self.answer_temperature is not None:
        if self.answer_temperature == 40:
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
