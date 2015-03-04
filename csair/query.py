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
        print("\n\nEnter 'back' to go back to main menu.")
        print("Please enter the number '1 ~ " + str(count - 1) + "' to get information of that city.")

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
        print("\n\n################### City Info ###################")
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
        print("\n\nEnter 'back' to go back to city list.")
        print("Please enter the number '1 ~ " + str(count - 1) + "' to get information of that destination city.")

    ## Process the query
    def processQuery(self):
        input_str = input("> ")
        if self.status == "show_menu":
            if input_str == "1":
                self.listAllCities()
            elif input_str == "2":
                self.status = "show_route_network_information"
                pass
            elif input_str == "quit":
                sys.exit(0)
            else:
                print("Invalid option: " + input_str)
        elif self.status == "list_cities_CSAir_flies_to":
            if input_str == "back":                                                    # go back to main menu
                self.showMenu()
            elif int(input_str) >= 1 and int(input_str) <= len(self.city_list):        # get city info
                self.chosen_city = self.city_list[int(input_str) - 1] # set chosen city
                self.showCityInfo()
            else:
                print("Invalid option: " + input_str)
        elif self.status == "list_city_information":
            if input_str == "back":                                                    # go back to city list
                self.listAllCities()
            elif int(input_str) >= 1 and int(input_str) <= len(self.city_list):        # get city info
                self.chosen_city = self.city_list[int(input_str) - 1] # set chosen city
                self.showCityInfo()
            else:
                print("Invalid option: " + input_str)