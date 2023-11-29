import random

class ElectricalObject():
    def __init__(self, name):
        self.name = name
        self.connects = []
        self.is_conductive = False

class LED(ElectricalObject):
    def __init__(self):
        super().__init__("LED")
        self.on = False
        self.anode = None
        self.cathode = None

class Wire(ElectricalObject):
    def __init__(self):
        super().__init__("Wire")
        self.is_conductive = True

class Battery(ElectricalObject):
    def __init__(self):
        super().__init__("Battery")
        self.anode = None
        self.cathode = None

class TextGame:
    def __init__(self, randomSeed):
        self.random = random.Random(randomSeed)
        self.led = LED()
        self.wire1 = Wire()
        self.wire2 = Wire()
        self.battery = Battery()
        self.score = 0

    def getTaskDescription(self):
        return "Your task is to connect the LED to the battery using the wires to light it up."

    def generatePossibleActions(self):
        actions = [
            "look",
            "inventory",
            "examine LED",
            "examine Wire",
            "examine Battery",
            "connect LED anode to Battery anode with Wire",
            "connect LED cathode to Battery cathode with Wire",
        ]
        return actions

    def step(self, actionStr):
        if actionStr == "connect LED anode to Battery anode with Wire":
            self.led.anode = self.battery.anode
            self.led.connects.append(self.wire1)
            self.battery.connects.append(self.wire1)
            return "LED anode is connected to Battery anode with a Wire."
        elif actionStr == "connect LED cathode to Battery cathode with Wire":
            self.led.cathode = self.battery.cathode
            self.led.connects.append(self.wire2)
            self.battery.connects.append(self.wire2)
            return "LED cathode is connected to Battery cathode with a Wire."
        else:
            return "Invalid action."

    def calculateScore(self):
        if self.led.anode == self.battery.anode and self.led.cathode == self.battery.cathode:
            self.led.on = True
            self.score = 1
        else:
            self.led.on = False
            self.score = 0
        return self.score

def main():
    randomSeed = 0
    game = TextGame(randomSeed=randomSeed)

    print("Task Description: " + game.getTaskDescription())
    print("")

    possibleActions = game.generatePossibleActions()
    print("Possible actions: " + str(possibleActions))
    print("")

    while True:
        actionStr = input("> ")
        if actionStr == "exit" or actionStr == "quit":
            break

        if actionStr in possibleActions:
            result = game.step(actionStr)
            print(result)
            score = game.calculateScore()
            print("Score: " + str(score))
            if score == 1:
                print("Congratulations! You have successfully lit the LED.")
                break
        else:
            print("Invalid action. Type 'help' for a list of possible actions.")

        if actionStr == "help":
            print("Possible actions: " + str(possibleActions))
            print("")

if __name__ == "__main__":
    main()
