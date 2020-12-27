from py2neo import Graph,Node,NodeSelector

global users
global u
global uid
global pid
global movie
global mediaType
global searchRes
global g
global userType

g = Graph('http://127.0.0.1:7474/db/data',user='neo4j',password='123')
