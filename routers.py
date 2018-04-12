import dijkstras

from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import threading
import sys
from urllib.parse import urlparse
import glob
import os
import time

# -----------------------------------------------------------------------------
# This class can be instantiated to create a multithreaded server multithreaded 
# -----------------------------------------------------------------------------
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


# Network layout of the routers as given in the project description
graph = {
    'A': {'B': 4, 'C': 3, 'E': 7},
    'B': {'A': 4, 'C': 6, 'L': 5},
    'C': {'A': 3, 'B': 6, 'D': 11},
    'D': {'C': 11, 'L': 9, 'F': 6, 'G': 10},
    'E': {'A': 7, 'G': 5},
    'F': {'L': 5, 'D': 6},
    'G': {'E': 5, 'D': 10},
    'L': {'B': 5, 'D': 9, 'F': 5}
}


# Calculating the shortest paths to and from
pathAnnToJan = dijkstras.dijkstras(graph,'F','A', visited=[], distances={}, predecessors={})
pathJanToAnn = pathAnnToJan[::-1]

pathJanToChan = dijkstras.dijkstras(graph,'E','F', visited=[], distances={}, predecessors={})
pathChanToJan = pathJanToChan[::-1]

pathAnnToChan = dijkstras.dijkstras(graph,'E','A', visited=[], distances={}, predecessors={})
pathChanToAnn = pathAnnToChan[::-1]

# Dictionary for router name and associated port number
routerNameAndPort = {
    'A': 8000,
    'B': 8001,
    'C': 8002,
    'D': 8003,
    'E': 8004,
    'F': 8005,
    'G': 8006,
    'L': 8007,
    'H': 8008
}



