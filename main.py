from asyncore import read
from contextlib import redirect_stdout
from typing import List
from dataclasses import dataclass, field
from collections import deque
import os
import re
import csv

from countries import Country
from resources import Resource


@dataclass
class ResourceQuantity:
  name: str = field()
  quantity: int = field()

@dataclass
class TransformTemplate:
  name: str = field(default="")
  inputs: List[ResourceQuantity] = field(default_factory=list)
  outputs: List[ResourceQuantity] = field(default_factory=list)

def read_file(file_path: str) -> List[dict]:
  file_contents = None
  with open(file_path, mode='r') as file:
    file_contents = file.read()
  return file_contents

def validate_nonempty(template: str = "") -> bool:
  return template != ""

def validate_enclosed(template: str = "") -> bool:
  left_paren_count = template.count("(")
  right_paren_count = template.count(")")
  if left_paren_count != right_paren_count:
    return False
  return True

def validate_keywords(template: str = "") -> bool:
  transform_keywords = ["TRANSFORM", "INPUTS", "OUTPUTS"]
  for keyword in transform_keywords:
    if not keyword in template:
      return False
  return True

def validate(template: str = ""):
  if not validate_nonempty(template):
    raise Exception("Empty template")
  if not validate_enclosed(template):
    raise Exception("Incorrect parentheses counts, verify all expressions are properly enclosed")
  elif not validate_keywords(template):
    raise Exception("Missing required keywords, verify transform is syntactically correct")

def build_resource_quantities(resource_quantities_block):
  quantities = []

  regex = r"\(([A-Za-z]+) (\d)\)"
  matches = re.finditer(regex, resource_quantities_block, re.MULTILINE)
  for match in matches:
      resource_name, resource_quantity = match.groups()
      quantities.append(ResourceQuantity(name=resource_name, quantity=int(resource_quantity)))

  return quantities

def build_transform_template(template_path: str, template: str) -> TransformTemplate:
  transform = TransformTemplate()
  
  basename = os.path.basename(template_path)
  transform_name = os.path.splitext(basename)[0]
  transform.name = transform_name

  inputs_start = template.index("INPUTS")
  outputs_start = template.index("OUTPUTS")

  inputs_string = template[inputs_start:outputs_start]
  outputs_string = template[outputs_start:]

  transform.inputs = build_resource_quantities(inputs_string)
  transform.outputs = build_resource_quantities(outputs_string)

  return transform

def parse(template_path: str) -> TransformTemplate:
  template = read_file(template_path)
  validate(template)
  transform_template = build_transform_template(template_path, template)
  return transform_template

def read_csv(file_path: str) -> List[dict]:
  entries = []
  with open(file_path, mode='r') as file:
    csvFile = csv.DictReader(file)

    for entry in csvFile:
      entries.append(entry)
  
  return entries

def state_quality(countries, resources):
    resource_dict = {r.name: r for r in resources}
    for country in countries:
        score = 0
        attributes = {attr: getattr(country, attr) for attr in dir(country) if not callable(getattr(country, attr)) and not attr.startswith("__")}
        for attribute, value in attributes.items():
            if attribute in resource_dict:
                score += value * resource_dict[attribute].weight
        return score

def apply_transform_template(country: Country, template: TransformTemplate) -> None:
    newCountry = country
    for input_resource in template.inputs:
        if input_resource.name == 'Population':
            continue 
        if getattr(newCountry, input_resource.name) < input_resource.quantity:
            return None
    
    for input_resource in template.inputs:
        if input_resource.name == 'Population':
            continue
        setattr(newCountry, input_resource.name, getattr(newCountry, input_resource.name) - input_resource.quantity)
    
    for output_resource in template.outputs:
        setattr(newCountry, output_resource.name, getattr(newCountry, output_resource.name) + output_resource.quantity)

    return newCountry


def search_best_transform(countries, transforms, resources):
        best_score = state_quality(countries, resources)
        best_transform = None
        best_country = None

        for transform in transforms:
            count = 0
            for country in countries:
                new_country = apply_transform_template(country, transform)
                if(new_country == None):
                    continue

                copyCountries = countries
                copyCountries[count] = new_country
                new_score = state_quality(copyCountries, resources)

                if new_score > best_score:
                    best_score = new_score
                    best_transform = transform
                    best_country = count
                count += 1
                
        return best_transform,best_country


def main():
    resourceCSV = read_csv("weights.csv")
    resources = []
    for resource_data in resourceCSV:
        resource = Resource(resource_data['Resource'], resource_data['Weight'])
        resources.append(resource)

    for each in resources:
        each.info()
    print("\n")

    countries = []
    with open ('initialData.csv') as initialData:
        reader = csv.reader(initialData)
        next(reader)
    
        for country_data in reader:
            country = Country(*country_data)
            countries.append(country)

    i = 0
    for each in countries:
        print("Country " + str(i))
        each.info()
        print("\n")
        i += 1

    start_score = state_quality(countries, resources)
    
    templates = []

    alloysPath="./transforms/alloys.tmpl"
    alloysTemplate = parse(alloysPath)
    templates.append(alloysTemplate)

    housingPath="./transforms/housing.tmpl"
    housingTemplate = parse(housingPath)
    templates.append(housingTemplate)

    electronicsPath="./transforms/electronics.tmpl"
    electronicsTemplate = parse(electronicsPath)
    templates.append(electronicsTemplate)

    f = open("output.txt","w")
    f.write('Output File')

    i = 0
    for each in countries:
        f.write("\nStarting Country:" + str(i) + ", ")
        attributes = vars(each)
        for attribute, value in attributes.items():
            f.write(attribute + "=" + str(value)+ ", ")
        i += 1

    best_transform, best_country = search_best_transform(countries,templates,resources)
    transformIndex = 0

    while(best_transform != None):
        best_transform, best_country = search_best_transform(countries,templates,resources)
        if(best_transform != None):
            apply_transform_template(countries[best_country], best_transform)
            transformIndex += 1
            f.write("\nTransform: " + str(transformIndex) + ", " + countries[best_country].name + ": " + best_transform.name)

    i = 0
    for each in countries:
        f.write("\nEnding Country " + str(i) + ", ")
        attributes = vars(each)
        for attribute, value in attributes.items():
            f.write(attribute + "=" + str(value) + ", ")
        i += 1

    end_score = state_quality(countries,resources)

    f.write("\nTransforms made: " + str(transformIndex))
    f.write("\nStarting State Quality Score: " + str(start_score))
    f.write("\nEnding State Quality Score: " + str(end_score))


if __name__ == "__main__":
    main()