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
        self.status = "show_menu" #  store status
        self.chosen_city = ""     #  city that is chosen
        self.city_list = []       # clear city list

    ## List names of all ports that CSAir flies to
    def listAllCities(self):
        self.status = "list_cities_CSAir_flies_to"
        print("\n\n################### City List ################### ")
        nodes = self.graph.nodes # get nodes(port)
        count = 1
        self.city_list = [] # clear city list
        for code in nodes:
            print(str(count) + ": " + nodes[code].info["name"])
            self.city_list.append(nodes[code])   # store that city to list
            count+=1

        ## show options
        print("\n\nEnter 'back' to go back to main menu.")
        possible_options_string = "Please enter the number '1"
        if count - 1 > 1:
            possible_options_string += " ~ " + str(count - 1)
        possible_options_string += "' to get information of that city."
        print(possible_options_string)

    ## Show Menu
    def showMenu(self):
        self.status = "show_menu"
        print("\n\n################### Main Menu ###################")
        print("Enter 'quit' to quit the query.")
        print("Please enter the number '1 ~ 3' to choose a search option.")
        print("1, Cities information")
        print("2, Route information")



    ## Show City information
    '''
    Its code
    Its name
    Its country
    Its continent
    Its timezone
    Its latitude and longitude
    Its population
    Its region
    A list of all of the other cities that are accessible via a single non-stop flight from that source city. This list should include the distance of each of those flights.
    '''
    def showCityInfo(self):
        print("\n\n################### City Info ###################")
        self.status = "list_city_information"
        city = self.chosen_city
        city_info = city.info
        # Get all info
        code = city_info["code"]
        name = city_info["name"]
        country = city_info["country"]
        continent = city_info["continent"]
        timezone = city_info["timezone"]
        coordinates = city_info["coordinates"]
        population = city_info["population"]
        region = city_info["region"]
        connections = city.destinations
        print("Code:        " + code)
        print("Name:        " + name)
        print("Country:     " + country)
        print("Continent:   " + continent)
        print("Timezone:    " + str(timezone))
        coordinates_string = "Coordinate: "
        for key in coordinates:
            coordinates_string = coordinates_string + key + " " + str(coordinates[key]) + "    "
        print(coordinates_string)
        print("Population:  " + str(population))
        print("Region:      " + str(region))

        print("\nCities that are accessible via a single non-stop flight from " + name + ": ")
        count = 1
        self.city_list = [] # clear city list
        for dest in connections:
            distance = connections[dest]
            self.city_list.append(dest)   # store dest to city list
            print("\n" + str(count) + ".\nDist:     " + dest.info["name"])
            print("Distance: " + str(distance))
            count+=1

        ## show options
        print("\n\nEnter 'back' to go back to city list.")
        possible_options_string = "Please enter the number '1"
        if count - 1 > 1:
            possible_options_string += " ~ " + str(count - 1)
        possible_options_string += "' to get information of that city."
        print(possible_options_string)

    ## Show route network info
    def showRouteNetworkInfo(self):
        self.status = "show_route_network_information"

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

        print("\n\n################### Route Network Information ###################")
        # the longest single flight in the network
        print("\n* The longest single flight in the network: ")
        print("      from:     " + longest_single_flight["from"].info["name"])
        print("      to:       " + longest_single_flight["to"].info["name"])
        print("      distance: " + str(longest_single_flight["distance"]))

        # the longest single flight in the network
        print("\n* The shortest single flight in the network: ")
        print("      from:     " + shortest_single_flight["from"].info["name"])
        print("      to:       " + shortest_single_flight["to"].info["name"])
        print("      distance: " + str(shortest_single_flight["distance"]))

        # the average distance of all the flights in the network
        print("\n* The average distance of all the flights in the network: ")
        print("      " + str(total_distance / route_num))

        # biggest city served by CSAir
        print("\n* The biggest city (by population) served by CSAir: ")
        print("      code:       " + biggest_city.info["code"])
        print("      name:       " + biggest_city.info["name"])
        print("      population: " + str(biggest_city.info["population"]))

        # smallest city served by CSAir
        print("\n* The smallest city (by population) served by CSAir: ")
        # print("      code:       " + smallest_city.info["code"])
        print("      name:       " + smallest_city.info["name"])
        print("      population: " + str(smallest_city.info["population"]))

        # the average size (by population) of all the cities served by CSAir
        print("\n* The average size (by population) of all the cities served by CSAir: ")
        print("      " + str(total_population / cities_num))

        # a list of continents served by CSAir and which cities are in them
        print("\n* A list of continents served by CSAir and which cities are in them:")
        for continent in continents:
            print("      ** " + continent)
            count = 1
            cities = continents[continent]
            for city in cities:
                print("          " + str(count) +": " + city.info["name"])
                count += 1

        # a list of the continents served by CSAir and which cities are in them
        cities_and_their_num_of_outbound_flights = sorted(cities_and_their_num_of_outbound_flights, key=lambda t:t[0], reverse=True)
        max_num_of_outbound_flights = cities_and_their_num_of_outbound_flights[0][0]
        print("\n* CSAir's hub cities - the cities that have the most direct connections:")
        i = 0
        while i < len(cities_and_their_num_of_outbound_flights) and cities_and_their_num_of_outbound_flights[i][0] == max_num_of_outbound_flights:
            print("      name:       " + cities_and_their_num_of_outbound_flights[i][1].info["name"])
            i += 1


    ## Process the query
    def processQuery(self):
        input_str = input("> ")

        ## under main menu
        if self.status == "show_menu":
            if input_str == "1":
                self.listAllCities()
            elif input_str == "2":
                self.showRouteNetworkInfo()
            elif input_str == "quit":
                sys.exit(0)
            else:
                print("Invalid option: " + input_str)
        ## under city list
        elif self.status == "list_cities_CSAir_flies_to":
            if input_str == "back":                                                    # go back to main menu
                self.showMenu()
            elif int(input_str) >= 1 and int(input_str) <= len(self.city_list):        # get city info
                self.chosen_city = self.city_list[int(input_str) - 1] # set chosen city
                self.showCityInfo()
            else:
                print("Invalid option: " + input_str)
        ## under city info
        elif self.status == "list_city_information":
            if input_str == "back":                                                    # go back to city list
                self.listAllCities()
            elif int(input_str) >= 1 and int(input_str) <= len(self.city_list):        # get city info
                self.chosen_city = self.city_list[int(input_str) - 1] # set chosen city
                self.showCityInfo()
            else:
                print("Invalid option: " + input_str)
        elif self.status == "show_route_network_information":
            if input_str == "back":                                                    # go back to main menu
                self.showMenu()
            else:
                print("Invalid option: " + input_str)