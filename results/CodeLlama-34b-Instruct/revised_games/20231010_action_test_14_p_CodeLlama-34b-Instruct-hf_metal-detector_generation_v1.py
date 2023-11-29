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

    # (1-arg) Move
    for direction, room in self.current_room.connects.items():
        if room is not None:
            self.addAction("move " + direction, ["move", direction])

    # (1-arg) Examine
    for objReferent, objs in allObjects.items():
        for obj in objs:
            self.addAction("examine " + objReferent, ["examine", obj])

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

def actionMove(self, direction):
    room = self.agent.parentContainer.connects[direction]
    self.agent.removeSelfFromContainer()
    room.addObject(self.agent)
    self.current_room = room
    return f"You move {direction}."

def actionExamine(self, obj):
    # check type of the obj
    if type(obj) == Hole:
        return f"You examine the {obj.name}."
    elif type(obj) == Item:
        return f"You examine the {obj.name}."
    else:
        return f"You can't examine the {obj.name}."

def actionDig(self, shovel):
    # check shovel type
    if type(shovel) != Shovel:
        return f"You can't dig with {shovel.name}."
    # check if the agent has the shovel in inventory
    if type(shovel.parentContainer) != Agent:
        return f"You should take the {shovel.name} first."
    # check if the shovel has non-zero durability
    if shovel.properties["durability"] == 0:
        return f"You can't dig with {shovel.name} because it is broken."

    # dig
    self.current_room.buried = []
    shovel.properties["durability"] -= 1
    return f"You dig with {shovel.name}."

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
    elif (actionVerb == "move"):
        # move to a new location
        target_location = action[1]
        self.observationStr = self.actionMove(target_location)
    elif (actionVerb == "examine"):
        # examine an object
        obj = action[1]
        self.observationStr = self.actionExamine(obj)
    elif (actionVerb == "dig"):
        # dig with a shovel
        shovel = action[1]
        self.observationStr = self.actionDig(shovel)
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

    allObjects = self.rootObject.getAllContainedObjectsRecursive()
    for obj in allObjects:
        if obj.name == "treasure box" and type(obj.parentContainer) == Hole:
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
