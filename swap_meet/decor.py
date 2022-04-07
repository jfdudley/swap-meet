from swap_meet.item import Item

class Decor(Item):
    def __init__(self, condition = 0, age = None):
        super().__init__(condition = condition, age = age, category = "Decor")

    def __str__(self):
        return "Something to decorate your space."
