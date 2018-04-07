
# Code obtained from the following website
# http://www.gilles-bertrand.com/2014/03/dijkstra-algorithm-python-example-source-code-shortest-path.html
def dijkstra(graph,src,dest,visited=[],distances={},predecessors={}):
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
        
        print('\n\n') 
        print('shortest path: '+str(path)+" cost="+str(distances[dest]))
        print('\n\n') 
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
        dijkstra(graph, x, dest, visited, distances, predecessors)
        


if __name__ == "__main__":
    
    # For undirected graphs, repeat the edges
    graph = {'s': {'a': 2, 'c': 10},
            'a': {'s': 2, 'b': 7, 'c':9},
            'b': {'a': 7, 'c': 10},
            'c': {'a': 9, 'b': 10, 's': 10}}
    
    dijkstra(graph,'b','c')

   

