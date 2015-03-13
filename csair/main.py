__author__ = 'wangyiyi'
from graph import Graph
from text_based_user_interface import TextBasedUserInterface

if __name__ == '__main__':
    #graph = Graph("./data/new_data.json")
    graph = Graph()
    prog = TextBasedUserInterface(graph)
    prog.cmdloop()