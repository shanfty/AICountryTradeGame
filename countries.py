class Country(object):
    name = ''
    population = 0
    metallicElements = 0
    timber = 0 
    metallicAlloys = 0
    electronics = 0
    housing = 0
    metallicAlloyWaste = 0
    electronicWaste = 0
    housingWaste = 0

    def __init__(self, name, population, metallicElements, timber, metallicAlloys, electronics, housing, metallicAlloyWaste = 0, electronicWaste = 0, housingWaste = 0):
        self.name = name
        self.population = int(population)
        self.metallicElements = int(metallicElements)
        self.timber = int(timber)
        self.metallicAlloys = int(metallicAlloys)
        self.electronics = int(electronics)
        self.housing = int(housing)
        self.metallicAlloyWaste = int(metallicAlloyWaste)
        self.electronicWaste = int(electronicWaste)
        self.housingWaste = int(housingWaste)
    
    def info(self):
        attributes = vars(self)
        for attribute, value in attributes.items():
            print(attribute, "=", value)