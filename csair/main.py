__author__ = 'wangyiyi'
from graph import Graph
from query import Query

print("\n\nHi there! Welcome to use CSAir information query system\n")

graph = Graph("./data/data.json")
#graph.visualizeCSAirRouteMap()
query = Query(graph)
query.showMenu()
while(True):
    query.processQuery()