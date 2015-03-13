__author__ = 'wangyiyi'

import sys
sys.path.insert(0, '../')

from unittest import TestCase
from csair.node import Node
from csair.graph import Graph

class TestGraph(TestCase):
    def testGenerateNode(self):
        ## init graph
        g = Graph("../data/data.json")

        ## test graph node create correctly
        self.assertEqual(48, len(g.nodes.keys()))

        ## test some keys
        self.assertEqual(True, "SCL" in g.nodes.keys())
        self.assertEqual(True, "PEK" in g.nodes.keys())
        self.assertEqual(False, "ASDAS" in g.nodes.keys())


    def testConnectNodes(self):
        ## init graph
        g = Graph("../data/data.json")

        self.assertEqual(2, len(g.nodes["LIM"].destinations.keys()))
        self.assertEqual(1, len(g.nodes["SCL"].destinations.keys()))
        self.assertEqual(3, len(g.nodes["THR"].destinations.keys()))
        self.assertEqual(4, len(g.nodes["SHA"].destinations.keys()))

    def testGenerateURL(self):
        ## init graph
        g = Graph("", json_data={
            "metros": [
                {
			        "code" : "SCL" ,
			        "name" : "Santiago" ,
			        "country" : "CL" ,
			        "continent" : "South America" ,
			        "timezone" : -4 ,
			        "coordinates" : {"S" : 33, "W" : 71} ,
			        "population" : 6000000 ,
			        "region" : 1
		        },
                {
                    "code" : "LIM" ,
                    "name" : "Lima" ,
                    "country" : "PE" ,
                    "continent" : "South America" ,
                    "timezone" : -5 ,
                    "coordinates" : {"S" : 12, "W" : 77} ,
                    "population" : 9050000 ,
                    "region" : 1
                }],
                "routes": [
                    {
			            "ports" : ["SCL" , "LIM"] ,
			            "distance" : 2453
		            }
                ]
        })

        self.assertEqual("http://www.gcmap.com/mapui?P=LIM-SCL,+SCL-LIM", g.generateURL())