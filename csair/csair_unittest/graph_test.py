__author__ = 'wangyiyi'

import sys
sys.path.insert(0, '../')

from unittest import TestCase
from csair.node import Node
from csair.graph import Graph
import json

class TestGraph(TestCase):
    def testGenerateNode(self):
        ## init graph
        g = Graph("../data/new_data.json")

        ## test graph node create correctly
        self.assertEqual(48, len(g.nodes.keys()))

        ## test some keys
        self.assertEqual(True, "SCL" in g.nodes.keys())
        self.assertEqual(True, "PEK" in g.nodes.keys())
        self.assertEqual(False, "ASDAS" in g.nodes.keys())


    def testConnectNodes(self):
        ## init graph
        g = Graph(file_name="../data/new_data.json")

        self.assertEqual(3, len(g.nodes["LIM"].destinations.keys()))
        self.assertEqual(1, len(g.nodes["SCL"].destinations.keys()))
        self.assertEqual(5, len(g.nodes["THR"].destinations.keys()))
        self.assertEqual(5, len(g.nodes["SHA"].destinations.keys()))

    def testGenerateURL(self):
        ## init graph
        g = Graph(json_data={
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

        self.assertEqual("http://www.gcmap.com/mapui?P=SCL-LIM", g.generateURL())

    def testRemoveCity(self):
        """
        Test remove city
        """
        g = Graph(json_data={
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

        g.removeCity("LIM")
        self.assertEqual(1, len(g.nodes.keys()))
        self.assertEqual(0, len(g.nodes["SCL"].destinations.keys()))

    def testRemoveRoute(self):
        """
        Test remove a route
        """
        g = Graph(json_data={
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
        invalid_remove = g.removeRoute("LIM", "SCL")
        valid_remove = g.removeRoute("SCL", "LIM")
        self.assertEqual(False, invalid_remove)
        self.assertEqual(True,  valid_remove)
        self.assertEqual(2, len(g.nodes.keys()))
        self.assertEqual(0, len(g.nodes["SCL"].destinations.keys()))

    def testAddCity(self):
        """
        Test add city
        """
        g = Graph(json_data={
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
        g.addCity({"code": "Yoo", "name": "Yooo", "country":"UK", "continent": "Europe", "timezone": -4, "coordinates": {"S": 1, "W": 2}, "population": 10, "region": 12})
        self.assertEqual(3, len(g.nodes.keys()))
        self.assertNotEqual(False, g.getCityByNameOrCode("Yoo"))
        self.assertNotEqual(False, g.getCityByNameOrCode("Yooo"))

    def testJSONGeneration(self):
        json_data = {
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
		        }],
                "routes": []
        }
        g = Graph(json_data=json_data)
        self.assertEqual(g.convertGraphToJSON(), json_data)

    def testAddRoute(self):
        """
        test add route
        """
        g = Graph(json_data={
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
        g.addRoute("LIM", "SCL", 2000)
        self.assertEqual(1, len(g.nodes["LIM"].destinations.keys()))
        self.assertIn(g.nodes["SCL"], g.nodes["LIM"].destinations)

    def testShortestPath(self):
        """
            test shortest path
        """
        g = Graph("../data/new_data.json")

        result =  g.shortestPath("BOG", "SAO")
        self.assertEqual(2, len(result))

        result = g.shortestPath("JNB", "ALG")
        self.assertEqual(5, len(result))

        result = g.shortestPath("LAX", "SYD")
        self.assertEqual(2, len(result))

        result = g.shortestPath("Yooooo", "LAX")
        self.assertEqual(False, result)
