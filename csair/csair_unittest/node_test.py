__author__ = 'wangyiyi'

import sys
sys.path.insert(0, '../')

from unittest import TestCase
from csair.node import Node

class TestNode(TestCase):

    ## test node constructor
    def test_constructor(self):
        simple_info = {
        "   code" : "SCL" ,
			"name" : "Santiago" ,
			"country" : "CL" ,
			"continent" : "South America" ,
			"timezone" : -4 ,
			"coordinates" : {"S" : 33, "W" : 71} ,
			"population" : 6000000 ,
			"region" : 1
        }

        ## Create Node object
        node = Node(simple_info)

        ## test info stored correctly
        self.assertEqual(simple_info, node.info, "Node constructor error")

        ## test destinations initialized correctly
        self.assertEqual({}, node.destinations, "Node destinations property initialized incorrectly")

    def test_connect(self):
        ## Create Node Object
        source = Node({
        "   code" : "SCL" ,
			"name" : "Santiago" ,
			"country" : "CL" ,
			"continent" : "South America" ,
			"timezone" : -4 ,
			"coordinates" : {"S" : 33, "W" : 71} ,
			"population" : 6000000 ,
			"region" : 1
        })

        route = {
			"ports" : ["SCL" , "LIM"] ,
			"distance" : 2453};

        ## Create Node Object
        dest = Node({
			"code" : "LIM" ,
			"name" : "Lima" ,
			"country" : "PE" ,
			"continent" : "South America" ,
			"timezone" : -5 ,
			"coordinates" : {"S" : 12, "W" : 77} ,
			"population" : 9050000 ,
			"region" : 1
		})

        ## connect source to dest
        source.connect(dest, route["distance"])

        ## check source connected
        self.assertEqual(1, len(source.destinations.keys()))
        self.assertEqual(0, len(dest.destinations.keys()))
        self.assertEqual(route["distance"], source.destinations[dest])

    def test_disconnect(self):
        ## Create Node Object
        source = Node({
        "   code" : "SCL" ,
			"name" : "Santiago" ,
			"country" : "CL" ,
			"continent" : "South America" ,
			"timezone" : -4 ,
			"coordinates" : {"S" : 33, "W" : 71} ,
			"population" : 6000000 ,
			"region" : 1
        })

        route = {
			"ports" : ["SCL" , "LIM"] ,
			"distance" : 2453};

        ## Create Node Object
        dest = Node({
			"code" : "LIM" ,
			"name" : "Lima" ,
			"country" : "PE" ,
			"continent" : "South America" ,
			"timezone" : -5 ,
			"coordinates" : {"S" : 12, "W" : 77} ,
			"population" : 9050000 ,
			"region" : 1
		})

        ## connect source to dest
        source.connect(dest, route["distance"])

        ## check source connected
        self.assertEqual(1, len(source.destinations.keys()))
        self.assertEqual(0, len(dest.destinations.keys()))
        self.assertEqual(route["distance"], source.destinations[dest])

        ## disconnect dest from source
        source.disconnect(dest)

        ## check disconnection
        self.assertEqual(0, len(source.destinations.keys()))