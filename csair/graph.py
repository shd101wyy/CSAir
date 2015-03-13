__author__ = 'wangyiyi'
import json
from pprint import pprint
from node import Node
import webbrowser
'''
Graph class
parse JSON File, generate graph
'''
class Graph:
    def generateNodes(self, metros):
        """ generate node according to metros data
        :param metros: metro information
        """
        for info in metros:
            node = Node(info) # create Node
            self.nodes[info["code"]] = node # add to node list

    def connectNodes(self, routes):
        """ build routes by connecting nodes
        :param routes: route information
        """
        for info in routes:
            distance = info["distance"]     # get distance
            ports = info["ports"]             # get 2 codes of ports
            source = self.nodes[ports[0]]
            destination = self.nodes[ports[1]]
            source.connect(destination, distance)     # connect source and destination
            # the json file now represents directed graph instead of undirected graph
            # destination.connect(source, distance)     # connect destination to source as well

    def generateURL(self):
        """  generate url to visualize the map
            # eg: http://www.gcmap.com/mapui?P=LIM-MEX,+LIM-BOG,+MEX-LAX
        """
        url = "http://www.gcmap.com/mapui?P="
        url_param = ""
        for city_code in self.nodes:
            city = self.nodes[city_code]      # get city
            destinations = city.destinations  # get its destinations
            for dest in destinations:
                url_param += "+" + city_code +"-" +dest.info["code"] +"," # create param for url
        url_param = url_param[1:-1] # clean url parameters
        url = url + url_param # get url
        return url

    def visualizeCSAirRouteMap(self):
        """ Visualize CSAir's route map
            open the browser if necessary
        """
        webbrowser.open(self.generateURL())

    def getCityByNameOrCode(self, name_or_code):
        """ find city object by city name or city code
            if no such city is found, return False
        :param name_or_code:
        """
        name_or_code = name_or_code.lower()
        for city_code in self.nodes:
            city = self.nodes[city_code]
            if city.info["name"].lower() == name_or_code or city.info["code"].lower() == name_or_code:
                return city
        return False

    def removeCity(self, city_name_or_code):
        """
        remove a city from the graph, given city name or city code
        return True if we find the city to remove
        otherwise return False
        """

        """
        :param city_name_or_code:
        :return:
        """
        city = self.getCityByNameOrCode(city_name_or_code)
        if city == False:
            return False # didnt find city
        else:
            destinations = city.destinations
            for dest in destinations:
                dest.disconnect(city)  # disconnect
            self.nodes.pop(city.info["code"], None)
            return True # successfully removed city from current graph

    def removeRoute(self, source_name_or_code, dest_name_or_code):
        """
        remove a route
        if there is such route, remove it and return True
        otherwise return False
        :param source_name_or_code: source
        :param dest_name_or_code:  destination
        """
        src = self.getCityByNameOrCode(source_name_or_code)
        dest = self.getCityByNameOrCode(dest_name_or_code)
        if src == False or dest == False: # invalid city
            return False
        if dest in src.destinations:
            src.disconnect(dest)
            return True  # removed route
        else:
            return False # no such route

    def convertGraphToJSON(self):
        """ Convert current graph to JSON data format
        """
        data = {"metros": [], "routes": []}
        for city_code in self.nodes:
            city = self.nodes[city_code]   # get city
            city_info = city.info
            city_destinations = city.destinations

            # put city_info to data
            data["metros"].append(city_info)

            # put dest to data
            for dest in city_destinations:
                data["routes"].append({"ports": [city_info["code"], dest.info["code"]], "distance": city_destinations[dest]})
        return data

    def saveGraph(self, file_name):
        """ Save the graph to json file given file_name
        """
        with open("./data/" + file_name, 'w') as outfile:
            json.dump(self.convertGraphToJSON(), outfile, indent=4, sort_keys=True)

    def addCity(self, info):
        """ Add a city to graph
        """
        self.nodes[info["code"]] = Node(info)

    def addRoute(self, src_name_or_code, dest_name_or_code, distance):
        """
        Add a route between two cities
        return True if the route is created; otherwise return False
        :param src_name_or_code:  source city
        :param dest_name_or_code:  destination city
        :param distance:  distance of the route
        """
        src = self.getCityByNameOrCode(src_name_or_code)
        dest = self.getCityByNameOrCode(dest_name_or_code)
        if src == False or dest == False: # didn't find city
            return False
        else:
            src.connect(dest, distance)
            return True

    def loadJSON(self, file_name):
        """load a json file
        """
        try:
            json_file = open("data/" + file_name) # load JSON file
            json_data = json.load(json_file) # parse JSON data
            json_file.close() # close file

            # Genearte nodes
            metros = json_data["metros"]
            self.generateNodes(metros)

            # Generate connections
            routes = json_data["routes"]
            self.connectNodes(routes)

        except Exception:
            print(Exception)

    def __init__(self, file_name=None, json_data=None):
        """
        ## Constructor: initiate graph
        ## Load JSON file, parser JSON data if necessary
        ## Generate Graph by JSON data
        """
        self.nodes = {} # key is code of the port, value is the node
        if file_name == None and json_data == None:
            return
        if file_name != None:
            json_file = open(file_name) # load JSON file
            json_data = json.load(json_file) # parse JSON data
            json_file.close() # close file

        # Genearte nodes
        metros = json_data["metros"]
        self.generateNodes(metros)

        # Generate connections
        routes = json_data["routes"]
        self.connectNodes(routes)




    def shortestPath(self, src, dest):
        """
        ## Dijkstra's Algorithm refered from Wikipedia
        ## Return the shortest path: a list that contains all cities
        ## if the src or dest is invalid, return False
        :param src: source city
        :param dest: destination city
        """
        src = self.getCityByNameOrCode(src)
        dest = self.getCityByNameOrCode(dest)
        if src == False or dest == False:
            return False
        dist = {}
        prev = {}
        unvisited_nodes = {}

        dist[src] = 0
        prev[src] = None
        unvisited_nodes[src] = True

        for code in self.nodes:   # initialization
            city = self.nodes[code]
            if city != src:
                dist[city] = float("inf")
                prev[city] = None
            unvisited_nodes[city] = True

        while len(unvisited_nodes.keys()) != 0:
            smallest = None
            for n in unvisited_nodes:
                if smallest == None or dist[n] < dist[smallest]:
                    smallest = n
            u = smallest # get vertex that has smallest dist
            unvisited_nodes.pop(u, None) # remove u from unvisited nodes

            if u == dest: # find destination
                output = []
                while u != None:
                    output = [u] + output
                    u = prev[u]
                return output

            for v in u.destinations:
                alt = dist[u] + u.destinations[v]
                if alt < dist[v]:
                    dist[v] = alt
                    prev[v] = u



