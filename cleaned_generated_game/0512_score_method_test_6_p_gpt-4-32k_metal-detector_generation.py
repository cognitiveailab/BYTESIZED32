import random

class ElectricalObject():
    def __init__(self, name, is_conductive=False):
        self.name = name
        self.is_conductive = is_conductive
        self.connects = {"A": None, "B": None}

    def connect(self, terminal, other, other_terminal):
        self.connects[terminal] = (other, other_terminal)
        other.connects[other_terminal] = (self, terminal)

    def disconnect(self, terminal):
        other, other_terminal = self.connects[terminal]
        self.connects[terminal] = None
        other.connects[other_terminal] = None

class LED(ElectricalObject):
    def __init__(self):
        super().__init__("LED")
        self.on = False

    def update(self):
        anode, _ = self.connects["A"]
        cathode, _ = self.connects["B"]
        if isinstance(anode, Battery) and anode.connects["A"] and isinstance(cathode, Battery) and cathode.connects["B"]:
            self.on = True
        else:
            self.on = False

class Wire(ElectricalObject):
    def __init__(self):
        super().__init__("wire", is_conductive=True)

class Battery(ElectricalObject):
    def __init__(self):
        super().__init__("battery", is_conductive=True)

class TextGame:
    def __init__(self, randomSeed):
        self.random = random.Random(randomSeed)
        self.score = 0
        self.numSteps = 0
        self.gameOver = False
        self.gameWon = False
        self.led = LED()
        self.wire1 = Wire()
        self.wire2 = Wire()
        self.battery = Battery()

    def getTaskDescription(self):
        return "Your task is to light up an LED using a battery and two wires. Connect the battery anode to the LED anode and the battery cathode to the LED cathode."

    def generatePossibleActions(self):
        actions = [
            "look",
            "inventory",
            "examine LED",
            "examine wire",
            "examine battery",
            "take LED",
            "take wire",
            "take battery",
            "connect LED A to battery A",
            "connect LED A to battery B",
            "connect LED B to battery A",
            "connect LED B to battery B",
            "connect LED A to wire A",
            "connect LED A to wire B",
            "connect LED B to wire A",
            "connect LED B to wire B",
            "connect battery A to wire A",
            "connect battery A to wire B",
            "connect battery B to wire A",
            "connect battery B to wire B",
        ]
        return actions

    def step(self, actionStr):
        self.numSteps += 1
        if actionStr == "look":
            return "You are in a workshop with an LED, a battery, and two wires."
        elif actionStr == "inventory":
            return "You have an LED, a battery, and two wires."
        elif actionStr.startswith("examine"):
            item = actionStr.split(" ")[1]
            if item == "LED":
                return "The LED has two terminals: A (anode) and B (cathode)."
            elif item == "wire":
                return "The wire is conductive and has two terminals: A and B."
            elif item == "battery":
                return "The battery has two terminals: A (anode) and B (cathode)."
        elif actionStr.startswith("take"):
            return "You already have all the items in your inventory."
        elif actionStr.startswith("connect"):
            items = actionStr.split(" ")[1:]
            if items == ["LED", "A", "to", "battery", "A"]:
                self.led.connect("A", self.battery, "A")
            elif items == ["LED", "A", "to", "battery", "B"]:
                self.led.connect("A", self.battery, "B")
            elif items == ["LED", "B", "to", "battery", "A"]:
                self.led.connect("B", self.battery, "A")
            elif items == ["LED", "B", "to", "battery", "B"]:
                self.led.connect("B", self.battery, "B")
            elif items == ["LED", "A", "to", "wire", "A"]:
                self.led.connect("A", self.wire1, "A")
            elif items == ["LED", "A", "to", "wire", "B"]:
                self.led.connect("A", self.wire1, "B")
            elif items == ["LED", "B", "to", "wire", "A"]:
                self.led.connect("B", self.wire1, "A")
            elif items == ["LED", "B", "to", "wire", "B"]:
                self.led.connect("B", self.wire1, "B")
            elif items == ["battery", "A", "to", "wire", "A"]:
                self.battery.connect("A", self.wire1, "A")
            elif items == ["battery", "A", "to", "wire", "B"]:
                self.battery.connect("A", self.wire1, "B")
            elif items == ["battery", "B", "to", "wire", "A"]:
                self.battery.connect("B", self.wire1, "A")
            elif items == ["battery", "B", "to", "wire", "B"]:
                self.battery.connect("B", self.wire1, "B")
            else:
                return "Invalid connection."

            self.led.update()
            if self.led.on:
                self.gameOver = True
                self.gameWon = True
                return "You successfully connected the LED and it is now lit!"
            else:
                return "You connected the items, but the LED is not lit yet."
        else:
            return "Invalid action."

    def calculateScore(self):
        if self.gameWon:
            self.score = 1
        else:
            self.score = 0

def main():
    randomSeed = 0
    game = TextGame(randomSeed=randomSeed)

    print("Task Description: " + game.getTaskDescription())
    print("")

    while not game.gameOver:
        actionStr = input("> ")
        observationStr = game.step(actionStr)
        game.calculateScore()

        print("Observation: " + observationStr)
        print("Score: " + str(game.score))
        print("")

if __name__ == "__main__":
    main()
