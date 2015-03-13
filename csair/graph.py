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

    ## generate node according to metros data
    def generateNodes(self, metros):
        for info in metros:
            node = Node(info) # create Node
            self.nodes[info["code"]] = node # add to node list

    ## build routes by connecting nodes
    def connectNodes(self, routes):
        for info in routes:
            distance = info["distance"]     # get distance
            ports = info["ports"]             # get 2 codes of ports
            source = self.nodes[ports[0]]
            destination = self.nodes[ports[1]]
            source.connect(destination, distance)     # connect source and destination
            # the json file now represents directed graph instead of undirected graph
            # destination.connect(source, distance)     # connect destination to source as well

    ## generate url to visualize the map
    def generateURL(self):
        # eg: http://www.gcmap.com/mapui?P=LIM-MEX,+LIM-BOG,+MEX-LAX
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

    ## Visualize CSAir's route map
    def visualizeCSAirRouteMap(self):
        webbrowser.open(self.generateURL())

    '''
        find city by name
        if no such city is found, return False
    '''
    def getCityByNameOrCode(self, name_or_code):
        name_or_code = name_or_code.lower()
        for city_code in self.nodes:
            city = self.nodes[city_code]
            if city.info["name"].lower() == name_or_code or city.info["code"].lower() == name_or_code:
                return city
        return False

    '''
        remove a city from the graph, given city name or city code
        return True if we find the city to remove
        otherwise return False
    '''
    def removeCity(self, city_name_or_code):
        city = self.getCityByNameOrCode(city_name_or_code)
        if city == False:
            return False # didnt find city
        else:
            destinations = city.destinations
            for dest in destinations:
                dest.disconnect(city)  # disconnect
            self.nodes.pop(city.info["code"], None)
            return True # successfully removed city from current graph


    '''
        remove a route
        given 2 params: source and destination
        if there is such route, remove it and return True
        otherwise return false
    '''
    def removeRoute(self, source_name_or_code, dest_name_or_code):
        src = self.getCityByNameOrCode(source_name_or_code)
        dest = self.getCityByNameOrCode(dest_name_or_code)
        if src == False or dest == False: # invalid city
            return False
        if dest in src.destinations:
            src.disconnect(dest)
            return True  # removed route
        else:
            return False # no such route




    '''
        Convert current graph to JSON data format
    '''
    def convertGraphToJSON(self):
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

    '''
        Save the graph to json file
    '''
    def saveGraph(self, file_name):
        with open("./data/" + file_name, 'w') as outfile:
            json.dump(self.convertGraphToJSON(), outfile, indent=4, sort_keys=True)

    '''
        Add a city to graph
    '''
    def addCity(self, info):
        self.nodes[info["code"]] = Node(info)

    '''
        Add a route between two cities
        return True if the route is created; otherwise return False
    '''
    def addRoute(self, src_name_or_code, dest_name_or_code, distance):
        src = self.getCityByNameOrCode(src_name_or_code)
        dest = self.getCityByNameOrCode(dest_name_or_code)
        if src == False or dest == False: # didn't find city
            return False
        else:
            src.connect(dest, distance)
            return True

    '''
        load a json file
    '''
    def loadJSON(self, file_name):
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

    ## Constructor: initiate graph
    ## Load JSON file, parser JSON data
    ## Generate Graph by JSON data
    def __init__(self, file_name=None, json_data=None):
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





## x = Graph("./data/data.json")