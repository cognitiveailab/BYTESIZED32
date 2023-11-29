def __init__(self, randomSeed):
    # Random number generator, initialized with a seed passed as an argument
    self.random = random.Random(randomSeed)

    # Game Object Tree
    self.rootObject = self.initializeRoom()
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

    # Add the 'capacity_per_plant' attribute
    self.capacity_per_plant = 1000
