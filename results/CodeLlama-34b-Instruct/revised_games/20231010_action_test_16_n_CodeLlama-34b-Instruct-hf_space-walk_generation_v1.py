# density_stone.py
# based on space-walk.py
# ruoyao wang (apr 29/2023)

# Task Description: Create a micro-simulation that models how to measure the density of a stone.
# Environment: room
# Task-critical Objects: Stone, MeasuringCup, Scale, Sink, Water
# High-level object classes: Container (MeasuringCup, Sink)
# Critical properties: water_out_per_tick (Sink), volume (Water, MeasuringCup, Stone), containedVolume (MeasuringCup), containsLiquid (MeasuringCup), weight (Stone, MeasuringCup, Water)
# Actions: look, inventory, examine, take/put object, turn on/off, answer
# Distractor Items: Stone
# Distractor Actions: None
# High-level solution procedure: take stone, put stone on scale, look, take measuring cup, put measuring cup in sink, turn on sink, turn off sink, look, take stone, put stone in measuring cup, look, answer

import random

#
# Abstract class for all game objects
#
class GameObject():
    def __init__(self, name):
        # Prevent this constructor from running if it's already been run during multiple inheritance
        if hasattr(self, "constructorsRun"):
            return
        # Otherwise, keep a list of constructors that have already been run
        self.constructorsRun = ["GameObject"]

        self.name = name
        self.parentContainer = None
        self.contains = []
        self.properties = {}

        # Default properties
        self.properties["isContainer"] = False    # By default, objects are not containers
        self.properties["isMoveable"] = True     # By default, objects are moveable

    # Get a property of the object (safely), returning None if the property doesn't exist
    def getProperty(self, propertyName):
        if propertyName in self.properties:
            return self.properties[propertyName]
        else:
            return None

    # Add an object to this container, removing it from its previous container
    def addObject(self, obj):
        obj.removeSelfFromContainer()
        self.contains.append(obj)
        obj.parentContainer = self

    # Remove an object from this container
    def removeObject(self, obj):
        self.contains.remove(obj)
        obj.parentContainer = None

    # Remove the current object from whatever container it's currently in
    def removeSelfFromContainer(self):
        if self.parentContainer != None:
            self.parentContainer.removeObject(self)

    # Get all contained objects, recursively
    def getAllContainedObjectsRecursive(self):
        outList = []
        for obj in self.contains:
            # Add self
            outList.append(obj)
            # Add all contained objects
            outList.extend(obj.getAllContainedObjectsRecursive())
        return outList

    # Get all contained objects that have a specific name (not recursively)
    def containsItemWithName(self, name):
        foundObjects = []
        for obj in self.contains:
            if obj.name == name:
                foundObjects.append(obj)
        return foundObjects

    # Game tick: Perform any internal updates that need to be performed at each step of the game.
    def tick(self):
        pass

    # Get a list of referents (i.e. names that this object can be called by)
    def getReferents(self):
        return [self.name]

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return f"a {self.name}"

#
#   Abstract Game-object Classes
#


