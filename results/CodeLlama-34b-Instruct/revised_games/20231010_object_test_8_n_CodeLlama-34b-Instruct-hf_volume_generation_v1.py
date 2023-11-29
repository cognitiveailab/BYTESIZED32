class World:
    def __init__(self):
        self.objects = []

    def add_object(self, obj):
        self.objects.append(obj)

    def get_all_contained_objects_recursive(self):
        return self.objects
