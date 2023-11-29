# Task: Create a micro-simulation that models how to add certain amount of water into a pot using a measuring cup.
# Environment: kitchen
# Task-critical Objects: Sink, MeasuringCup, Pot, Water
# High-level object classes: Device (Sink), Container (Sink, MeasuringCup, Pot) 
# Critical properties: volume (Water), max_volume (MeasuringCup, Pot), contained_volume (MeasuringCup, Pot)
# Actions: look, inventory, examine, take/put object, pour liquid into container
# Distractor Items: Pot, MeasuringCup
# Distractor Actions: None
# High-level solution procedure: take measuring cup, put measuring cup in sink, turn on sink, take measuring cup, pour water in measuring cup into pot, repeat till the water in the pot reaches the target volume