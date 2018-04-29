import random
from socketserver import ThreadingMixIn, TCPServer, BaseRequestHandler
import threading
import sys
import time
import socket
import pickle

# Dictionary for names and associated port numbers
namesAndPorts = {
    'A': 8000,
    'B': 8001,
    'C': 8002,
    'D': 8003,
    'E': 8004,
    'F': 8005,
    'G': 8006,
    'L': 8007,
    'H': 8008,
    'Ann': 1111,
    'Jan': 1100,
    'Chan': 1001
}

# Everything is local
localHost = "127.0.0.1"

# Code obtained from the following website
# http://www.gilles-bertrand.com/2014/03/dijkstra-algorithm-python-example-source-code-shortest-path.html
# Gives the shortest path between two given nodes in a graph
def Dijkstras(graph,src,dest,visited=[],distances={},predecessors={}):
    """ calculates a shortest path tree routed in src """    
    
    # a few sanity checks
    if src not in graph:
        raise TypeError('The root of the shortest path tree cannot be found')
    if dest not in graph:
        raise TypeError('The target of the shortest path cannot be found')    
    
    # ending condition
    if src == dest:
        
        # We build the shortest path and display it
        path = []
        pred = dest
        while pred != None:
            path.append(pred)
            pred = predecessors.get(pred, None)
        return path
    else :     
        
        # if it is the initial run, initializes the cost
        if not visited: 
            distances[src] = 0

        # visit the neighbors
        for neighbor in graph[src] :
            
            # Visit them if they are not visited
            if neighbor not in visited:

                # Calculate the distance from the current node to them and if this distance is 
                # less than the current distance, update it and update pred of neighbor to be current node
                new_distance = distances[src] + graph[src][neighbor]
                if new_distance < distances.get(neighbor,float('inf')):
                    distances[neighbor] = new_distance
                    predecessors[neighbor] = src
        
        # mark as visited
        visited.append(src)
        
        # now that all neighbors have been visited: recurse                         
        # select the non visited node with lowest distance 'x'
        # run Dijskstra with src='x'
        unvisited={}
        for k in graph:
            if k not in visited:
                unvisited[k] = distances.get(k, float('inf'))        
        
        x = min(unvisited, key = unvisited.get)
        path = Dijkstras(graph, x, dest, visited, distances, predecessors)
        return path


# Creates a TCP packet with the necessary fields 
def CreateTCPPacket(sourceID, destinationID, acknowledgementNumber, sequenceNumber, data, urgentPointer, synBit, finBit, rstBit, terBit):
    
    # Creates an empty dict    
    packet = {}
    
    # Calculates the checksum on the data part
    checksum = Checksum(data)

    # Lets the receiver know if the packet is has to deliver urgent data
    urgentPointer = urgentPointer
    # header length is equal to the size of everything in the packet but the data 
    headerLength = len(str(sourceID)) + len(str(destinationID)) + len(str(acknowledgementNumber)) + len(str(sequenceNumber)) + len(str(urgentPointer)) + len(str(synBit)) + len(str(finBit)) + len(str(rstBit)) + len(str(terBit))
                   
    # Append all the fields to the dictionary 
    packet.update({'Source ID': sourceID})
    packet.update({'Destination ID': destinationID})
    packet.update({'Sequence Number': sequenceNumber})
    packet.update({'Acknowledgement Number': acknowledgementNumber})
    packet.update({'Data': data})
    packet.update({'Checksum': checksum})
    packet.update({'Urgent Pointer': urgentPointer})
    packet.update({'Syn Bit': synBit})
    packet.update({'Fin Bit': finBit})
    packet.update({'Rst Bit': rstBit})
    packet.update({'Ter Bit': terBit})
    packet.update({'Header Length': headerLength})

    return packet


# This function will inspect incoming packet and send it to the next relevant node
def PassPacket(shortestPath, routerName, packetOnTheWay):
    
    # Identify which router the packet is at and send it to the next relevant
    nextRouterIndex = shortestPath.index(routerName) + 1

    # Make sure not to get index out of bounds
    if nextRouterIndex < len(shortestPath):
        nextRouterName = shortestPath[nextRouterIndex]
        nextRouterPort = namesAndPorts.get(nextRouterName)  

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Connect to server and send data
            sock.connect((localHost, nextRouterPort))
            sock.sendall(packetOnTheWay)
        
        except ConnectionRefusedError:
            print(nextRouterName + " is offline.")

        finally:
            sock.close()

# Code obtained from the following website
# https://stackoverflow.com/questions/1767910/checksum-udp-calculation-python
# Computes internet checksum
def Checksum(msg):
    s = 0
    for i in range(0, len(msg), 2):
        try:
            w = ord(msg[i]) + (ord(msg[i+1]) << 8)

        # String has an odd number of characters. When this is the case, assume the next letter would have returned zero
        except IndexError:
            w = ord(msg[i]) + (0 << 8)

        s = CarryAroundAdd(s, w)
    return ~s & 0xffff

# Helper function for the checksum function which was obtained from the same website
def CarryAroundAdd(a, b):
    c = a + b
    return (c & 0xffff) + (c >> 16)


# Helper function that reads a given file and return the content
def ReadFile(path):
    with open(path, 'r') as file:
        content = file.readlines()
    
    return content

if __name__ == '__main__':
    print(ReadFile('./Supplemental Text Files/Ann/Ann-_Chan.txt'))


# Helper function to write log messages to the relevant log file
def WriteToLogFile(path, mode, data):
    with open(path, mode) as file:
        file.write(data)


# Helper function to get the dictionary key given its corresponding value
def GetKeyFromValue(value):
    for key in namesAndPorts:
        if namesAndPorts.get(key) == value:
            return key





   

