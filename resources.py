class Resource(object):
    name = ''
    weight = 0
    decayRate = 0

    def __init__(self, name, weight, decayRate):
        self.name = name
        self.weight = float(weight)
        self.decayRate = float(decayRate)

    def info(self):
        attributes = vars(self)
        for attribute, value in attributes.items():
            print(attribute, "=", value)