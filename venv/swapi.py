import requests
import json

def getNextPage(url):
    response = requests.get(url)
    data = json.loads(response.text)
    nextpage = data['next']
    return nextpage

def buildResultList(type):
    result_list = []
    response = requests.get('https://swapi.dev/api/' + type)
    print('Populating ', type,'...')
    print("Downloading original page", 'https://swapi.dev/api/' + type)
    data = json.loads(response.text)
    nextpage = data['next']

    result_list = result_list + data['results']

    while nextpage is not None:
        print('Downloading next page ', nextpage)
        response = requests.get(nextpage)
        result = json.loads(response.text)
        result_list = result_list + result['results']
        nextpage = getNextPage(nextpage)

    return result_list

people = buildResultList('people')
planets = buildResultList('planets')
starships = buildResultList('starships')
species = buildResultList('species')

# initialization of reference dictionaries
starships_dict = {}
planets_dict = {}
species_dict = {}
people_species_dict = {}
people_dict = {}


# population of url to relevant value
for s in starships:
    starships_dict[s['url']] = s['name']

for p in planets:
    planets_dict[p['url']] = p['name']

for s in species:
    species_dict[s['url']] = s['name']

# this loop builds the person->species dictionary and prints each name and the information relevant to that person
for p in people:
    print(p['name'])
    # here I built the reference dictionary that ties the url of the person to that person's species
    # this is used in a subsequent step when the planet_species dictionary is built and manipulated
    people_species_dict[p['url']] = species_dict.get(''.join(p['species']))
    print('\tStarships:')
    for s in p['starships']:
        print('\t\t', starships_dict.get(s))
    print('\tPlanets:')
    print('\t\t',planets_dict.get(p['homeworld']))

planet_species = {}

# using the planet dictionary I parsed each resident of the planet and got the species for each person
for p in planets:
    for r in p['residents']:
        planet_species[p['name']] = people_species_dict.get(r)

# this dictionary comprehension inverts the planets and species that live on them, making the species name the key
planet_species_inverted = dict()
for k,v in planet_species.items():
    planet_species_inverted.setdefault(v,list()).append(k)

#initialize an empty dictionary to hold the frequency count of planets per species
species_planet_dict = {}

# frequency count of planets per species
for k,val in planet_species_inverted.items():
    species_planet_dict[k] = len([item for item in val if item])

# use a loop to print out the species that live on more than one planet
print('Species that inhabit more than one planet: ')
for k in species_planet_dict:
    v = species_planet_dict[k]
    if v > 1:
       print(k)
