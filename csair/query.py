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
        self.queryRouteInfo()     #  calculate route info

    ## get a list of all cities that csair flies to
    def getAllCities(self):
        return self.graph.nodes


    ## query route info
    def queryRouteInfo(self):
        cities = self.graph.nodes # get nodes(port)
        longest_single_flight_distance = -1
        longest_single_flight = -1
        shortest_single_flight_distance = -1
        shortest_single_flight = -1
        total_distance = 0
        biggest_city_population = -1
        biggest_city = -1
        smallest_city_population = -1
        smallest_city = -1
        total_population = 0
        cities_num = 0
        continents = {}     # its key is continent name
        route_num = 0
        cities_and_their_num_of_outbound_flights = []
        biggest_connection_num = -1;
        biggest_connection_city = -1;
        for code in cities:
            city = cities[code]
            city_info = city.info                  # get city info
            city_destionatiosn = city.destinations # get city destinations
            ## check flying distance
            for dest in city_destionatiosn:
                distance = city_destionatiosn[dest]
                ## get longest single flight in the network
                if longest_single_flight_distance == -1 or longest_single_flight_distance < distance:
                    longest_single_flight_distance = distance
                    longest_single_flight = {"from": city, "to": dest, "distance": distance}

                ## get shortest single flight in the network
                if shortest_single_flight_distance == -1 or shortest_single_flight_distance > distance:
                    shortest_single_flight_distance = distance
                    shortest_single_flight = {"from": city, "to": dest, "distance": distance}

                ## increase total distance
                total_distance += distance

                ## increase total number of route
                route_num += 1
            cities_and_their_num_of_outbound_flights.append((len(city_destionatiosn.keys()), city))

            ## get biggest_city
            if biggest_city_population == -1 or biggest_city_population < city_info["population"]:
                biggest_city_population = city_info["population"]
                biggest_city = city

            ## get smallest city
            if smallest_city_population == -1 or smallest_city_population > city_info["population"]:
                smallest_city_population = city_info["population"]
                smallest_city = city

            ## increase total population
            total_population += city_info["population"]

            ## set to continents
            continent = city_info["continent"]
            if continent in continents:
                continents[continent].append(city)
            else:
                continents[continent] = [city]

            ## increase total number of cities
            cities_num += 1

        ## process route info
        self.longest_single_flight = longest_single_flight          # set longest single flight
        self.shortest_single_flight = shortest_single_flight        # set shortest single flight
        self.average_distance = total_distance / route_num          # calculate average distance
        self.biggest_city = biggest_city                            # set biggest city
        self.smallest_city = smallest_city                          # set smallest city
        self.average_population = total_population / cities_num     # calculate average population
        self.continents = continents                                # set continents
        cities_and_their_num_of_outbound_flights = sorted(cities_and_their_num_of_outbound_flights, key=lambda t:t[0], reverse=True)
        self.hub_cites = []                                         # get hub cities
        max_num_of_outbound_flights = cities_and_their_num_of_outbound_flights[0][0]
        self.max_num_of_outbound_flights = max_num_of_outbound_flights
        i = 0
        while i < len(cities_and_their_num_of_outbound_flights) and cities_and_their_num_of_outbound_flights[i][0] == max_num_of_outbound_flights:
            self.hub_cites.append(cities_and_their_num_of_outbound_flights[i][1])
            i += 1