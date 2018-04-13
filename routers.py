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
        return
    
    def log_message(self, format, *args):
        return

def ThreadRouter (exitEvent, routerName):
    try:
        httpServer = ThreadedHTTPServer((localHost, routerNameAndPort.get(routerName)), RequestHandlerA)
       
        httpServer.timeout = 0.01           # Make sure not to wait too long when serving requests
        httpServer.daemon_threads = True    # So that handle_request thread exits when current thread exits

        # Poll so that you see the signal to exit as opposed to calling server_forever
        while not exitEvent.isSet():
            httpServer.handle_request()              
    except:
        print('Problem creating router' + routerName + '.')
    
    httpServer.server_close()
    sys.exit()




if __name__ == '__main__':
    try:
        exitEvent = threading.Event() # Set this upon keyboard interrupt to let the threads know they have to exit
        exitEvent.clear()             # Make sure the evebt is clear initially
        
        # Create as many threads as the number of routers
        A = threading.Thread(target=ThreadRouter, args=(exitEvent, 'A'))
        B = threading.Thread(target=ThreadRouter, args=(exitEvent, 'B'))
        C = threading.Thread(target=ThreadRouter, args=(exitEvent, 'C'))
        D = threading.Thread(target=ThreadRouter, args=(exitEvent, 'D'))
        E = threading.Thread(target=ThreadRouter, args=(exitEvent, 'E'))
        F = threading.Thread(target=ThreadRouter, args=(exitEvent, 'F'))
        G = threading.Thread(target=ThreadRouter, args=(exitEvent, 'G'))
        L = threading.Thread(target=ThreadRouter, args=(exitEvent, 'L'))
        H = threading.Thread(target=ThreadRouter, args=(exitEvent, 'H'))

        # Start the routers
        A.start()
        B.start()
        C.start()
        D.start()
        E.start()
        F.start()
        G.start()
        L.start()
        H.start()
    except:
        print ("Error: unable to start routers.")


    try:

        # Run forever till keyboard interrupt is caught
        while True:
            pass
    except KeyboardInterrupt:
        exitEvent.set()  # Upon catching keyboard interrupt, let the threads know they have to exit
        
        # Wait for all routers to finish
        A.join()
        B.join()
        C.join()
        D.join()
        E.join()
        F.join()
        G.join()
        L.join() 
        H.join()
                
        sys.exit()