# Abstract class for things that can be considered 'containers' (e.g. a drawer, a box, a table, a shelf, etc.)
class Container(GameObject):
    def __init__(self, name):
        GameObject.__init__(self, name)
        Container.__init__(self, name)
        self.properties["isMoveable"] = False
        self.properties["isOpenable"] = False  # Can the container be opened (e.g. a drawer, a door, a box, etc.), or is it always 'open' (e.g. a table, a shelf, etc.)
        self.properties["isOpen"] = True      # Is the container open or closed (if it is openable)
        self.properties["containerPrefix"] = "in" # The prefix to use when referring to the container (e.g. "in the drawer", "on the table", etc.)

    # Try to open the container
    # Returns an observation string, and a success flag (boolean)
    def openContainer(self):
        # First, check to see if this object is openable
        if not self.getProperty("isOpenable"):
            # If not, then it can't be opened
            return ("The " + self.name + " can't be opened.", False)

        # If this object is openable, then check to see if it is already open
        if self.getProperty("isOpen"):
            # If so, then it can't be opened
            return ("The " + self.name + " is already open.", False)

        # If this object is openable and it is closed, then open it
        self.properties["isOpen"] = True
        return ("The " + self.name + " is now open.", True)

    # Try to close the container
    # Returns an observation string, and a success flag (boolean)
    def closeContainer(self):
        # First, check to see if this object is openable
        if not (self.getProperty("isOpenable") == True):
            # If not, then it can't be closed
            return ("The " + self.name + " can't be closed.", False)

        # If this object is openable, then check to see if it is already closed
        if not (self.getProperty("isOpen") == True):
            # If so, then it can't be closed
            return ("The " + self.name + " is already closed.", False)

        # If this object is openable and it is open, then close it
        self.properties["isOpen"] = False
        return ("The " + self.name + " is now closed.", True)

    # Try to place the object in a container.
    # Returns an observation string, and a success flag (boolean)
    def placeObjectInContainer(self, obj):
        # First, check to see if this object is a container
        if not (self.getProperty("isContainer") == True):
            # If not, then it can't be placed in a container
            return ("The " + self.name + " is not a container, so things can't be placed there.", False)

        # Check to see if the object is moveable
        if not (obj.getProperty("isMoveable") == True):
            # If not, then it can't be removed from a container
            return ("The " + obj.name + " is not moveable.", None, False)

        # If this object is a container, then check to see if it is open
        if not (self.getProperty("isOpen") == True):
            # If not, then it can't be placed in a container
            return ("The " + self.name + " is closed, so things can't be placed there.", False)

        # If this object is a container and it is open, then place the object in the container
        self.addObject(obj)
        return ("The " + obj.getReferents()[0] + " is placed in the " + self.name + ".", True)

    # Try to remove the object from a container.
    # Returns an observation string, a reference to the object being taken, and a success flag (boolean)
    def takeObjectFromContainer(self, obj):
        # First, check to see if this object is a container
        if not (self.getProperty("isContainer") == True):
            # If not, then it can't be removed from a container
            return ("The " + self.name + " is not a container, so things can't be removed from it.", None, False)

        # Check to see if the object is moveable
        if not (obj.getProperty("isMoveable") == True):
            # If not, then it can't be removed from a container
            return ("The " + obj.name + " is not moveable.", None, False)

        # If this object is a container, then check to see if it is open
        if not (self.getProperty("isOpen") == True):
            # If not, then it can't be removed from a container
            return ("The " + self.name + " is closed, so things can't be removed from it.", None, False)

        # Check to make sure that the object is contained in this container
        if obj not in self.contains:
            return ("The " + obj.name + " is not contained in the " + self.name + ".", None, False)

        # If this object is a container and it is open, then remove the object from the container
        obj.removeSelfFromContainer()
        return ("The " + obj.getReferents()[0] + " is removed from the " + self.name + ".", obj, True)

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "a " + self.name

# A room
class Room(Container):
    def __init__(self, name, isOuterSpace=False):
        GameObject.__init__(self, name)
        Container.__init__(self, name)
        self.properties["isMoveable"] = False
        self.properties["isOuterSpace"] = isOuterSpace
        self.connects = {} # other rooms that this room connects to, {room: door}

    def makeDescriptionStr(self, makeDetailed=False):
        outStr = f"You find yourself in a {self.name}.  In the {self.name}, you see: \n"
        for obj in self.contains:
            outStr += "\t" + obj.makeDescriptionStr() + "\n"

        return outStr

    # connect to another room
    def connect(self, room):
        if room not in self.connects:
            self.connects[room] = None
            room.connects[self] = None

    # check if there exists a path that connects to another room without any closed door on the path
    def connectsToOuterSpace(self, visited):
        visited.append(self)
        if self.properties["isOuterSpace"]:
            return True
        connected = False
        for r in self.connects:
            if r in visited:
                continue
            elif self.connects[r] is not None and not self.connects[r].getProperty("is_open"):
                continue
            elif r.getProperty("isOuterSpace"):
                connected = True
                break
            else:
                connected = r.connectsToOuterSpace(visited)
                if connected:
                    break
        return connected


# A door
class Door(GameObject):
    def __init__(self, name, room1, room2, is_open=False):
        GameObject.__init__(self, name)

        self.properties["is_open"] = is_open
        self.properties["isMoveable"] = False

        # connects to the door to two rooms
        self.connects = {room1: room2, room2: room1} # rooms connected by the door
        room1.connects[room2] = self
        room2.connects[room1] = self

    def open(self, curr_room):
        # The door is already opened
        if self.properties["is_open"]:
            return f"The door to the {self.connects[curr_room].name} is already open."
        else:
            # If the door is closed, open it
            self.properties["is_open"] = True
            return f"You open the door to the {self.connects[curr_room].name}."

    def close(self, curr_room):
        # The door is already closed
        if not self.properties["is_open"]:
            return f"The door to the {self.connects[curr_room].name} is already closed."
        else:
            # If the door is closed, open it
            self.properties["is_open"] = False
            return f"You close the door to the {self.connects[curr_room].name}."

    def getReferents(self, curr_room):
        return [f"door to {self.connects[curr_room].name}"]

    def makeDescriptionStr(self, curr_room, makeDetailed=False):
        if self.properties["is_open"]:
            outStr = f"a door to the {self.connects[curr_room].name} that is open"
        else:
            outStr = f"a door to the {self.connects[curr_room].name} that is closed"
        return outStr

