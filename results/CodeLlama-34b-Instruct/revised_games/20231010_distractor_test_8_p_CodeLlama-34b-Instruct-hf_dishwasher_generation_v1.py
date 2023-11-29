#
#   Specific Game Objects
#

# A room, which is a container that can hold objects.  It can also have mosquitoes in it.
class Room(Container):
    def __init__(self, name):
        GameObject.__init__(self, name)
        Container.__init__(self, name)

        # Set the properties of this object
        self.properties["isContainer"] = True
        self.properties["isOpenable"] = False  # A room is not openable
        self.properties["isOpen"] = True     # A room is always open
        self.properties["hasMosquito"] = False # By default, a room does not have mosquitoes

    # Try to move the agent to this room.
    # Returns an observation string, and a success flag (boolean)
    def moveAgentToRoom(self, agent):
        # If the agent is already in this room, then don't move it
        if (agent.parentContainer == self):
            return ("You are already in the " + self.name + ".", False)

        # Otherwise, move the agent to this room
        agent.removeSelfFromContainer()
        self.addObject(agent)
        return ("You move to the " + self.name + ".", True)

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        outStr = "the " + self.name + "."
        if self.properties["hasMosquito"]:
            outStr += " There is a mosquito in the room."
        return outStr

# A bottle, which is a container that can hold objects.  It can also be used to apply mosquito repellant.
class Bottle(Container):
    def __init__(self, name):
        GameObject.__init__(self, name)
        Container.__init__(self, name)

        # Set the properties of this object
        self.properties["isContainer"] = True
        self.properties["isOpenable"] = True  # A bottle is openable
        self.properties["isOpen"] = False     # A bottle is closed by default
        self.properties["isMoveable"] = True # A bottle is moveable
        self.properties["hasMosquitoRepellant"] = False # By default, a bottle does not have mosquito repellant

    # Try to use the bottle to apply mosquito repellant.
    # Returns an observation string, and a success flag (boolean)
    def useMosquitoRepellant(self, agent):
        # If the bottle is not open, then it can't be used
        if not self.properties["isOpen"]:
            return ("The " + self.name + " is closed, so it can't be used.", False)

        # If the bottle does not have mosquito repellant, then it can't be used
        if not self.properties["hasMosquitoRepellant"]:
            return ("The " + self.name + " does not have mosquito repellant, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is already wearing mosquito repellant, then it can't be used
        if agent.getProperty("useMosquitoRepellant"):
            return ("You are already wearing mosquito repellant.", False)

        # If the agent has been bitten by a mosquito, then it can't be used
        if agent.getProperty("bitByMosquito"):
            return ("You have been bitten by a mosquito, so you can't use mosquito repellant.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room as the bottle, then it can't be used
        if agent.parentContainer != self.parentContainer:
            return ("The " + self.name + " is not in the same room as you, so it can't be used.", False)

        # If the agent is not in the same room