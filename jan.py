import helper

from socketserver import ThreadingMixIn, TCPServer, BaseRequestHandler
import threading
import sys
import time
import socket
import pickle


# Everything should be local, make sure all ports are under this IP
localHost = "127.0.0.1"

# Port number that will ann will be listening to is her ID + 1000
portListeningTo = 1100

# Ann will always be dumping her messages to the router she is connected to
portTalkingTo = 8000

# Path to where the communication files are stored 
pathToJanToAnnFile = './Supplemental Text Files/Ann/Jan-_Ann.txt'
pathToJanToChanFile = './Supplemental Text Files/Ann/Jan-_Chan.txt'

# Path to where the communication files are stored when recieved 
pathToJanToAnnLogFile = './Supplemental Text Files/Ann/JanToAnnLog.txt'
pathToJanToChanLogFile = './Supplemental Text Files/Ann/JanToChanLog.txt'

# read the content inside each of the files
contentJanToAnn = helper.ReadFile(pathToJanToAnnFile)
contentJanToChan = helper.ReadFile(pathToJanToChanFile)




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
        data = self.request.recv(1024)
        print(data)
         
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
        print('Problem creating server for agent Jan.')
    
    sys.exit()

if __name__ == '__main__':
    try:
        exitEvent = threading.Event() # Set this upon keyboard interrupt to let the threads know they have to exit
        exitEvent.clear()             # Make sure the evebt is clear initially
        
        # Create a seperate for Jan's server portion
        janServer = threading.Thread(target=AgentServer, args=(exitEvent))
       
        # Start the ann's server
        janServer.start()
    except:
        print ("Couldn't create thread for Jan's router.")


    try:
        # Run forever till keyboard interrupt is caught
        while True:
            pass
    except KeyboardInterrupt:
        exitEvent.set()  # Upon catching keyboard interrupt, let the threads know they have to exit
        
        # Wait for Ann's server to finish
        janServer.join()
                
        sys.exit()
