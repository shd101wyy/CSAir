# I am using Python version 3.4.3

'''
Define Node class
'''
class Node():
    def __init__(self,
                 info):
        """
        Constructor for Node class
        save necessary information: code, name, countrym continent, timezone, coordinate, population, region
        """

        # Store several information for that place
        self.info = info

        # Flight goes from "self" to destinations
        self.destinations = {}   # key is destination, value is distance

    def connect(self, dest, distance):
        """
        Connect self to that destination to create an edge.
        """
        self.destinations[dest] = distance

    def disconnect(self, dest):
        """
        Disconnect two ports
        """
        if dest in self.destinations:
            self.destinations.pop(dest, None)

