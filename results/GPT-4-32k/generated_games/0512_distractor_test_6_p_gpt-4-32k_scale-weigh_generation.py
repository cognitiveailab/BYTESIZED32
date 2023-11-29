import random

class ElectricalObject():
    def __init__(self, name):
        self.name = name
        self.connects = []
        self.is_conductive = True

    def connect(self, other):
        self.connects.append(other)
        other.connects.append(self)

class LED(ElectricalObject):
    def __init__(self):
        super().__init__("LED")
        self.on = False

class Wire(ElectricalObject):
    def __init__(self):
        super().__init__("Wire")

class Battery(ElectricalObject):
    def __init__(self):
        super().__init__("Battery")
        self.anode = ElectricalObject("Anode")
        self.cathode = ElectricalObject("Cathode")

class TextGame:
    def __init__(self, randomSeed):
        self.random = random.Random(randomSeed)
        self.led = LED()
        self.wire1 = Wire()
        self.wire2 = Wire()
        self.battery = Battery()
        self.score = 0

    def getTaskDescription(self):
        return "Your task is to light up the LED using the battery and wires."

    def generatePossibleActions(self):
        return [
            "look",
            "inventory",
            "examine",
            f"take {self.wire1.name}",
            f"take {self.wire2.name}",
            f"connect {self.battery.anode.name} to {self.led.name} anode with {self.wire1.name}",
            f"connect {self.battery.cathode.name} to {self.led.name} cathode with {self.wire2.name}",
        ]

    def step(self, actionStr):
        if actionStr == f"connect {self.battery.anode.name} to {self.led.name} anode with {self.wire1.name}":
            self.battery.anode.connect(self.led)
            self.led.connect(self.wire1)
            self.wire1.connect(self.battery.anode)
            return "Connected battery anode to LED anode with a wire."
        elif actionStr == f"connect {self.battery.cathode.name} to {self.led.name} cathode with {self.wire2.name}":
            self.battery.cathode.connect(self.led)
            self.led.connect(self.wire2)
            self.wire2.connect(self.battery.cathode)
            return "Connected battery cathode to LED cathode with a wire."
        else:
            return "Invalid action."

    def calculateScore(self):
        if self.battery.anode in self.led.connects and self.battery.cathode in self.led.connects:
            self.led.on = True
            self.score = 1
        else:
            self.led.on = False
            self.score = 0
        return self.score

def main():
    game = TextGame(randomSeed=1)
    print(game.getTaskDescription())

    while True:
        action = input("> ")
        if action == "exit" or action == "quit":
            break

        print(game.step(action))
        print("LED is on:", game.led.on)
        print("Score:", game.calculateScore())

if __name__ == "__main__":
    main()
