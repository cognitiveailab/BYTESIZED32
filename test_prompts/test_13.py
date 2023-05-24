# Task: Create a micro-simulation that models how to find keys, use keys to open doors to go to another room and collect a coin
# Environment: house
# Task-critical Objects: Room, Door, Key, Drawer, Coin
# High-level object classes: Container (Room, Drawer)
# Critical properties: connects (Room), is_locked (Door), is_open (Door), key (Door)
# Actions: look, inventory, examine, take/put object, open/close container, open/close door, unlock door with key, move to room
# Distractor Items: Key, Room, Door
# Distractor Actions: None
# High-level solution procedure: find the keys and open corresponding doors, move to the coin room and take coin.