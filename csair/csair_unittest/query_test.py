__author__ = 'wangyiyi'
import sys
sys.path.insert(0, '../')

from unittest import TestCase
from csair.query import Query
from csair.graph import Graph
class TestQuery(TestCase):

    # test getting all cities
    def testGetAllCities(self):
        graph = Graph("../data/data.json")
        query = Query(graph)
        self.assertEqual(48, len(query.getAllCities().keys()))
        self.assertEqual(True, "SCL" in query.getAllCities())
        self.assertEqual(True, "MEX" in query.getAllCities())
        self.assertEqual(False, "MASD" in query.getAllCities())

    # test route information
    def testQueryRouteInfo(self):
        graph = Graph("",
            {
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
                    } , {
                        "code" : "LIM" ,
                        "name" : "Lima" ,
                        "country" : "PE" ,
                        "continent" : "South America" ,
                        "timezone" : -5 ,
                        "coordinates" : {"S" : 12, "W" : 77} ,
                        "population" : 9050000 ,
                        "region" : 1
                    }
                ],
                "routes": [
                    {
                        "ports" : ["SCL" , "LIM"] ,
                        "distance" : 2453
                    }
                ]
            })
        query = Query(graph)
        query.queryRouteInfo()
        self.assertEqual(query.getAllCities()["LIM"], query.biggest_city) # check biggest city
        self.assertEqual(query.getAllCities()["SCL"], query.smallest_city) # check smalllest city
        self.assertEqual(2453, query.average_distance) # check average distance
        self.assertEqual({"from": query.getAllCities()["SCL"], "to": query.getAllCities()["LIM"], "distance": 2453}, query.longest_single_flight) # check longest single flight
        self.assertEqual({"from": query.getAllCities()["SCL"], "to": query.getAllCities()["LIM"], "distance": 2453}, query.shortest_single_flight) # check shortest single flight
        self.assertEqual(True, "South America" in query.continents) # check continents
        self.assertEqual(2, len(query.continents["South America"]))
        self.assertEqual([query.getAllCities()["SCL"]], query.hub_cites) # check outbound cites
        self.assertEqual(1, query.max_num_of_outbound_flights )