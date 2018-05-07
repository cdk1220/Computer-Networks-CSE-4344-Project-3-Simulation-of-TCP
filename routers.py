import helper

from socketserver import ThreadingMixIn, TCPServer, BaseRequestHandler
import threading
import sys
import time
import socket
import pickle
import datetime
import random


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

pathToAirForceJanLogFile = './Supplemental Text Files/AirForceJanLogFile.txt'

# Calculating the shortest paths to and from
pathAnnToJan = helper.Dijkstras(graph,'F','A', visited=[], distances={}, predecessors={})
pathAnnToJan.insert(0, 'Ann')
pathAnnToJan.append('Jan')
pathJanToAnn = pathAnnToJan[::-1]
print("pathAnnToJan = " + str(pathAnnToJan))
print("PathJanToAnn = "+ str(pathJanToAnn) + "\n\n")

pathJanToChan = helper.Dijkstras(graph,'E','F', visited=[], distances={}, predecessors={})
pathJanToChan.insert(0, 'Jan')
pathJanToChan.append('Chan')
pathChanToJan = pathJanToChan[::-1]
print("pathJanToChan = "+ str(pathJanToChan))
print("pathChanToJan = "+ str(pathChanToJan)+ "\n\n")

pathAnnToChan = helper.Dijkstras(graph,'E','A', visited=[], distances={}, predecessors={})
pathAnnToChan.insert(0, 'Ann')
pathAnnToChan.append('Chan')
pathChanToAnn = pathAnnToChan[::-1]
print("pathAnnToChan = " + str(pathAnnToChan))
print("pathChanToAnn = " + str(pathChanToAnn)+ "\n\n")

# Everything should be local, make sure all ports are under this IP
localHost = helper.localHost


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
            packetOnTheWay = self.request.recv(4096)
            packet = pickle.loads(packetOnTheWay)
            print(routerName + '\n' + str(packet) + '\n')
            
            sourceID = packet.get('Source ID')
            destinationID = packet.get('Destination ID')

            # Packet is from Ann to Jan
            if sourceID == helper.namesAndPorts.get('Ann') and destinationID == helper.namesAndPorts.get('Jan'):
                helper.PassPacket(pathAnnToJan, routerName, packetOnTheWay)
            
            # Packet is from Jan to the Airforce
            elif sourceID == helper.namesAndPorts.get('Jan') and destinationID == helper.namesAndPorts.get('H'):
                
                sourceID = helper.namesAndPorts.get('H')
                destinationID = helper.namesAndPorts.get('Jan')                              # The destination of the packet about to be sent is where the original packet came from
                sequenceNumber = random.randint(10000, 99999)                                # First time talking to Jan, create new sequence number                                                                                  
                                                                                             # Next byte of data that you want
                acknowledgementNumber = packet.get('Sequence Number')+ len(packet.get('Data'))    
                packetData = 'Success!'                                                      # Second step of three way handshake, therefore no data
                urgentPointer = 0                                                            # Not urgent as this is connection setup
                synBit = 0                                                                   # Syn bit is zero
                finBit = 0                                                                   # Trying to finish connection
                rstBit = 0                                                                   # Not trying to reset connection, therefore 0
                terBit = 0                                                                   # Not trying to terminate connection, therefore 0

                # Create packet with above data
                responsePacket = helper.CreateTCPPacket(sourceID, destinationID, acknowledgementNumber, sequenceNumber, packetData, urgentPointer, synBit, finBit, rstBit, terBit)

                # Send packet
                helper.SerializeAndSendPacket(responsePacket, destinationID)

                # Log what happened at the airport router
                timeStamp = time.time()
                data = datetime.datetime.fromtimestamp(timeStamp).strftime('%Y-%m-%d %H:%M:%S') + '\n'
                data = data + 'Received following line.\n'
                data = data + packet.get('Data')
                data = data + 'Acknowledgement sent along with below line.\n'
                data = data + packetData + '\n\n'
                helper.WriteToLogFile(pathToAirForceJanLogFile, 'w', data)

                print('Airforce to Jan: Success!')
            
            # Packet is from Jan to Ann
            elif sourceID == helper.namesAndPorts.get('Jan') and destinationID == helper.namesAndPorts.get('Ann'):    
                helper.PassPacket(pathJanToAnn, routerName, packetOnTheWay)
            
            # Packet is from Jan to Chan
            elif sourceID == helper.namesAndPorts.get('Jan') and destinationID == helper.namesAndPorts.get('Chan'):    
                helper.PassPacket(pathJanToChan, routerName, packetOnTheWay)

            # Packet is from Chan to Jan
            elif sourceID == helper.namesAndPorts.get('Chan') and destinationID == helper.namesAndPorts.get('Jan'):    
                helper.PassPacket(pathChanToJan, routerName, packetOnTheWay)

            # Packet is from Ann to Chan
            elif sourceID == helper.namesAndPorts.get('Ann') and destinationID == helper.namesAndPorts.get('Chan'):    
                helper.PassPacket(pathAnnToChan, routerName, packetOnTheWay)
            
            # Packet is from Jan to Ann
            elif sourceID == helper.namesAndPorts.get('Chan') and destinationID == helper.namesAndPorts.get('Ann'):    
                helper.PassPacket(pathChanToAnn, routerName, packetOnTheWay)

            

            # Packet has no right direction
            else:
                print('Packet has no right direction' + '\n\n')

            return

    return RequestHandler


# ------------------------------------------
# Function for the router threads to execute
# ------------------------------------------
def ThreadRouter (exitEvent, routerName):
    try:
        RequestHandler = TCPHandler(routerName)
        server = ThreadedTCPServer((localHost, helper.namesAndPorts.get(routerName)), RequestHandler)
       
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
