def tick(self):
    output_str = None
    # increase the temperature of the device
    if self.properties["temperature_increase_per_tick"] is not None:
        self.properties["temperature"] += self.properties["temperature_increase_per_tick"]
    # if the temperature reaches the maximum temperature, turn off the device
    if self.properties["temperature"] >= self.properties["max_temperature"]:
        self.properties["temperature"] = self.properties["max_temperature"]
        output_str = "The " + self.name + " is turned off."
    return output_str
