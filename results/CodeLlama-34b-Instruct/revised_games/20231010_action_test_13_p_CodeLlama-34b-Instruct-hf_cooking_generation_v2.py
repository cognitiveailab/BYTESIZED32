# Main game loop
while not game.gameOver:

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
