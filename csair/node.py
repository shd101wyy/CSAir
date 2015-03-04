# I am using Python version 3.4.3

'''
Define Node class
'''
class Node():
    # Constructor for Node class
    # save necessary information: code, name, countrym continent, timezone, coordinate, population, region
    def __init__(self,
                 info):

        # Store several information for that place
        self.info = info

        # Flight goes from "self" to destinations
        self.destinations = {}   # key is destination, value is distance

    # Connect self to that destination to create an edge.
    def connect(self, dest, distance):
        self.destinations[dest] = distance

    # Disconnect two ports
    def disconnect(self, dest):
        if dest in self.destinations:
            self.destinations.remove(dest)

