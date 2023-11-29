class Fork(GameObject):
    def __init__(self, name, conductive=False):
        GameObject.__init__(self, name)
        self.properties["is_fork"] = True
        self.properties["conductive"] = conductive
