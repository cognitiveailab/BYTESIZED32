def getReferents(self, curr_room):
    return [f"door to {self.connects[curr_room].name}"]
