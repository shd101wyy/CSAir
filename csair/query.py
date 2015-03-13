__author__ = 'wangyiyi'
from graph import Graph
import sys
'''
Build up the query system
'''
class Query():
    ## Constructor: bind graph
    def __init__(self, graph):
        self.graph = graph        #  bind graph
        if self.graph.nodes != {}:
            self.queryRouteInfo()

    ## load json file
    def loadJSON(self, file_name):
        self.graph.loadJSON(file_name)
        self.queryRouteInfo()     #  calculate route info

    ## get a list of all cities that csair flies to
    def getAllCities(self):
        return self.graph.nodes

    ## get longest single flight
    def getLongestSingleFlight(self):
        cities = self.graph.nodes # get nodes(port)
        longest_single_flight_distance = -1
        longest_single_flight = -1
        for code in cities:
            city = cities[code]
            city_destinations = city.destinations # get city destinations
            for dest in city_destinations:
                distance = city_destinations[dest]
                if longest_single_flight_distance == -1 or longest_single_flight_distance < distance:
                    longest_single_flight_distance = distance
                    longest_single_flight = {"from": city, "to": dest, "distance": distance}
        self.longest_single_flight = longest_single_flight

    # get shortest single flight
    def getShortestSingleFlight(self):
        cities = self.graph.nodes # get nodes(port)
        shortest_single_flight_distance = -1
        shortest_single_flight = -1
        for code in cities:
            city = cities[code]
            city_destinations = city.destinations # get city destinations
            for dest in city_destinations:
                distance = city_destinations[dest]
                if shortest_single_flight_distance == -1 or shortest_single_flight_distance > distance:
                    shortest_single_flight_distance = distance
                    shortest_single_flight = {"from": city, "to": dest, "distance": distance}
        self.shortest_single_flight = shortest_single_flight

    # calculate average distance
    def getAverageDistance(self):
        cities = self.graph.nodes # get nodes(port)
        total_distance = 0
        route_num = 0
        for code in cities:
            city = cities[code]
            city_destinations = city.destinations
            for dest in city_destinations:
                distance = city_destinations[dest]
                total_distance += distance          # increase total distance
                route_num += 1                      # increase route num
        self.average_distance = total_distance / route_num  # calculate average distance

    # get biggest city
    def getBiggestCity(self):
        cities = self.graph.nodes # get nodes(port)
        biggest_city_population = -1
        biggest_city = -1
        for code in cities:
            city = cities[code]
            city_info = city.info
            # get biggest city
            if biggest_city_population == -1 or biggest_city_population < city_info["population"]:
                biggest_city_population = city_info["population"]
                biggest_city = city
        self.biggest_city = biggest_city

    # get smallest city
    def getSmallestCity(self):
        cities = self.graph.nodes # get nodes(port)
        smallest_city_population = -1
        smallest_city = -1
        for code in cities:
            city = cities[code]
            city_info = city.info
            # get smallest city
            if smallest_city_population == -1 or smallest_city_population > city_info["population"]:
                smallest_city_population = city_info["population"]
                smallest_city = city
        self.smallest_city = smallest_city

    # get average size of city
    def getAverageSizeOfCity(self):
        cities = self.graph.nodes # get nodes(port)
        total_population = 0
        cities_num = 0
        for code in cities:
            city = cities[code]
            city_info = city.info
            # increase total number of population
            total_population += city_info["population"]
            # increase total number of cities
            cities_num += 1
        self.average_population = total_population / cities_num

    # get a list of continents
    def getContinentsInformation(self):
        cities = self.graph.nodes # get nodes(port)
        continents = {}  # its key is continent name
        for code in cities:
            city = cities[code]
            city_info = city.info
            ## set to continents
            continent = city_info["continent"]
            if continent in continents:
                continents[continent].append(city)
            else:
                continents[continent] = [city]
        self.continents = continents

    # get hub cities
    def getHubCities(self):
        cities = self.graph.nodes # get nodes (port)
        cities_and_their_num_of_outbound_flights = []
        for code in cities:
            city = cities[code]
            city_destinations = city.destinations
            cities_and_their_num_of_outbound_flights.append((len(city_destinations.keys()), city))

        # sort by number of outbound flights
        cities_and_their_num_of_outbound_flights = sorted(cities_and_their_num_of_outbound_flights, key=lambda t:t[0], reverse=True)
        self.max_num_of_outbound_flights = cities_and_their_num_of_outbound_flights[0][0]
        self.hub_cities = []
        i = 0
        while i < len(cities_and_their_num_of_outbound_flights) and cities_and_their_num_of_outbound_flights[i][0] == self.max_num_of_outbound_flights:
            self.hub_cities.append(cities_and_their_num_of_outbound_flights[i][1])
            i += 1

    # query all required information
    def queryRouteInfo(self):
        self.getLongestSingleFlight()
        self.getShortestSingleFlight()
        self.getAverageDistance()
        self.getBiggestCity()
        self.getSmallestCity()
        self.getAverageSizeOfCity()
        self.getContinentsInformation()
        self.getHubCities()
