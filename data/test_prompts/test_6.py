# Task: Create a micro-simulation that models how to lit an LED.
# Environment: workshop
# Task-critical Objects: LED, Wire, Battery
# High-level object classes: ElectricalObject (LED, Wire, Battery)
# Critical properties: connects (ElectricalObject), is_conductive (ElectricalObject), on (LED)
# Actions: look, inventory, examine, take/put object, connect X terminal A to Y terminal B
# Distractor Items: ElectricalObject
# Distractor Actions: None
# High-level solution procedure: connect battery anode to LED anode with a wire, connect battery cathode to LED cathode with a wire