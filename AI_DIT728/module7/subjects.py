"""
This is how the data is stored, a quite simple implementation that lets us store
names and tags for subject and add places to subjects
"""


class subject():
    def __init__(self, name, tags):
        self.name = name
        self.tags = tags
        self.places = []

    def add_place(self, place):
        self.places.append(place)


class place():
    def __init__(self, name, tags, price, opening, closing):
        self.name = name
        self.tags = tags
        self.price = price
        self.opening_time = opening
        self.closing_time = closing
