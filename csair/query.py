__author__ = 'wangyiyi'
from graph import Graph
import sys
'''
Build up the query system
'''
class Query():
    def __init__(self, graph):
        """
        Constructor: bind graph
                     calculate and get information for route network if necessary.
        """
        self.graph = graph        #  bind graph
        if self.graph.nodes != {}:
            self.queryAllRouteInfo()

    def loadJSON(self, file_name):
        """
        load json file
        """
        self.graph.loadJSON(file_name)
        if self.graph.nodes != {}:
            self.queryAllRouteInfo()     #  calculate route info

    def getAllCities(self):
        """
        get a list of all cities that csair flies to
        """
        return self.graph.nodes

    def getLongestSingleFlight(self):
        """
        get longest single flight
        """
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

    def getShortestSingleFlight(self):
        """
        get shortest single flight
        """
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

    def getAverageDistance(self):
        """
        calculate average distance
        """
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

    def getBiggestCity(self):
        """
        get biggest city
        """
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

    def getSmallestCity(self):
        """
        get smallest city
        """
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

    def getAverageSizeOfCity(self):
        """
        get average size of city
        """
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

    def getContinentsInformation(self):
        """
        get a list of continents
        """
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

    def getHubCities(self):
        """
        get hub cities
        """
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

    def calculateLayoverTime(self, outbound_flights_num):
        """
        calculate layover time
        """
        return 2 - (1/6) * (outbound_flights_num - 1)

    def calculateFlyingTime(self, distance):
        """
        calculate flying time
        """
        a = (750 - 0) / (400 / 750)
        if distance <= 400:
            half_distance = distance / 2
            t = ((2 * half_distance) / a) ** 0.5
            t = t * 2 # accelerate and decelerate
        else:
            t = ((2 * 200) / a) ** 0.5
            t = t * 2   # accelerate and decelerate
            t += (distance - 400)/750 # cruising
        return t

    def queryRouteInfo(self, list_of_cities):
        """
        query information about the route among many cities
        return False if the route is invalid
        """
        total_distance = 0
        total_cost = 0
        total_time = 0
        cost_per_km = 0.35
        i = 0
        while i < len(list_of_cities) - 1:
            if type(list_of_cities[0]) == str:
                src = self.graph.getCityByNameOrCode(list_of_cities[0].strip())
            else:
                src = list_of_cities[0]
            if type(list_of_cities[1]) == str:
                dest = self.graph.getCityByNameOrCode(list_of_cities[1].strip())
            else:
                dest = list_of_cities[1]
            if src == False or dest == False: # invalid src or dest
                return False
            if not (dest in src.destinations): # not connected
                return False
            distance = src.destinations[dest]
            total_distance += distance

            if cost_per_km == 0: # keep it free
                pass
            else: # decrease the cost for another leg
                total_cost += cost_per_km * distance
                cost_per_km -= 0.05

            # add layover time
            if i != 0:
                total_time += self.calculateLayoverTime(len(src.destinations))
            # add flying time
            total_time += self.calculateFlyingTime(distance)
            i += 1
        return {"total_distance": total_distance,
                "total_cost": total_cost,
                "total_time": total_time}


    def queryAllRouteInfo(self):
        """
        query all required information for the route network
        """
        self.getLongestSingleFlight()
        self.getShortestSingleFlight()
        self.getAverageDistance()
        self.getBiggestCity()
        self.getSmallestCity()
        self.getAverageSizeOfCity()
        self.getContinentsInformation()
        self.getHubCities()
