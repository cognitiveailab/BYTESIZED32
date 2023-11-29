    def actionUnlock(self, door, key):
        # Check to make sure the door is a door
        if (door.getProperty("is_door") == False):
            return "You can't unlock the " + door.getReferents()[0] + "."

        # Check to make sure the key is a key
        if (key.getProperty("is_key") == False):
            return "You can't unlock the " + door.getReferents()[0] + " with the " + key.getReferents()[0] + "."

        # Unlock the door
        obsStr, success = door.unlockDoor(key)
        if (success == False):
            return obsStr

        return obsStr
