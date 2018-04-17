import helper

from socketserver import ThreadingMixIn, TCPServer, BaseRequestHandler
import threading
import sys
import time
import socket
import pickle


# ---------------------------
# Router and Path Information
# ---------------------------

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
pathAnnToJan = helper.dijkstras(graph,'F','A', visited=[], distances={}, predecessors={})
pathAnnToJan.insert(0, 'Ann')
pathAnnToJan.append('Jan')
pathJanToAnn = pathAnnToJan[::-1]

pathJanToChan = helper.dijkstras(graph,'E','F', visited=[], distances={}, predecessors={})
pathJanToChan.insert(0, 'Jan')
pathJanToChan.append('Chan')
pathChanToJan = pathJanToChan[::-1]

pathAnnToChan = helper.dijkstras(graph,'E','A', visited=[], distances={}, predecessors={})
pathAnnToChan.insert(0, 'Ann')
pathAnnToChan.append('Chan')
pathChanToAnn = pathAnnToChan[::-1]

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

# Everything should be local, make sure all ports are under this IP
localHost = "127.0.0.1"


# -----------------------------------------------------------------------------
# This class can be instantiated to create a multithreaded server multithreaded 
# -----------------------------------------------------------------------------
class ThreadedTCPServer(ThreadingMixIn, TCPServer):
    """Handle requests in a separate thread."""
    

# -----------------------------------------------------
# Request handler for the server portion of the routers
# -----------------------------------------------------
def TCPHandler(routerName):
    class RequestHandler(BaseRequestHandler):
        
        def handle(self):
        
            # self.request is the TCP socket connected to the client
            data = self.request.recv(1024)
            data = data.decode()

            print(data)
            print(routerName + '\n\n\n')

            # Identify who the packet is to
            if data == "To Jan":

                # Identify which router the packet is at and send it to the next relevant
                nextRouterIndex = pathAnnToJan.index(routerName) + 1

                # Make sure not to get index out of bounds
                if nextRouterIndex < len(pathAnnToJan):
                    nextRouterName = pathAnnToJan[nextRouterIndex]
                    nextRouterPort = namesAndPorts.get(nextRouterName)  

                    try:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        
                        # Connect to server and send data
                        sock.connect((localHost, nextRouterPort))
                        data = "To Jan"
                        sock.sendall(data.encode())
                    finally:
                        sock.close()    
            return

    return RequestHandler


# ------------------------------------------
# Function for the router threads to execute
# ------------------------------------------
def ThreadRouter (exitEvent, routerName):
    try:
        RequestHandler = TCPHandler(routerName)
        server = ThreadedTCPServer((localHost, namesAndPorts.get(routerName)), RequestHandler)
       
        server.timeout = 0.01           # Make sure not to wait too long when serving requests
        server.daemon_threads = True    # So that handle_request thread exits when current thread exits

        # Poll so that you see the signal to exit as opposed to calling server_forever
        while not exitEvent.isSet():
            server.handle_request()     

        server.server_close()         
    except:
        print('Problem creating router' + routerName + '.')
    
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