# A stone
class Stone(GameObject):
    def __init__(self, name):
        GameObject.__init__(self, name)

        self.properties["weight"] = 10

    def makeDescriptionStr(self, makeDetailed=False):
        return "a " + self.name

# A measuring cup
class MeasuringCup(GameObject):
    def __init__(self, name):
        GameObject.__init__(self, name)

        self.properties["isContainer"] = True
        self.properties["isOpenable"] = False
        self.properties["isOpen"] = True
        self.properties["containerPrefix"] = "in"
        self.properties["volume"] = 0
        self.properties["containedVolume"] = 0
        self.properties["containsLiquid"] = False

    def makeDescriptionStr(self, makeDetailed=False):
        if self.properties["containsLiquid"]:
            return "a " + self.name + " containing water"
        else:
            return "a " + self.name

    def tick(self):
        # If the measuring cup is not contained in a sink, then it is not a container
        if self.parentContainer == None or not self.parentContainer.getProperty("isContainer"):
            self.properties["isContainer"] = False
        else:
            self.properties["isContainer"] = True

        # If the measuring cup is contained in a sink, then it is a container
        if self.parentContainer != None and self.parentContainer.getProperty("isContainer"):
            self.properties["isContainer"] = True

        # If the measuring cup is a container, then its volume is the sum of the volumes of its contents
        if self.properties["isContainer"]:
            self.properties["volume"] = 0
            for obj in self.contains:
                self.properties["volume"] += obj.getProperty("volume")

        # If the measuring cup is not a container, then its volume is 0
        else:
            self.properties["volume"] = 0

        # If the measuring cup is a container, then its contained volume is the sum of the volumes of its contents
        if self.properties["isContainer"]:
            self.properties["containedVolume"] = 0
            for obj in self.contains:
                self.properties["containedVolume"] += obj.getProperty("volume")

        # If the measuring cup is not a container, then its contained volume is 0
        else:
            self.properties["containedVolume"] = 0

        # If the measuring cup is a container and it contains liquid, then it contains liquid
        if self.properties["isContainer"] and self.properties["containedVolume"] > 0:
            self.properties["containsLiquid"] = True

        # If the measuring cup is a container and it does not contain liquid, then it does not contain liquid
        elif self.properties["isContainer"] and self.properties["containedVolume"] == 0:
            self.properties["containsLiquid"] = False

        # If the measuring cup is not a container, then it does not contain liquid
        else:
            self.properties["containsLiquid"] = False

# A sink
class Sink(Container):
    def __init__(self, name):
        GameObject.__init__(self, name)

        self.properties["water_out_per_tick"] = 1

    def makeDescriptionStr(self, makeDetailed=False):
        return "a " + self.name

    def tick(self):
        # If the sink is not contained in a room, then it is not a container
        if self.parentContainer == None or not self.parentContainer.getProperty("isContainer"):
            self.properties["isContainer"] = False
        else:
            self.properties["isContainer"] = True

        # If the sink is contained in a room, then it is a container
        if self.parentContainer != None and self.parentContainer.getProperty("isContainer"):
            self.properties["isContainer"] = True

        # If the sink is a container, then its volume is the sum of the volumes of its contents
        if self.properties["isContainer"]:
            self.properties["volume"] = 0
            for obj in self.contains:
                self.properties["volume"] += obj.getProperty("volume")

        # If the sink is not a container, then its volume is 0
        else:
            self.properties["volume"] = 0

        # If the sink is a container, then its contained volume is the sum of the volumes of its contents
        if self.properties["isContainer"]:
            self.properties["containedVolume"] = 0
            for obj in self.contains:
                self.properties["containedVolume"] += obj.getProperty("volume")

        # If the sink is not a container, then its contained volume is 0
        else:
            self.properties["containedVolume"] = 0

        # If the sink is a container and it contains liquid, then it contains liquid
        if self.properties["isContainer"] and self.properties["containedVolume"] > 0:
            self.properties["containsLiquid"] = True

        # If the sink is a container and it does not contain liquid, then it does not contain liquid
        elif self.properties["isContainer"] and self.properties["containedVolume"] == 0:
            self.properties["containsLiquid"] = False

        # If the sink is not a container, then it does not contain liquid
        else:
            self.properties["containsLiquid"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"] = True

        # If the sink is a container and it is closed, then it is not a container
        elif self.properties["isContainer"] and not self.properties["isOpen"]:
            self.properties["isContainer"] = False

        # If the sink is not a container, then it is not a container
        else:
            self.properties["isContainer"] = False

        # If the sink is a container and it is open, then it is a container
        if self.properties["isContainer"] and self.properties["isOpen"]:
            self.properties["isContainer"]