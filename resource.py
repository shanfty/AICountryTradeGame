class Resource(object):
    name = ''
    weight = 0

    def __init__(self, name, weight):
        self.name = name
        self.weight = float(weight)

    def info(self):
        attributes = vars(self)
        for attribute, value in attributes.items():
            print(attribute, "=", value)