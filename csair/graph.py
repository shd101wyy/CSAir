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



    ## Constructor: initiate graph
    ## Load JSON file, parser JSON data
    ## Generate Graph by JSON data
    def __init__(self, file_name, json_data=None):
        if json_data == None:
            json_file = open(file_name) # load JSON file
            json_data = json.load(json_file) # parse JSON data
            json_file.close() # close file

        self.nodes = {} # key is code of the port, value is the node

        # Genearte nodes
        metros = json_data["metros"]
        self.generateNodes(metros)

        # Generate connections
        routes = json_data["routes"]
        self.connectNodes(routes)




## x = Graph("./data/data.json")