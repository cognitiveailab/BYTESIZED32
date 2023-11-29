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

# Examine an object
def actionExamine(self, obj):
    # Check to make sure the object is in the environment
    if (obj.parentContainer == None):
        return "You don't currently have the " + obj.getReferents()[0] + " in your inventory."

    # Examine the object
    return obj.makeDescriptionStr(makeDetailed = True)

# Measure an object with a ruler
def actionMeasure(self, objToMeasure, ruler):
    # Check to make sure the object is in the environment
    if (objToMeasure.parentContainer == None):
        return "You don't currently have the " + objToMeasure.getReferents()[0] + " in your inventory."

    # Check to make sure the ruler is in the environment
    if (ruler.parentContainer == None):
        return "You don't currently have the " + ruler.getReferents()[0] + " in your inventory."

    # Measure the object with the ruler
    return f"You measure the {objToMeasure.getReferents()[0]} with the {ruler.getReferents()[0]}."

# Answer
def actionAnswer(self, area):
    self.agent_answer_area = area
    return f"You believe the area of the paper is {area} cm^2."

# Turn on a device
def actionTurnOn(self, device):
    # Check to make sure the device is in the environment
    if (device.parentContainer == None):
        return "You don't currently have the " + device.getReferents()[0] + " in your inventory."

    # Turn on the device
    return f"You turn on the {device.getReferents()[0]}."

# Turn off a device
def actionTurnOff(self, device):
    # Check to make sure the device is in the environment
    if (device.parentContainer == None):
        return "You don't currently have the " + device.getReferents()[0] + " in your inventory."

    # Turn off the device
    return f"You turn off the {device.getReferents()[0]}."

#
#   Performs an action in the environment, returns the result (a string observation, the reward, and whether the game is completed).
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
        self.observationStr = self.actionExamine(thingToExamine)
    elif (actionVerb == "take"):
        # Take an object from a container
        thingToTake = action[1]
        self.observationStr = self.actionTake(thingToTake)
    elif (actionVerb == "turn on"):
        # turn on a sink
        thingToTurnOn = action[1]
        self.observationStr = self.actionTurnOn(thingToTurnOn)
    elif (actionVerb == "turn off"):
        # Turn off a sink
        thingToTurnOff = action[1]
        self.observationStr = self.actionTurnOff(thingToTurnOff)

    elif (actionVerb == "put"):
        # Put an object in a container
        thingToMove = action[1]
        newContainer = action[2]
        self.observationStr = self.actionPut(thingToMove, newContainer)
    elif (actionVerb == "measure"):
        # Measure an object with a ruler
        thingToMeasure = action[1]
        ruler = action[2]
        self.observationStr = self.actionMeasure(thingToMeasure, ruler)
    elif (actionVerb == "answer"):
        # answer
        answer = action[1]
        self.observationStr = self.actionAnswer(answer)

    # Catch-all
    else:
        self.observationStr = "ERROR: Unknown action."

    # Do one tick of the environment
    tick_output_strs = self.doWorldTick()
    # if any tick output some information, add it to the output string
    if len(tick_output_strs) > 0:
        self.observationStr = '\n'.join([self.observationStr] + tick_output_strs)
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
    output_strs = []
    for obj in allObjects:
        tick_output_str = obj.tick()
        if tick_output_str is not None:
            output_strs.append(tick_output_str)
    return output_strs

# Calculate the game score
def calculateScore(self):
    # Baseline score
    self.score = 0

    if self.agent_answer_area is not None:
        if self.answer_area == self.agent_answer_area:
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
