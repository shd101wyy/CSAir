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

    # test biggest city
    def testGetBiggestCity(self):
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
            }
        g = Graph(json_data=json_data)
        query = Query(g)
        self.assertEqual(query.getAllCities()["LIM"], query.biggest_city)

    # test smallest city
    def testGetSmallestCity(self):
        json_data =  {
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
            }
        g = Graph(json_data=json_data)
        query = Query(g)
        self.assertEqual(query.getAllCities()["LIM"], query.biggest_city)

    # test average distance
    def testAverageDistance(self):
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
            }
        g = Graph(json_data=json_data)
        query = Query(g)
        self.assertEqual(2453, query.average_distance) # check average distance

    # test longest single flight
    def testLongestSingleFlight(self):
        json_data =  {
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
            }
        g = Graph(json_data=json_data)
        query = Query(g)
        self.assertEqual({"from": query.getAllCities()["SCL"], "to": query.getAllCities()["LIM"], "distance": 2453}, query.longest_single_flight) # check longest single flight

    # test shortest single flight
    def testShortestSingleFlight(self):
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
            }
        g = Graph(json_data=json_data)
        query = Query(g)
        self.assertEqual({"from": query.getAllCities()["SCL"], "to": query.getAllCities()["LIM"], "distance": 2453}, query.shortest_single_flight) # check shortest single flight


    # test continents
    def testContinents(self):
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
            }
        g = Graph(json_data=json_data)
        query = Query(g)
        self.assertEqual(True, "South America" in query.continents) # check continents
        self.assertEqual(2, len(query.continents["South America"]))

    # test hub city
    def testHubCity(self):
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
            }
        g = Graph(json_data=json_data)
        query = Query(g)
        self.assertEqual([query.getAllCities()["SCL"]], query.hub_cities) # check outbound cites
        self.assertEqual(1, query.max_num_of_outbound_flights)

    def testQueryRouteInfo(self):
        """
        Test query route info
        test: total distance, total cost, total time
        """
        g = Graph("../data/new_data.json")
        query = Query(g)
        self.assertEqual(False, query.queryRouteInfo(["LIM", "TYO"]))
        self.assertEqual(False, query.queryRouteInfo(["SCL2", "SCL"]))
        result = query.queryRouteInfo(["SCL", "LIM"])
        self.assertEqual(2453, result["total_distance"])
        self.assertEqual(858.55, result["total_cost"])
        self.assertEqual("3.80", (str(result["total_time"]))[:4])

        result = query.queryRouteInfo(["JNB", "FIH", "KRT", "CAI", "BGW"])
        self.assertEqual(11068, result["total_distance"])
        self.assertEqual(3043, int(result["total_cost"]))
        self.assertEqual("22.3", (str(result["total_time"]))[:4])