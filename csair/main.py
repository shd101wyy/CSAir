__author__ = 'wangyiyi'
from graph import Graph
from text_based_user_interface import TextBasedUserInterface

#graph = Graph("./data/new_data.json")
graph = Graph()
prog = TextBasedUserInterface(graph)
prog.cmdloop()
#prog.showMenu()
#while(True):
#    prog.showMenu()