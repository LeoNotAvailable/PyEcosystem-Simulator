class Plant():
    def __init__(self, x, y, quantity):
        self.position= (x, y)
        self.type= "plant"
        self.quantity= quantity

    def grow(self):
        pass

    def reproduce(self):
        pass

    def update_stats(self): # Plants won't be affected by their age, but by any extern condition or illness.
        pass



class Water():
    def __init__(self, x, y, quantity):
        self.position= (x, y)
        self.type= "water"
        self.quantity= quantity