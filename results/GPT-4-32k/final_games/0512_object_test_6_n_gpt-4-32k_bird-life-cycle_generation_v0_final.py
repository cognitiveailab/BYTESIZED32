import random

class ElectricalObject():
    def __init__(self, name, is_conductive):
        self.name = name
        self.is_conductive = is_conductive
        self.connects = []

    def connect(self, other):
        self.connects.append(other)
        other.connects.append(self)

class LED(ElectricalObject):
    def __init__(self):
        super().__init__("LED", True)
        self.on = False

class Wire(ElectricalObject):
    def __init__(self):
        super().__init__("Wire", True)

class Battery(ElectricalObject):
    def __init__(self):
        super().__init__("Battery", True)
        self.anode = ElectricalObject("Anode", True)
        self.cathode = ElectricalObject("Cathode", True)

class TextGame:
    def __init__(self, randomSeed):
        self.random = random.Random(randomSeed)
        self.led = LED()
        self.wire1 = Wire()
        self.wire2 = Wire()
        self.battery = Battery()
        self.inventory = [self.led, self.wire1, self.wire2, self.battery]
        self.score = 0
        self.gameOver = False

    def getTaskDescription(self):
        return "Your task is to connect the LED to the battery using the wires to light it up."

    def generatePossibleActions(self):
        actions = []
        for item1 in self.inventory:
            for item2 in self.inventory:
                if item1 != item2:
                    actions.append(f"connect {item1.name} to {item2.name}")
        return actions

    def step(self, actionStr):
        if not actionStr.startswith("connect"):
            return "Invalid action. Use 'connect X to Y' format."

        items = actionStr.split(" ")[1::2]
        item1_name, item2_name = items

        item1 = None
        item2 = None
        for item in self.inventory:
            if item.name == item1_name:
                item1 = item
            if item.name == item2_name:
                item2 = item

        if item1 is None or item2 is None:
            return "Invalid items. Use items from the inventory."

        if item1.is_conductive and item2.is_conductive:
            item1.connect(item2)

        if self.check_LED_lit():
            self.gameOver = True
            self.score = 100
            return "LED is lit! You have completed the task."
        else:
            return f"{item1.name} is connected to {item2.name}. LED is not lit yet."

    def check_LED_lit(self):
        if self.led in self.battery.anode.connects and self.led in self.battery.cathode.connects:
            for wire in [self.wire1, self.wire2]:
                if wire in self.led.connects and wire in self.battery.anode.connects and wire in self.battery.cathode.connects:
                    return True
        return False

    def calculateScore(self):
        return self.score

def main():
    randomSeed = 0
    game = TextGame(randomSeed=randomSeed)

    print("Task Description: " + game.getTaskDescription())
    print("")

    while not game.gameOver:
        actionStr = input("> ")
        result = game.step(actionStr)
        print(result)
        print("")

    print("Final Score: " + str(game.calculateScore()))

if __name__ == "__main__":
    main()
