# Task: Create a micro-simulation that models how to measure the density of a stone
# Environment: room
# Task-critical Objects: Stone, MeasuringCup, Scale, Sink, Water
# High-level object classes: Container (MeasuringCup, Sink)
# Critical properties: water_out_per_tick (Sink), volume (Water, MeasuringCup, Stone), containedVolume (MeasuringCup), containsLiquid (MeasuringCup), weight (Stone, MeasuringCup, Water)
# Actions: look, inventory, examine, take/put object, turn on/off, answer
# Distractor Items: Stone
# Distractor Actions: None
# High-level solution procedure: take stone, put stone on scale, look, take measuring cup, put measuring cup in sink, turn on sink, turn off sink, look, take stone, put stone in measuring cup, look, answer