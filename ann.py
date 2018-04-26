import helper
import random
import datetime
import time
from socketserver import ThreadingMixIn, TCPServer, BaseRequestHandler
import threading
import sys
import time
import socket
import pickle

# Everything should be local, make sure all ports are under this IP
localHost = "127.0.0.1"

# Port number that will ann will be listening to is her ID + 1000
portListeningTo = 1111

# Ann will always be dumping her messages to the router she is connected to
portTalkingTo = 8000

# Paths to where communication files are stored
pathToAnnToChanFile = './Supplemental Text Files/Ann/Ann-_Chan.txt'
pathToAnnToJanFile = './Supplemental Text Files/Ann/Ann-_Jan.txt'

# Paths to where the resulting log files from communication will be stored
pathChanToAnnLogFile = './Supplemental Text Files/Ann/ChanToAnnLog.txt'
pathJanToAnnLogFile = './Supplemental Text Files/Ann/JanToAnnLog.txt'

# Sequence Numbers for initial packets
initialSequenceNumberAnnToJan = random.randint(10000, 99999)
initialSequenceNumberAnnToChan = random.randint(10000, 99999)

# Flag variables to check and see if a packet is sent only after receiving the acknowledgement 
packetSentAnnToJan = False
packetSentAnnToChan = False

# Reading communication material from the text files
contentAnnToJan = helper.ReadFile(pathToAnnToJanFile)
contentAnnToChan = helper.ReadFile(pathToAnnToChanFile)

# ---------------------------------------------------------------
# This class can be instantiated to create a multithreaded server
# ---------------------------------------------------------------
class ThreadedTCPServer(ThreadingMixIn, TCPServer):
    """Handle requests in a separate thread."""
    

