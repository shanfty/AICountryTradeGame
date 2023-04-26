# AICountryTradeGame
Artificial Intelligence Country Trading Game Part 1
Taking in an initial state through csv along with the resources and the weights of them. 
Using these weights and initial resources of each country we will search for the best transform to make to better the state quality score.
The state quality score is currently based off bettering the entire world(all countries added together) depending on the input of resource weights.
To run the function just run main.py and make any changes to initialData2.csv or weights2.csv Currently setup to run the 2nd set of initial parameters of countries and resources

State Quality Function
def state_quality(countries, resources):
    resource_dict = {r.name: r for r in resources}
    for country in countries:
        score = 0
        attributes = {attr: getattr(country, attr) for attr in dir(country) if not callable(getattr(country, attr)) and not attr.startswith("__")}
        for attribute, value in attributes.items():
            if attribute in resource_dict:
                score += value * resource_dict[attribute].weight
        return score

Decay Resources Function
def decay_tick(countries, resources):
    resource_dict = {r.name: r for r in resources}
    countryCount = 0
    for country in countries:
        attributes = {attr: getattr(country, attr) for attr in dir(country) if not callable(getattr(country, attr)) and not attr.startswith("__")}
        for attribute, value in attributes.items():
            if attribute in resource_dict:
                setattr(country, attribute, value - (resource_dict[attribute].decayRate))
        countryCount += 1
    return countries

Search Sequence Function
def recursive_apply_transformer(countries, countryId, country, transforms, depth, resources, currScore, transform_sequence=None):
    if transform_sequence is None:
        transform_sequence = []  # initialize the transform sequence if it is not provided
    best_transform_sequence = []
    best_score = currScore
    
    if depth == 0:
        return transform_sequence, currScore

    for transform in transforms:
        new_country = apply_transform_template(country, transform)
        if new_country is None:
            continue
        newCountries = countries
        newCountries[countryId] = new_country
        score = state_quality(newCountries,resources)
        new_transform_sequence  = transform_sequence + [transform]
        new_transform_sequence, score = recursive_apply_transformer(newCountries,countryId,new_country,transforms,depth-1,resources,score, new_transform_sequence)
        if score > currScore:
            best_score = score
            best_transform_sequence = new_transform_sequence
        depth = 3
        new_transform_sequence = []
        transform_sequence = []
    return best_transform_sequence, best_score

def search_best_transform_deeper(countryId, country, countries, transforms, resources, depth=3):
    best_score = state_quality(countries, resources)
    best_transform_sequence = []

    transform_sequence, new_score = recursive_apply_transformer(countries, countryId, country, transforms, depth, resources, best_score)
    if new_score > best_score:
       best_score = new_score
       best_transform_sequence = transform_sequence
    
    return best_transform_sequence


