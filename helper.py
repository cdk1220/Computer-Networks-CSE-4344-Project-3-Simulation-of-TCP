import random

# Code obtained from the following website
# http://www.gilles-bertrand.com/2014/03/dijkstra-algorithm-python-example-source-code-shortest-path.html
# Gives the shortest path between two given nodes in a graph
def dijkstras(graph,src,dest,visited=[],distances={},predecessors={}):
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
        path = dijkstras(graph, x, dest, visited, distances, predecessors)
        return path


# Creates a TCP packet with the necessary fields 
def CreateTCPPacket(sourceID, destinationID, sequenceNumber, data, urgentPointer, synBit, finBit, headerLength):
    
    # Creates an empty dict    
    packet = {}
    
    # Gets the length of the data
    dataSize = len(data)
    
    # Ackknowledgment number is the next byte that the receiving end is expecting   
    acknowledgementNumber = sequenceNumber + dataSize

    # Calculates the checksum on the data part
    checksum = None

    # Lets the receiver know if the packet is has to deliver urgent data
    urgentPointer = urgentPointer
    
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
    packet.update({'Header Length': headerLength})

    return packet


# Code obtained from the following website
# https://stackoverflow.com/questions/1767910/checksum-udp-calculation-python
# Computes internet checksum
def checksum(msg):
    s = 0
    for i in range(0, len(msg), 2):
        w = ord(msg[i]) + (ord(msg[i+1]) << 8)
        s = carry_around_add(s, w)
    return ~s & 0xffff

# Helper function for the checksum function which was obtained from the same website
def carry_around_add(a, b):
    c = a + b
    return (c & 0xffff) + (c >> 16)




   

