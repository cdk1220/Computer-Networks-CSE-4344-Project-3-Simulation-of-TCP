import dijkstras

from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import threading
import sys
from urllib.parse import urlparse
import glob
import os
import time

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

# Everything should be local, make sure all ports are under this IP
localHost = "127.0.0.1"

# -----------------------------------------------------------------------------
# This class can be instantiated to create a multithreaded server multithreaded 
# -----------------------------------------------------------------------------
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

class RequestHandlerA(BaseHTTPRequestHandler):
    def do_GET(self):
                
        self.send_response(200)
        self.end_headers()

        print("\n-------------------- Done Processing -----------------------\n\n") 

        return

def ThreadRouterA (e):
    try:
        httpServer = ThreadedHTTPServer((localHost, 8000), RequestHandlerA)
        httpServer.timeout = 0.01
        httpServer.daemon_threads = True

        while not e.isSet():
            httpServer.handle_request()
               
    # Upon encountering a keyboard interrupt, close the server before existing 
    except:
        print('Problem')




if __name__ == '__main__':
    try:
        exitEvent = threading.Event() # Set this upon keyboard interrupt to let the threads know they have to exit
        exitEvent.clear()             # Make sure the evebt is clear initially
        
        A = threading.Thread(target=ThreadRouterA, args=(exitEvent,))
        A.start()
    except:
        print ("Error: unable to start thread")

    try:
        # Run forever till keyboard interrupt is caught
        while True:
            pass
    except KeyboardInterrupt:
        exitEvent.set()  # Upon catching keyboard interrupt, let the threads know they have to exit
        A.join()         # Wait till thread A finishes
        sys.exit()