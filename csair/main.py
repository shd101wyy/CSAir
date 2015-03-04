__author__ = 'wangyiyi'
from graph import Graph
from query import Query

print("\n\nHi there! Welcome to use CSAir information query system\n")

graph = Graph("./data/data.json")
query = Query(graph)
query.showMenu()
while(True):
    query.processQuery()