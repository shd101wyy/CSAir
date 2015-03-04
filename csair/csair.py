# I am using Python version 3.4.3

'''
Define Node class
'''
class Node():
    # Constructor for Node class
    # save necessary information: code, name, countrym continent, timezone, coordinate, population, region
    def __init__(self,
                 code,
                 name,
                 country,
                 continent,
                 timezone,
                 coordinates,
                 population,
                 region):
        self.code = code
        self.name = name
        self.country = country
        self.continent = continent
        self.timezone = timezone
        self.coordinates = coordinates
        self.population = population
        self.region = region