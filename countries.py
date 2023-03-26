class Country(object):
    name = ''
    population = 0
    metallicElements = 0
    timber = 0 
    metallicAlloys = 0
    electronics = 0
    housing = 0
    metallicAlloysWaste = 0
    electronicsWaste = 0
    housingWaste = 0
    water = 0
    availableLand = 0
    potentialEnergyUsable = 0

    def __init__(self, name, population, metallicElements = 0, timber = 0, metallicAlloys = 0, electronics = 0, housing = 0, availableLand = 0, water = 0, potentialEnergyUsable = 0, metallicAlloysWaste = 0, electronicsWaste = 0, housingWaste = 0):
        self.name = name
        self.population = int(population)
        self.metallicElements = int(metallicElements)
        self.timber = int(timber)
        self.metallicAlloys = int(metallicAlloys)
        self.electronics = int(electronics)
        self.housing = int(housing)
        self.metallicAlloysWaste = int(metallicAlloysWaste)
        self.electronicsWaste = int(electronicsWaste)
        self.housingWaste = int(housingWaste)
        self.availableLand = int(availableLand)
        self.water = int(water)
        self.potentialEnergyUsable = int(potentialEnergyUsable)


    def info(self):
        attributes = vars(self)
        for attribute, value in attributes.items():
            print(attribute, "=", value)