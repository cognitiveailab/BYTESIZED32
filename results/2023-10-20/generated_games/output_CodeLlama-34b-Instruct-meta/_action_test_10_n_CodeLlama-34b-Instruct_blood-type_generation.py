# melting_butter.py
# based on dishwasher.py
# ruoyao wang (feb 20/2023)

# Task: Create a micro-simulation that models how to melt butter
# Environment: room
# Task-critical Objects: Stove, Butter, Pot
# High-level object classes: Device (Stove), Container (Stove, Pot) 
# Critical properties: maxTemperature (Stove), tempIncreasePerTick (Stove), temperature (Butter), stateOfMatter (Butter), solidName/liquidName/gasName (Butter), meltingPoint/boilingPoint (Butter)
# Actions: look, inventory, examine, take/put object, turn on/off, eat butter
# Distractor Items: None
# Distractor Actions: eat butter
# High-level solution procedure: take butter, put butter in pot, take pot, put pot on stove, turn on stove, wait till butter melts

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

    # Game tick: Perform any internal updates that need to be performed at each step of the game.
    def tick(self):
        pass

    # Get a list of referents (i.e. names that this object can be called by)
    def getReferents(self):
        return [self.name]

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return self.name


#
#   Abstract Game-object Classes
#


# Abstract class for things that can be considered 'containers' (e.g. a drawer, a box, a table, a shelf, etc.)
class Container(GameObject):
    def __init__(self, name):
        # Prevent this constructor from running if it's already been run during multiple inheritance
        if hasattr(self, "constructorsRun"):
            if "Container" in self.constructorsRun:
                return

        GameObject.__init__(self, name)
        # Otherwise, mark this constructor as having been run
        self.constructorsRun.append("Container")

        self.properties["isContainer"] = True
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
        return "the " + self.name + "."

# A device that can be turned on and off
class Device(GameObject):
    def __init__(self, name):
        GameObject.__init__(self, name)
        self.properties["isDevice"] = True
        self.properties["isOn"] = False

    # Try to turn the device on
    # Returns an observation string, and a success flag (boolean)
    def turnOn(self):
        # First, check to see if this object is a device
        if not (self.getProperty("isDevice") == True):
            # If not, then it can't be turned on
            return ("The " + self.name + " is not a device, so it can't be turned on.", False)

        # If this object is a device, then check to see if it is already on
        if self.getProperty("isOn"):
            # If so, then it can't be turned on
            return ("The " + self.name + " is already on.", False)

        # If this object is a device and it is off, then turn it on
        self.properties["isOn"] = True
        return ("The " + self.name + " is now on.", True)

    # Try to turn the device off
    # Returns an observation string, and a success flag (boolean)
    def turnOff(self):
        # First, check to see if this object is a device
        if not (self.getProperty("isDevice") == True):
            # If not, then it can't be turned off
            return ("The " + self.name + " is not a device, so it can't be turned off.", False)

        # If this object is a device, then check to see if it is already off
        if not (self.getProperty("isOn") == True):
            # If so, then it can't be turned off
            return ("The " + self.name + " is already off.", False)

        # If this object is a device and it is on, then turn it off
        self.properties["isOn"] = False
        return ("The " + self.name + " is now off.", True)

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A container that can hold liquids
class LiquidContainer(Container):
    def __init__(self, name):
        Container.__init__(self, name)
        self.properties["isLiquidContainer"] = True
        self.properties["liquidName"] = "liquid"

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + " containing " + self.properties["liquidName"] + "."

# A container that can hold solids
class SolidContainer(Container):
    def __init__(self, name):
        Container.__init__(self, name)
        self.properties["isSolidContainer"] = True
        self.properties["solidName"] = "solid"

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + " containing " + self.properties["solidName"] + "."

# A container that can hold gases
class GasContainer(Container):
    def __init__(self, name):
        Container.__init__(self, name)
        self.properties["isGasContainer"] = True
        self.properties["gasName"] = "gas"

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + " containing " + self.properties["gasName"] + "."

# A device that can heat up liquids
class HeatingDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isHeatingDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can cool down liquids
class CoolingDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isCoolingDevice"] = True
        self.properties["maxTemperature"] = -100
        self.properties["tempIncreasePerTick"] = -10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can melt solids
class MeltingDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isMeltingDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can boil liquids
class BoilingDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isBoilingDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can freeze liquids
class FreezingDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isFreezingDevice"] = True
        self.properties["maxTemperature"] = -100
        self.properties["tempIncreasePerTick"] = -10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can vaporize liquids
class VaporizingDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isVaporizingDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can condensate liquids
class CondensingDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isCondensingDevice"] = True
        self.properties["maxTemperature"] = -100
        self.properties["tempIncreasePerTick"] = -10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can sublimate solids
class SublimatingDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isSublimatingDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can deposit solids
class DepositingDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isDepositingDevice"] = True
        self.properties["maxTemperature"] = -100
        self.properties["tempIncreasePerTick"] = -10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can ionize gases
class IonizingDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isIonizingDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can neutralize gases
class NeutralizingDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isNeutralizingDevice"] = True
        self.properties["maxTemperature"] = -100
        self.properties["tempIncreasePerTick"] = -10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a vacuum
class VacuumDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isVacuumDevice"] = True
        self.properties["maxTemperature"] = -100
        self.properties["tempIncreasePerTick"] = -10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a pressure
class PressureDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isPressureDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a magnetic field
class MagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isMagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a gravitational field
class GravitationalDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isGravitationalDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def makeDescriptionStr(self, makeDetailed=False):
        return "the " + self.name + "."

# A device that can create a electromagnetic field
class ElectromagneticDevice(Device):
    def __init__(self, name):
        Device.__init__(self, name)
        self.properties["isElectromagneticDevice"] = True
        self.properties["maxTemperature"] = 100
        self.properties["tempIncreasePerTick"] = 10

    # Make a human-readable string that describes this object
    def make
