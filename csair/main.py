__author__ = 'wangyiyi'
from graph import Graph
from text_based_user_interface import TextBasedUserInterface

print("\n\nHi there! Welcome to use CSAir information query system\n")

graph = Graph("./data/data.json")
prog = TextBasedUserInterface(graph)
prog.showMenu()
while(True):
    prog.processQuery()