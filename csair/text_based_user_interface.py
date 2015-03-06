__author__ = 'wangyiyi'
__author__ = 'wangyiyi'
import sys
from query import Query
'''
Build up the text based user interface.
'''
class TextBasedUserInterface():
    ## Constructor: bind graph
    def __init__(self, graph):
        self.query = Query(graph) ## setup query
        self.status = "show_menu" #  store status
        self.chosen_city = ""     #  city that is chosen
        self.city_list = []       # clear city list


    ## List names of all ports that CSAir flies to
    def listAllCities(self):
        self.status = "list_cities_CSAir_flies_to"
        print("\n\n################### City List ################### ")
        nodes = self.query.getAllCities() # get nodes(port)
        count = 1
        self.city_list = [] # clear city list

        # print each city name
        for code in nodes:
            print(str(count) + ": " + nodes[code].info["name"])
            self.city_list.append(nodes[code])   # store that city to list
            count+=1

        ## show options
        print("\n\nEnter 'back' to go back to main menu.")
        possible_options_string = "Please enter the number '1'"
        if count - 1 > 1:
            possible_options_string += " ~ '" + str(count - 1) + "'"
        possible_options_string += " to get information of that city."
        if count != 1:
            print(possible_options_string)

    ## Show Menu
    def showMenu(self):
        self.status = "show_menu"
        print("\n\n################### Main Menu ###################")
        print("Enter 'quit' to quit the query.")
        print("Please enter the number '1' ~ '3' to choose a search option.")
        print("1, Cities information")
        print("2, Route information")
        print("3, Visualize CSAir's route map")



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

        # print city info
        print("Code:        " + code)
        print("Name:        " + name)
        print("Country:     " + country)
        print("Continent:   " + continent)
        print("Timezone:    " + str(timezone))
        coordinates_string = "Coordinate: "
        # print coordinates
        for key in coordinates:
            coordinates_string = coordinates_string + key + " " + str(coordinates[key]) + "    "
        print(coordinates_string)
        print("Population:  " + str(population))
        print("Region:      " + str(region))

        print("\nCities that are accessible via a single non-stop flight from " + name + ": ")
        count = 1
        self.city_list = [] # clear city list

        # print possible destinations
        for dest in connections:
            distance = connections[dest]
            self.city_list.append(dest)   # store dest to city list
            print("\n" + str(count) + ".\nDist:     " + dest.info["name"])
            print("Distance: " + str(distance))
            count+=1

        ## show options
        print("\n\nEnter 'back' to go back to city list.")
        possible_options_string = "Please enter the number '1'"
        if count - 1 > 1:
            possible_options_string += " ~ '" + str(count - 1) + "'"
        possible_options_string += " to get information of that destination city."
        if count != 1:
            print(possible_options_string)

    ## Show route network info
    def showRouteNetworkInfo(self):
        self.status = "show_route_network_information"
        print("\n\n################### Route Network Information ###################")
        # the longest single flight in the network
        print("\n* The longest single flight in the network: ")
        print("      from:     " + self.query.longest_single_flight["from"].info["name"])
        print("      to:       " + self.query.longest_single_flight["to"].info["name"])
        print("      distance: " + str(self.query.longest_single_flight["distance"]))

        # the longest single flight in the network
        print("\n* The shortest single flight in the network: ")
        print("      from:     " + self.query.shortest_single_flight["from"].info["name"])
        print("      to:       " + self.query.shortest_single_flight["to"].info["name"])
        print("      distance: " + str(self.query.shortest_single_flight["distance"]))

        # the average distance of all the flights in the network
        print("\n* The average distance of all the flights in the network: ")
        print("      " + str(self.query.average_distance))

        # biggest city served by CSAir
        print("\n* The biggest city (by population) served by CSAir: ")
        print("      code:       " + self.query.biggest_city.info["code"])
        print("      name:       " + self.query.biggest_city.info["name"])
        print("      population: " + str(self.query.biggest_city.info["population"]))

        # smallest city served by CSAir
        print("\n* The smallest city (by population) served by CSAir: ")
        # print("      code:       " + smallest_city.info["code"])
        print("      name:       " + self.query.smallest_city.info["name"])
        print("      population: " + str(self.query.smallest_city.info["population"]))

        # the average size (by population) of all the cities served by CSAir
        print("\n* The average size (by population) of all the cities served by CSAir: ")
        print("      " + str(self.query.average_population))

        # a list of continents served by CSAir and which cities are in them
        print("\n* A list of continents served by CSAir and which cities are in them:")
        for continent in self.query.continents:
            print("      ** " + continent)
            count = 1
            cities = self.query.continents[continent]
            for city in cities:
                print("          " + str(count) +": " + city.info["name"])
                count += 1

        # a list of the continents served by CSAir and which cities are in them
        print("\n* CSAir's hub cities - the cities that have the most direct connections:")
        hub_cites = self.query.hub_cites
        max_num_of_outbound_flights = self.query.max_num_of_outbound_flights
        i = 0
        while i < len(hub_cites):
            print("      name:       " + hub_cites[i].info["name"])
            i += 1
        print("      max outbound flights num:     " + str(max_num_of_outbound_flights))

        print("\n\nEnter 'back' to go back to main menu.")


    ## Process the query
    def processQuery(self):
        input_str = input("> ").strip()
        try:
            ## under main menu
            if self.status == "show_menu":
                if input_str == "1":                                                       # list all cities that CSAir flies to
                    self.listAllCities()
                elif input_str == "2":                                                     # show route network info
                    self.showRouteNetworkInfo()
                elif input_str == "3":                                                     # Visualize  CSAir's route map
                    self.query.graph.visualizeCSAirRouteMap()
                elif input_str == "quit":                                                  # quit query
                    sys.exit(0)
                else:
                    print("Invalid option: " + input_str)
            ## under city list
            elif self.status == "list_cities_CSAir_flies_to":
                if input_str == "back":                                                    # go back to main menu
                    self.showMenu()
                elif len(input_str) > 0 and int(input_str) >= 1 and int(input_str) <= len(self.city_list):        # get city info
                    self.chosen_city = self.city_list[int(input_str) - 1] # set chosen city
                    self.showCityInfo()
                else:
                    print("Invalid option: " + input_str)
            ## under city info
            elif self.status == "list_city_information":
                if input_str == "back":                                                    # go back to city list
                    self.listAllCities()
                elif len(input_str) > 0 and int(input_str) >= 1 and int(input_str) <= len(self.city_list):        # get city info
                    self.chosen_city = self.city_list[int(input_str) - 1] # set chosen city
                    self.showCityInfo()
                else:
                    print("Invalid option: " + input_str)
            elif self.status == "show_route_network_information":
                if input_str == "back":                                                    # go back to main menu
                    self.showMenu()
                else:
                    print("Invalid option: " + input_str)
        except Exception:
            print("Invalid option: " + input_str)