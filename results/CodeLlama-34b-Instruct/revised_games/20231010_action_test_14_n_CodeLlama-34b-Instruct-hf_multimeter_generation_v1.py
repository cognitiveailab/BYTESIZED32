class TextGame:
    # ...

    def actionInventory(self):
        inventoryStr = "You are carrying: "
        for obj in self.agent.contains:
            inventoryStr += "\n\t" + obj.makeDescriptionStr()
        return inventoryStr

    # ...
