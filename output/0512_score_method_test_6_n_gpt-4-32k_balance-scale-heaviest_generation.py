Here is a text-based simulation for the task of lighting an LED:

```python
import random

class ElectricalObject():
    def __init__(self, name):
        self.name = name
        self.connects = []
        self.properties = {}
        self.properties["is_conductive"] = True

    def connect(self, other):
        self.connects.append(other)
        other.connects.append(self)

    def disconnect(self, other):
        self.connects.remove(other)
        other.connects.remove(self)

    def getReferents(self):
        return [self.name]

    def makeDescriptionStr(self, makeDetailed=False):
        return self.name

class LED(ElectricalObject):
    def __init__(self, name):
        super().__init__(name)
        self.properties["on"] = False
        self.properties["anode"] = None
        self.properties["cathode"] = None

    def update(self):
        if self.properties["anode"] and self.properties["cathode"]:
            self.properties["on"] = True
        else:
            self.properties["on"] = False

class Wire(ElectricalObject):
    def __init__(self, name):
        super().__init__(name)

class Battery(ElectricalObject):
    def __init__(self, name):
        super().__init__(name)
        self.properties["anode"] = None
        self.properties["cathode"] = None

class Workshop():
    def __init__(self):
        self.objects = []

    def addObject(self, obj):
        self.objects.append(obj)

    def removeObject(self, obj):
        self.objects.remove(obj)

    def getAllObjects(self):
        return self.objects

    def makeDescriptionStr(self, makeDetailed=False):
        outStr = "You find yourself in a workshop. In the workshop, you see: \n"
        for obj in self.objects:
            outStr += "\t" + obj.makeDescriptionStr() + "\n"
        return outStr

class TextGame:
    def __init__(self, randomSeed):
        self.random = random.Random(randomSeed)
        self.workshop = self.initializeWorkshop()
        self.score = 0
        self.numSteps = 0
        self.gameOver = False
        self.gameWon = False
        self.observationStr = self.workshop.makeDescriptionStr()

    def initializeWorkshop(self):
        workshop = Workshop()

        led = LED("LED")
        workshop.addObject(led)

        wire1 = Wire("wire1")
        workshop.addObject(wire1)

        wire2 = Wire("wire2")
        workshop.addObject(wire2)

        battery = Battery("battery")
        workshop.addObject(battery)

        return workshop

    def getTaskDescription(self):
        return "Your task is to light up the LED using the available components."

    def makeNameToObjectDict(self):
        allObjects = self.workshop.getAllObjects()

        nameToObjectDict = {}
        for obj in allObjects:
            for name in obj.getReferents():
                if name in nameToObjectDict:
                    nameToObjectDict[name].append(obj)
                else:
                    nameToObjectDict[name] = [obj]

        return nameToObjectDict

    def generatePossibleActions(self):
        self.possibleActions = {}

        allObjects = self.makeNameToObjectDict()

        for objReferent1, objs1 in allObjects.items():
            for objReferent2, objs2 in allObjects.items():
                for obj1 in objs1:
                    for obj2 in objs2:
                        if obj1 != obj2:
                            self.addAction("connect " + objReferent1 + " to " + objReferent2, ["connect", obj1, obj2])

        return self.possibleActions

    def addAction(self, actionStr, actionArgs):
        if not (actionStr in self.possibleActions):
            self.possibleActions[actionStr] = []
        self.possibleActions[actionStr].append(actionArgs)

    def step(self, actionStr):
        self.observationStr = ""

        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return (self.observationStr, self.score, self.gameOver, self.gameWon)

        self.numSteps += 1

        actions = self.possibleActions[actionStr]
        action = None

        if (len(actions) > 1):
            action = actions[0]
        else:
            action = actions[0]

        actionVerb = action[0]

        if (actionVerb == "connect"):
            obj1 = action[1]
            obj2 = action[2]
            obj1.connect(obj2)

            if isinstance(obj1, LED):
                if obj1.properties["anode"] is None and isinstance(obj2, Battery):
                    obj1.properties["anode"] = obj2
                elif obj1.properties["cathode"] is None and isinstance(obj2, Battery):
                    obj1.properties["cathode"] = obj2
                obj1.update()

            if isinstance(obj2, LED):
                if obj2.properties["anode"] is None and isinstance(obj1, Battery):
                    obj2.properties["anode"] = obj1
                elif obj2.properties["cathode"] is None and isinstance(obj1, Battery):
                    obj2.properties["cathode"] = obj1
                obj2.update()

            self.observationStr = f"{obj1.name} is now connected to {obj2.name}."

        self.calculateScore()

        return (self.observationStr, self.score, self.gameOver, self.gameWon)

    def calculateScore(self):
        self.score = 0

        allObjects = self.workshop.getAllObjects()
        for obj in allObjects:
            if isinstance(obj, LED) and obj.properties["on"]:
                self.score += 1
                self.gameOver = True
                self.gameWon = True

def main():
    randomSeed = 0

    game = TextGame(randomSeed=randomSeed)

    print("Task Description: " + game.getTaskDescription())
    print("")
    print("Initial Observation: " + game.observationStr)
    print("")
    print("Type 'help' for a list of possible actions.")
    print("")

    while True:
        actionStr = ""
        while ((len(actionStr) == 0) or (actionStr == "help")):
            actionStr = input("> ")
            if (actionStr == "help"):
                possibleActions = game.generatePossibleActions()
                print("Possible actions: " + str(possibleActions.keys()))
                print("")
                actionStr = ""
            elif (actionStr == "exit") or (actionStr == "quit"):
                return

        observationStr, score, gameOver, gameWon = game.step(actionStr)

        possibleActions = game.generatePossibleActions()

        print("Observation: " + observationStr)
        print("")
        print("Current step: " + str(game.numSteps))
        print("Score: " + str(score))
        print("Game Over: " + str(gameOver))
        print("Game Won: " + str(gameWon))
        print("")
        print("----------------------------------------")

if __name__ == "__main__":
    main()
```

This simulation allows the user to connect components in a workshop to light up an LED. The user can connect the LED to a battery using wires, and the game will be won when the LED is lit. The user can type 'help' to see a list of possible actions.