class subject():
    def __init__(self, name, tags):
        self.name = name
        self.tags = tags
        self.places = []

    def add_place(self, place):
        self.places.append(place)
