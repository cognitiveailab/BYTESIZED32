# Task: Create a micro-simulation that models how to melt butter
# Environment: room
# Task-critical Objects: Stove, Butter, Pot
# High-level object classes: Device (Stove), Container (Stove, Pot) 
# Critical properties: maxTemperature (Stove), tempIncreasePerTick (Stove), temperature (Butter), stateOfMatter (Butter), solidName/liquidName/gasName (Butter), meltingPoint/boilingPoint (Butter)
# Actions: look, inventory, examine, take/put object, turn on/off, eat butter
# Distractor Items: None
# Distractor Actions: eat butter
# High-level solution procedure: take butter, put butter in pot, take pot, put pot on stove, turn on stove, wait till butter melts
