import dijkstras
graph = {
            'A': {'B': 4, 'C': 3, 'E': 7},
            'B': {'A': 4, 'C': 5, 'L': 5},
            'C': {'A': 3, 'B': 6, 'D': 11},
            'D': {'C': 11, 'L': 9, 'F': 6, 'G': 10},
            'E': {'A': 7, 'G': 5},
            'F': {'L': 5, 'D': 6},
            'G': {'E': 5, 'D': 10},
            'L': {'B': 5, 'D': 9, 'F': 5}
            }

shortest_path = dijkstras.dijkstra(graph,'A','F')

print(shortest_path)
