    def actionInventory(self):
        # Display the agent's inventory
        inventoryStr = "You are carrying: \n"
        for obj in self.agent.contains:
            inventoryStr += "\t" + obj.makeDescriptionStr() + "\n"
        return inventoryStr
