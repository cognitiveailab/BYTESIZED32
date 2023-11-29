    # Pour liquid from one container to another
    def actionPour(self, liquid, container1, container2, container3):
        # Check that the first container is a container
        if (container1.getProperty("isContainer") == False):
            return "You can't pour from the " + container1.getReferents()[0] + "."

        # Check that the second container is a container
        if (container2.getProperty("isContainer") == False):
            return "You can't pour into the " + container2.getReferents()[0] + "."

        # Check that the third container is a container
        if (container3.getProperty("isContainer") == False):
            return "You can't pour into the " + container3.getReferents()[0] + "."

        # Enforce that the liquid must be in the inventory to do anything with it
        if (liquid.parent != self.agent):
            return "You don't currently have the " + liquid.getReferents()[0] + " in your inventory."

        # Take the liquid from the inventory
        obsStr1, objRef, success = liquid.parent.takeObjectFromContainer(liquid)
        if (success == False):
            return obsStr1

        # Pour the liquid from the first container to the second container
        obsStr2, success = container1.removeLiquid(liquid)
        if (success == False):
            # For whatever reason, the liquid can't be removed from the first container. Put the liquid back into the inventory
            self.agent.addObject(liquid)
            return obsStr2

        # Put the liquid in the second container
        obsStr3, success = container2.addLiquid(liquid)
        if (success == False):
            # For whatever reason, the liquid can't be added to the second container. Remove the liquid from the first container and put it back into the inventory
            container1.addObject(liquid)
            return obsStr3

        # Success -- show all observations
        return obsStr1 + "\n" + obsStr2 + "\n" + obsStr3
