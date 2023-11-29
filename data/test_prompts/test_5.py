# Task: Create a micro-simulation that models how to open a box whose cover is fixed by screws with a screwdriver.
# Environment: room
# Task-critical Objects: Screw, Screwdriver, Box, Coin
# High-level object classes: Container (Box)
# Critical properties: is_open (Box), is_openable (Box)
# Actions: look, inventory, examine, take/put object, screw/unscrew screw with screwdriver, open/close container
# Distractor Items: Hammer
# Distractor Actions: None
# High-level solution procedure: take screwdriver, unscrew all screws, open box, take coin, put coin in answer box