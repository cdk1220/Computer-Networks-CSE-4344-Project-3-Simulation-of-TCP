
# Code obtained from the following website
# http://www.gilles-bertrand.com/2014/03/dijkstra-algorithm-python-example-source-code-shortest-path.html
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

# creates a TCP packet with the necessary fields 
def TCP_Packet(source, destination, data):
    # creates an empty dict    
    packet = {}
    # gets the length of the data
    data_size = len(data)
    # increases the data size to create the ack number     
    ackNo = data_size + 1
    # create a 5 digit random number for the seq number 
    seqNo = random.randint(10000,99999)
    # append all the fields to the dictionary 
    packet.update({'sourceID':source})
    packet.update({'destnID':destination})
    packet.update({'ackNo':ackNo})
    packet.update({'seqNo':seqNo})
    packet.update({'data':data})


    # return the packet dictionary 
    return packet
      



   