# ----------------------------------------------------
# Request handler for the server portion of the agents
# ----------------------------------------------------
class TCPRequestHandler(BaseRequestHandler):
    def handle(self):
    
        # self.request is the TCP socket connected to the client
        incomingPacket = self.request.recv(4096)

        receivedFrom = helper.GetKeyFromValue(incomingPacket.get('Source ID'))

        # When someone else is trying to setup connection with us
        if incomingPacket.get('Syn Bit') == 1 and incomingPacket.get('Acknowledgement Number') == -1:
            
            # Send TCP packet with syn bit still one and acknowledgement number as 1 + sequence number. Also, create your own sequence number
            sourceID = portListeningTo                                            # The port listening to
            destinationID = incomingPacket.get('Source ID')                       # The destination of the packet about to be sent is where the original packet came from
            sequenceNumber = random.randint(10000, 99999)                         # First time talking to client, create new sequence number
            acknowledgementNumber = incomingPacket.get('Sequence Number') + 1     # Client wanted to connect, therefore no data in the original packet, ack # will be one more than client seq #
            packetData = ''                                                       # Second step of three way handshake, therefore no data
            urgentPointer = 0                                                     # Not urgent as this is connection setup
            synBit = 1                                                            # Syn bit has to be one for the second step of threeway handshake
            finBit = 0                                                            # Not trying to finish connection, therefore 0                                               
            rstBit = 0                                                            # Not trying to reset connection, therefore 0
            terBit = 0                                                            # Not trying to terminate connection, therefore 0
            headerLength = 0                                                      # FIGURE THIS OUT???????????????????????????????????????????
             
            # Create packet with above data
            packet = helper.CreateTCPPacket(sourceID, destinationID, acknowledgementNumber, sequenceNumber, packetData, urgentPointer, 
                                            synBit, finBit, rstBit, terBit, headerLength)
            
            # Try and send it
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect(localHost, portTalkingTo)
                sock.sendall(packet)
            finally:
                sock.close()
            
            # Log what happened
            timeStamp = time.time()
            data = datetime.datetime.fromtimestamp(timeStamp).strftime('%Y-%m-%d %H:%M:%S') + '\n'
            
            if receivedFrom == 'Jan':
                data = data + 'Jan attempted to connect.\n'
                helper.WriteToLogFile(pathJanToAnnLogFile, 'a', data)
            elif receivedFrom == 'Chan':
                data = data + 'Chan attempted to connect.\n'
                helper.WriteToLogFile(pathChanToAnnLogFile, 'a', data)                      

        # Your attempt to setup connection with someone else has been responded to
        elif incomingPacket.get('Syn Bit') == 1:

            # Start sending data here and raise the flag to wait for acknowledgement
            sourceID = portListeningTo                                            # The port listening to
            destinationID = incomingPacket.get('Source ID')                       # The destination of the packet about to be sent is where the original packet came from
            sequenceNumber = incomingPacket.get('Acknowledgement Number')         # The  next byte you should be sending is the byte that the other party is expecting
            acknowledgementNumber = incomingPacket.get('Sequence Number') + 1     # Just one more than the sequence number
            urgentPointer = 0                                                     # Not urgent as this is connection setup
            synBit = 0                                                            # Threeway handshake third step, no need of this bit
            finBit = 0                                                            # Not trying to finish connection, therefore 0                                               
            rstBit = 0                                                            # Not trying to reset connection, therefore 0
            terBit = 0                                                            # Not trying to terminate connection, therefore 0
            headerLength = 0                                                      # FIGURE THIS OUT???????????????????????????????????????????

            # Populate data field depending on who the connection is being established with
            if receivedFrom == 'Jan':
                packetData = contentAnnToJan.pop(0)     # Get the first element from list and delete it from there
            elif receivedFrom == 'Chan':
                packetData = contentAnnToChan.pop(0)    # Get the first element from list and delete it from there
             
            # Create packet with above data
            packet = helper.CreateTCPPacket(sourceID, destinationID, acknowledgementNumber, sequenceNumber, packetData, urgentPointer, 
                                            synBit, finBit, rstBit, terBit, headerLength)
            
            # Try and send it
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect(localHost, portTalkingTo)
                sock.sendall(packet)
            finally:
                sock.close()
            
            # Log what happened
            timeStamp = time.time()
            data = datetime.datetime.fromtimestamp(timeStamp).strftime('%Y-%m-%d %H:%M:%S') + '\n'
            
            if receivedFrom == 'Jan':
                data = data + 'Connection with Jan is successful.\n'
                data = data + packetData
                helper.WriteToLogFile(pathJanToAnnLogFile, 'a', data)
            elif receivedFrom == 'Chan':
                data = data + 'Connection with Chan is successful.\n'
                data = data + packetData
                helper.WriteToLogFile(pathChanToAnnLogFile, 'a', data)
        
        # If data field is empty, that means its an acknowledgement packet
        elif incomingPacket.get('Data') == '':
            # Send next piece of data
        
        # Any other case, is receiving dats
        else:
            # Send acknowledgement
            # Count the number of data packets in here
            
        print(data)
        # self.request.sendall(b'got it')            
        return


# ------------------------------------------
# Function for the router threads to execute
# ------------------------------------------
def AgentServer (exitEvent):
    try:
        server = ThreadedTCPServer((localHost, portListeningTo), TCPRequestHandler)
       
        server.timeout = 0.01           # Make sure not to wait too long when serving requests
        server.daemon_threads = True    # So that handle_request thread exits when current thread exits

        # Poll so that you see the signal to exit as opposed to calling server_forever
        while not exitEvent.isSet():
            server.handle_request()   

        server.server_close()           
    except:
        print('Problem creating server for agent Ann.')
    
    sys.exit()


if __name__ == '__main__':
    try:
        exitEvent = threading.Event() # Set this upon keyboard interrupt to let the threads know they have to exit
        exitEvent.clear()             # Make sure the evebt is clear initially
        
        # Create a seperate for Jan's server portion
        annServer = threading.Thread(target=AgentServer, args=(exitEvent,))
       
        # Start the ann's server
        annServer.start()
    except:
        print ("Couldn't create thread for Ann's router.")


    try:
        try:
            """
                Initiate communication here
            """
        except:
            print('Problem opening socket')

        # Run forever till keyboard interrupt is caught
        while True:
            pass
    except KeyboardInterrupt:
        exitEvent.set()  # Upon catching keyboard interrupt, let the threads know they have to exit
        
        # Wait for Ann's server to finish
        annServer.join()
                
        sys.exit()