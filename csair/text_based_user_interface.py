__author__ = 'wangyiyi'
__author__ = 'wangyiyi'
import sys
from query import Query
import cmd
import os
'''
Build up the text based user interface.
'''
class TextBasedUserInterface(cmd.Cmd):
    def __init__(self, graph):
        cmd.Cmd.__init__(self)
        self.prompt = "CSAir > "
        self.intro = "Hi there! Welcome to use CSAir information query system\nPlease use 'load_json_files' commands to load JSON data file first\ntype 'help' to check documented commands"
        self.query = Query(graph)

    def do_EOF(self, line):
        return True

    def do_list_json_files(self, line):
        """
            List all loadable JSON files
        """
        files = os.listdir("./data/")
        for file in files:
            print(file)

    def do_load(self, line):
        """
            Load JSON files
            load file1.json file2.json ...

            eg:
                load data.json
                load old.json new.json
        """
        if len(line) == 0:
            self.do_help("load")
            return
        files = line.split(" ")
        for file_name in files:
            self.query.loadJSON(file_name)

    def printCities(self):
        nodes = self.query.getAllCities() # get nodes(port)
        count = 1

        # print each city name
        for code in nodes:
            print(str(count) + ": " + nodes[code].info["name"])
            count+=1

    def do_city_info(self, line):
        """
            Show information of the city
            usage:
                   city_info                     -  Show  a list of all the cities that CSAir flies to
                   city_info [city_name]         -  Get specific information about a specific city in the CSAir route network
                   city_info [city_code]         -  Get specific information about a specific city in the CSAir route network

            eg:    city_info Beijing
                   city_info TKO
        """
        if len(line) == 0:    # list all cities
            self.printCities()
            return
        city = self.query.graph.getCityByNameOrCode(line) # get specific city
        if city == False: # didnt find city
            print("Cannot find city: " + line + " from database")
            return

        # Get all info
        city_info = city.info
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
            print("\n" + str(count) + ".\nDest:     " + dest.info["name"])
            print("Distance: " + str(distance))
            count+=1

    def do_route_info(self, line):
        """
            Statistical information about CSAir's route network, such as:
                a. the longest single flight in the network
                b. the shortest single flight in the network
                c. the average distance of all the flights in the network
                d. the biggest city (by population) served by CSAir
                e. the smallest city (by population) served by CSAir
                f. the average size (by population) of all the cities served by CSAir
                g. a list of the continents served by CSAir and which cities are in them
                h. identifying CSAir's hub cities – the cities that have the most direct connections.

            usage:
                route_info
        """
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
        print("      code:       " + self.query.smallest_city.info["code"])
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
        hub_cities = self.query.hub_cities
        max_num_of_outbound_flights = self.query.max_num_of_outbound_flights
        i = 0
        while i < len(hub_cities):
            print("      name:       " + hub_cities[i].info["name"])
            i += 1
        print("      max flights num:     " + str(max_num_of_outbound_flights))

    def do_show_map(self, line):
        """
            Visualizing CSAir's route map
            usage:
                show_map
        """
        self.query.graph.visualizeCSAirRouteMap()


    def do_remove_city(self, line):
        """
            Remove a city
            usage:
                remove_city  [city_name]         remove the city by city name
                remove_city  [city_code]         remove the city by city code

            eg:
                remove_city Tokyo
                remove_city TKO
        """
        if len(line) == 0:
            self.do_help("remove_city")
            return
        if self.query.graph.removeCity(line):
            print("City: " + line + " removed successfully")
        else:
            print("Cannot remove city: " + line)

    def do_remove_route(self, line):
        """
            Remove a route
            usage:
                remove_route [source city] [destination city]    source city disconnects the destination city

            eg:
                remove_route Shanghai Taipei    will disconnect Shanghai from Taipei
                remove_route SHA      TPE
        """
        if len(line) == 0:
            self.do_help("remove_route")
            return
        source_dest = line.split(" ")
        if len(source_dest) == 2:
            remove_result = self.query.graph.removeRoute(source_dest[0].strip(), source_dest[1].strip())
            if remove_result == True: # remove successfully
                print("Route: " + line + " is removed")
                return
        print("Cannot remove route: " + line)

    '''
        read coordinates from user
    '''
    def getUserInputCoordinates(self):
        while True:
            input_str = input("please enter the coordinates:(format eg: W 24 S 17):").strip().upper()
            if len(input_str) == 0:
                continue
            coord_info = input_str.split(" ")
            if len(coord_info) != 4:
                print("Invalid coordinates: " + input_str)
            else:
                try:
                    return {coord_info[0]: int(coord_info[1]), coord_info[2]: int(coord_info[3])}
                except Exception:
                    print("Invalid coordinates: " + input_str)

    ## get user input value for some city properties like code, name, etc
    def getUserInputForCity(self, city_info_key):
        if city_info_key == "coordinates":
            return self.getUserInputCoordinates()
        while True:
            input_str = input("Please enter the " + city_info_key + ":").strip()
            if len(input_str) == 0:
                continue
            if city_info_key == "population" or city_info_key == "region" or city_info_key == "timezone":
                if (input_str[0] == "-" and input_str[1:].isdigit()) or input_str.isdigit():
                    input_str = int(input_str)
                else:
                    print("Invalid input for " + city_info_key + ", which required Integer")
                    continue
            return input_str


    def do_add_city(self, line):
        """
            Add a new city to database
            usage:
                add_city
        """
        info_list = ["code", "name", "country", "continent", "timezone", "coordinates", "population", "region"]
        info = {}
        for key in info_list:
            info[key] = self.getUserInputForCity(key)
        self.query.graph.addCity(info) # add city to the graph
        print("City created successfully")
        print(info)

    def do_add_route(self, line):
        """
            add a route
            usage:
                add_route [source city] [destination city] [distance]   source city connects the destination city with distance

            eg:
                add_route PEK TYO 100    will connect Beijing to Tokyo with distance 100
        """
        if len(line) == 0:
            self.do_help("add_route")
            return
        source_dest_distance = line.split(" ")
        if len(source_dest_distance) == 3:
            try:
                connect_result = self.query.graph.addRoute(source_dest_distance[0].strip(), source_dest_distance[1].strip(), int(source_dest_distance[2].strip()))
                if connect_result == True: # add successfully
                    print("Route: " + line + " is connected")
                    return
            except Exception:
                print("Invalid Route: " + line)
                return

        print("Invalid Route: " + line)

    def do_quit(self, line):
        """
            quit the query program
        """
        sys.exit(0)


    def do_edit_city(self, line):
        """
            edit city information
            usage:
                edit_city [city_code]
            eg:
                edit_city LAX
        """
        if len(line) == 0:
            return
        city = self.query.graph.getCityByNameOrCode(line)
        if city == False:
            print("Cannot find city: " + line + " from database")

        print("\nCurrent city info:")
        print(city.info)
        print("Please enter the following option to edit the city:")
        print("back  -            go back to query system")
        print("1     -            edit code")
        print("2     -            edit name")
        print("3     -            edit country")
        print("4     -            edit continent")
        print("5     -            edit timezone")
        print("6     -            edit coordinates")
        print("7     -            edit population")
        print("8     -            edit region")

        key_dict = {
            "1": "code",
            "2": "name",
            "3": "country",
            "4": "continent",
            "5": "timezone",
            "6": "coordinates",
            "7": "population",
            "8": "region"
        }

        while True:
            input_str = input("edit city > ").strip();
            if len(input_str) == 0:
                continue
            elif input_str == "back":
                return
            try:
                if input_str in key_dict:
                    key = key_dict[input_str]
                    if key == "code":
                        old_code_value = city.info["code"]   # save old code value
                    city.info[key] = self.getUserInputForCity(key) # update property value
                    if key == "code":            # because here I changed code value, I also need to update the graph
                        self.query.graph.nodes["code"] = city
                        del dict[old_code_value]
                    print("\nUpdated:")
                    print(city.info)
                else:
                    continue
            except Exception:
                continue

    def do_save(self, line):
        """
            Save current route network
            usage:
                save [json_file_name]
            eg:
                save my_data.json
        """
        if len(line) == 0:
            self.do_help("save")
            return;
        if len(line) <= 5 or line[-5:] != ".json":
            print("Invalid file name: " + line + "      \nPlease end the file name with .json.  eg: data.json")
            return
        self.query.graph.saveGraph(line) # save the graph
        print("File: " + line + " saved successfully!")