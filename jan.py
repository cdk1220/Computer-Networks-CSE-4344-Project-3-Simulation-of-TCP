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


Mission3Counter = -1


# Everything should be local, make sure all ports are under this IP
localHost = helper.localHost

# Port number that will Jan will be listening to is her ID + 1000
portListeningTo = helper.namesAndPorts.get('Jan')

# Jan will always be dumping her messages to the router she is connected to
portTalkingTo = helper.namesAndPorts.get('F')

# Paths to where communication files are stored
pathToJanToChanFile = './Supplemental Text Files/Jan/Jan-_Chan.txt'
pathToJanToAnnFile = './Supplemental Text Files/Jan/Jan-_Ann.txt'

# Paths to where the resulting log files from communication will be stored
pathToJanChanLogFile = './Supplemental Text Files/Jan/JanChanLog.txt'
pathToJanAnnLogFile = './Supplemental Text Files/Jan/JanAnnLog.txt'
pathToJanAirForceLogFile = './Supplemental Text Files/Jan/JanAirForceLog.txt'

# Clear log files at the start of the session
helper.WriteToLogFile(pathToJanChanLogFile, 'w', '')
helper.WriteToLogFile(pathToJanAnnLogFile, 'w', '')

# Reading communication material from the text files
contentJanToChan = helper.ReadFile(pathToJanToChanFile)
contentJanToAnn = helper.ReadFile(pathToJanToAnnFile)

# Set this upon keyboard interrupt to let the threads know they have to exit
exitEvent = threading.Event() 

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
        incomingPacketDecoded = pickle.loads(incomingPacket)
        
        receivedFrom = helper.GetKeyFromValue(incomingPacketDecoded.get('Source ID'))
        global Mission3Counter

        if incomingPacketDecoded.get('Fin Bit') == 1 and Mission3Counter == 8:           
            
            timeStamp = time.time()
            data = datetime.datetime.fromtimestamp(timeStamp).strftime('%Y-%m-%d %H:%M:%S') + '\n'
            data = data + 'Acknowledgement recieved, Communication with Ann is Finished.This is the third step for the communication teardown.\n\n'
            helper.WriteToLogFile(pathToJanAnnLogFile, 'a', data)
            # exit Jan's event
            print('Jan Ending Connection...') 
            exitEvent.set()

        elif Mission3Counter == 6:
            
            # increment the next position
            Mission3Counter = 8

            sourceID = portListeningTo                                                   # The port listening to
            destinationID = helper.namesAndPorts.get('Ann')                              # The destination of the packet about to be sent is where the original packet came from
            sequenceNumber = incomingPacketDecoded.get('Acknowledgement Number')         # The  next byte you should be sending is the byte that the other party is expecting                                                                                  
                                                                                         # Next byte of data that you want
            acknowledgementNumber = incomingPacketDecoded.get('Sequence Number')+ len(incomingPacketDecoded.get('Data'))    
            packetData = 'Request for a finish mission?\n'                               # Second step of three way handshake, therefore no data
            urgentPointer = 0                                                            # Not urgent as this is connection setup
            synBit = 0                                                                   # Syn bit is zero
            finBit = 1                                                                   # Trying to finish connection
            rstBit = 0                                                                   # Not trying to reset connection, therefore 0
            terBit = 0                                                                   # Not trying to terminate connection, therefore 0
           
            # Create packet with above data
            responsePacket = helper.CreateTCPPacket(sourceID, destinationID, acknowledgementNumber, sequenceNumber, packetData, urgentPointer, synBit, finBit, rstBit, terBit)

            # Send packet
            helper.SerializeAndSendPacket(responsePacket, portTalkingTo)
            
            # Log what happened
            timeStamp = time.time()
            data = datetime.datetime.fromtimestamp(timeStamp).strftime('%Y-%m-%d %H:%M:%S') + '\n'
            data = data + 'Received following line.\n'
            data = data + incomingPacketDecoded.get('Data')
            data = data + 'Acknowledgement sent along with below line. This is the first step of the connection teardown.\n'
            data = data + packetData + '\n\n'
            helper.WriteToLogFile(pathToJanAnnLogFile, 'a', data)
            print('JanToAnn: Request for a finish mission?\n')



        elif Mission3Counter == 4 and incomingPacketDecoded.get('Data') == 'Success!':
            
            # increment the next position
            Mission3Counter = 6
            sourceID = portListeningTo                                                   # The port listening to
            destinationID = helper.namesAndPorts.get('Ann')                              # The destination of the packet about to be sent is where the original packet came from
            sequenceNumber = incomingPacketDecoded.get('Acknowledgement Number')         # The  next byte you should be sending is the byte that the other party is expecting                                                                                  
                                                                                         # Next byte of data that you want
            acknowledgementNumber = incomingPacketDecoded.get('Sequence Number')+ len(incomingPacketDecoded.get('Data'))
                                                                                         # confirm success by giving the code
            packetData = 'The authorization code:\n' + 'Congratulations\n' 
            urgentPointer = 1                                                            # Message is urgent
            synBit = 0                                                                   # Syn bit is zero
            finBit = 0                                                                   # Not trying to finish connection, therefore 0                                               
            rstBit = 0                                                                   # Not trying to reset connection, therefore 0
            terBit = 0                                                                   # Not trying to terminate connection, therefore 0
           
            # Create packet with above data
            responsePacket = helper.CreateTCPPacket(sourceID, destinationID, acknowledgementNumber, sequenceNumber, packetData, urgentPointer, synBit, finBit, rstBit, terBit)

            # Send packet
            helper.SerializeAndSendPacket(responsePacket, portTalkingTo)
            
            # Log what happened
            timeStamp = time.time()
            data = datetime.datetime.fromtimestamp(timeStamp).strftime('%Y-%m-%d %H:%M:%S') + '\n'
            data = data + 'Received following line.\n'
            data = data + incomingPacketDecoded.get('Data')
            data = data + 'Acknowledgement sent along with below line.\n'
            data = data + packetData + '\n\n'
            helper.WriteToLogFile(pathToJanAnnLogFile, 'a', data)
            print('JanToAnn: The authorization code:\n' + 'Congratulations\n')


        elif Mission3Counter == 2:
            
            # increment the next position
            # need to see how to execute to router H
            
            sourceID = portListeningTo                                                   # The port listening to
            destinationID = helper.namesAndPorts.get('H')                                # The destination of the packet about to be sent is where the original packet came from
            sequenceNumber = sequenceNumber = random.randint(10000, 99999)               # The  next byte you should be sending is the byte that the other party is expecting                                                                                  
                                                                                         # Next byte of data that you want
            acknowledgementNumber = -1 
                                                                                         # confirm success by giving the code
            packetData = 'Location of target: (32° 43 22.77 N,97° 9 7.53 W)\n' + 'The authorization code for the Airforce Headquarters:\n' + 'PEPPER THE PEPPER\n' 
            urgentPointer = 1                                                            # Message is urgent
            synBit = 0                                                                   # Syn bit is zero
            finBit = 0                                                                   # Not trying to finish connection, therefore 0                                               
            rstBit = 0                                                                   # Not trying to reset connection, therefore 0
            terBit = 0                                                                   # Not trying to terminate connection, therefore 0
           
            # Create packet with above data
            responsePacket = helper.CreateTCPPacket(sourceID, destinationID, acknowledgementNumber, sequenceNumber, packetData, urgentPointer, synBit, finBit, rstBit, terBit)

            # Send packet
            helper.SerializeAndSendPacket(responsePacket, helper.namesAndPorts.get('H'))
            

            # Log what happened
            
            timeStamp = time.time()
            data = datetime.datetime.fromtimestamp(timeStamp).strftime('%Y-%m-%d %H:%M:%S') + '\n'
            data = data + 'Received following line.\n'
            data = data + incomingPacketDecoded.get('Data')
            data = data + 'Acknowledgement sent along with below line.\n'
            #data = data + packetData + '\n\n'
            helper.WriteToLogFile(pathToJanAirForceLogFile, 'a', data)
            Mission3Counter = 4
            print('JanToAirForce: Location of target: (32° 43 22.77 N,97° 9 7.53 W)\n' + 'The authorization code for the Airforce Headquarters:\n' + 'PEPPER THE PEPPER\n')



        elif incomingPacketDecoded.get('Urgent Pointer') == 1:
            print('Communication with Chan has been Compromised\n')
            # increment the next position
            Mission3Counter = 2
            sourceID = portListeningTo                                                   # The port listening to
            destinationID = helper.namesAndPorts.get('Ann')                              # The destination of the packet about to be sent is where the original packet came from
            sequenceNumber = incomingPacketDecoded.get('Acknowledgement Number')         # The  next byte you should be sending is the byte that the other party is expecting                                                                                  
                                                                                         # Next byte of data that you want
            acknowledgementNumber = incomingPacketDecoded.get('Sequence Number')+ len(incomingPacketDecoded.get('Data'))
                                                                                         # confirm success by giving the code
            packetData = 'Location of target: (32° 43 22.77 N,97° 9 7.53 W)\n' + 'Request for a mission execution?\n' 
            urgentPointer = 1                                                            # Message is urgent
            synBit = 0                                                                   # Syn bit is zero
            finBit = 0                                                                   # Not trying to finish connection, therefore 0                                               
            rstBit = 0                                                                   # Not trying to reset connection, therefore 0
            terBit = 0                                                                   # Not trying to terminate connection, therefore 0
           
            # Create packet with above data
            responsePacket = helper.CreateTCPPacket(sourceID, destinationID, acknowledgementNumber, sequenceNumber, packetData, urgentPointer, synBit, finBit, rstBit, terBit)

            # Send packet
            helper.SerializeAndSendPacket(responsePacket, portTalkingTo)
            

            # Log what happened
            timeStamp = time.time()
            data = datetime.datetime.fromtimestamp(timeStamp).strftime('%Y-%m-%d %H:%M:%S') + '\n'
            data = data + 'Received following line.\n'
            data = data + incomingPacketDecoded.get('Data')
            data = data + 'Acknowledgement sent along with below line.\n'
            data = data + packetData + '\n\n'
            helper.WriteToLogFile(pathToJanAnnLogFile, 'a', data)
            
            print('JanToAnn: Location of target: (32° 43 22.77 N,97° 9 7.53 W)\n' + 'Request for a mission execution?\n')


        elif Mission3Counter < 0:
            # When someone else is trying to setup connection with us
            if incomingPacketDecoded.get('Syn Bit') == 1 and incomingPacketDecoded.get('Acknowledgement Number') == -1:
                
                # Send TCP packet with syn bit still one and acknowledgement number as 1 + sequence number. Also, create your own sequence number
                sourceID = portListeningTo                                                   # The port listening to
                destinationID = incomingPacketDecoded.get('Source ID')                       # The destination of the packet about to be sent is where the original packet came from
                sequenceNumber = random.randint(10000, 99999)                                # First time talking to client, create new sequence number
                acknowledgementNumber = incomingPacketDecoded.get('Sequence Number') + 1     # Client wanted to connect, therefore no data in the original packet, ack # will be one more than client seq #
                packetData = ''                                                              # Second step of three way handshake, therefore no data
                urgentPointer = 0                                                            # Not urgent as this is connection setup
                synBit = 1                                                                   # Syn bit has to be one for the second step of threeway handshake
                finBit = 0                                                                   # Not trying to finish connection, therefore 0                                               
                rstBit = 0                                                                   # Not trying to reset connection, therefore 0
                terBit = 0                                                                   # Not trying to terminate connection, therefore 0
               
                # Create packet with above data
                responsePacket = helper.CreateTCPPacket(sourceID, destinationID, acknowledgementNumber, sequenceNumber, packetData, urgentPointer, 
                                                synBit, finBit, rstBit, terBit)
                
                # Send packet
                helper.SerializeAndSendPacket(responsePacket, portTalkingTo)
                
                # Log what happened
                timeStamp = time.time()
                data = datetime.datetime.fromtimestamp(timeStamp).strftime('%Y-%m-%d %H:%M:%S') + '\n'
                
                if receivedFrom == 'Chan':
                    data = data + 'Chan as a client attempted to connect. Sent packet with Syn Bit as 1, which is the second step of the threeway handshake.\n\n'
                    helper.WriteToLogFile(pathToJanChanLogFile, 'a', data)
                elif receivedFrom == 'Ann':
                    data = data + 'Ann as a client attempted to connect. Sent packet with Syn Bit as 1, which is the second step of the threeway handshake.\n\n'
                    helper.WriteToLogFile(pathToJanAnnLogFile, 'a', data)                      

            # Your attempt to setup connection with someone else has been responded to
            elif incomingPacketDecoded.get('Syn Bit') == 1:

                # Start sending data here and raise the flag to wait for acknowledgement
                sourceID = portListeningTo                                                   # The port listening to
                destinationID = incomingPacketDecoded.get('Source ID')                       # The destination of the packet about to be sent is where the original packet came from
                sequenceNumber = incomingPacketDecoded.get('Acknowledgement Number')         # The  next byte you should be sending is the byte that the other party is expecting
                acknowledgementNumber = incomingPacketDecoded.get('Sequence Number') + 1     # Just one more than the sequence number
                urgentPointer = 0                                                            # Not urgent as this is connection setup
                synBit = 0                                                                   # Threeway handshake third step, no need of this bit
                finBit = 0                                                                   # Not trying to finish connection, therefore 0                                               
                rstBit = 0                                                                   # Not trying to reset connection, therefore 0
                terBit = 0                                                                   # Not trying to terminate connection, therefore 0

                # Populate data field depending on who the connection is being established with
                if receivedFrom == 'Chan':
                    try:
                        packetData = contentJanToChan.pop(0)     # Get the first element from list and delete it from there
                    except IndexError:
                        print('Jan-_Chan.txt is empty.\n\n')

                elif receivedFrom == 'Ann':
                    try:
                        packetData = contentJanToAnn.pop(0)    # Get the first element from list and delete it from there
                    except IndexError:
                        print('Jan-_Ann.txt is empty.\n\n')
                 
                # Create packet with above data
                responsePacket = helper.CreateTCPPacket(sourceID, destinationID, acknowledgementNumber, sequenceNumber, packetData, urgentPointer, 
                                                synBit, finBit, rstBit, terBit)
                
                # Send packet
                helper.SerializeAndSendPacket(responsePacket, portTalkingTo)
                
                # Log what happened
                timeStamp = time.time()
                data = datetime.datetime.fromtimestamp(timeStamp).strftime('%Y-%m-%d %H:%M:%S') + '\n'
                
                if receivedFrom == 'Chan':
                    data = data + 'Connection with Chan as the server is successful. This is the third step of the threeway handshake. First, which is below line was sent.\n'
                    data = data + packetData + '\n\n'
                    helper.WriteToLogFile(pathToJanChanLogFile, 'a', data)
                elif receivedFrom == 'Ann':
                    data = data + 'Connection with Ann as the server is successful. This is the third step of the threeway handshake. First, which is below line was sent.\n'
                    data = data + packetData + '\n\n'
                    helper.WriteToLogFile(pathToJanAnnLogFile, 'a', data)
            

            # Any other case, is receiving data
            else:
                # Send acknowledgement
                sourceID = portListeningTo                                            # The port listening to
                destinationID = incomingPacketDecoded.get('Source ID')                # The destination of the packet about to be sent is where the original packet came from
                sequenceNumber = incomingPacketDecoded.get('Acknowledgement Number')  # The  next byte you should be sending is the byte that the other party is expecting
                                                                                       
                                                                                      # Next byte of data that you want
                acknowledgementNumber = incomingPacketDecoded.get('Sequence Number') + len(incomingPacketDecoded.get('Data')) 

                urgentPointer = 0                                                     # Not urgent as this is connection setup
                synBit = 0                                                            # Syn bit has to be one for the second step of threeway handshake
                finBit = 0                                                            # Not trying to finish connection, therefore 0                                               
                rstBit = 0                                                            # Not trying to reset connection, therefore 0
                terBit = 0                                                            # Not trying to terminate connection, therefore 0

                # Populate data field depending on who the connection is being established with
                if receivedFrom == 'Chan':
                    try:
                        packetData = contentJanToChan.pop(0)     # Get the first element from list and delete it from there
                    except IndexError:
                        # Kick of connection tear down function here
                        pass

                elif receivedFrom == 'Ann':
                    try:
                        packetData = contentJanToAnn.pop(0)    # Get the first element from list and delete it from there
                    except IndexError:
                        # Kick of connection tear down function here
                        pass

                # Create packet with above data
                responsePacket = helper.CreateTCPPacket(sourceID, destinationID, acknowledgementNumber, sequenceNumber, packetData, urgentPointer, 
                                                synBit, finBit, rstBit, terBit)
                
                # Send packet
                helper.SerializeAndSendPacket(responsePacket, portTalkingTo)
                
                # Log what happened
                timeStamp = time.time()
                data = datetime.datetime.fromtimestamp(timeStamp).strftime('%Y-%m-%d %H:%M:%S') + '\n'
                data = data + 'Received following line.\n'
                data = data + incomingPacketDecoded.get('Data')
                data = data + 'Acknowledgement sent along with below line.\n'
                data = data + packetData + '\n\n'

                if receivedFrom == 'Chan':
                    helper.WriteToLogFile(pathToJanChanLogFile, 'a', data)
                elif receivedFrom == 'Ann':
                    helper.WriteToLogFile(pathToJanAnnLogFile, 'a', data)
          
        return


# ------------------------------------------
# Function for the router threads to execute
# ------------------------------------------
def AgentServer ():
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
        # Make sure the evebt is clear initially
        exitEvent.clear()                    
        
        # Create a seperate for Jan's server portion
        janServer = threading.Thread(target=AgentServer, args=())
       
        # Start the Jan's server
        janServer.start()

        # Sleep to ensure that all agents are online
        time.sleep(10)
    except:
        print ("Couldn't create thread for Jan's router.")


    try:

        # Start connection setup with Ann
        sourceID = portListeningTo                                            # The port listening to
        destinationID = helper.namesAndPorts.get('Ann')                       # Trying to setup connection with Jan, so send the packet to Jan
        sequenceNumber = random.randint(10000, 99999)                         # First time talking to Ann, create new sequence number
        acknowledgementNumber = -1                                            # Haven't recevied anything from Jan, therefore -1
        packetData = ''                                                       # Acknowledgment packets contain no data
        urgentPointer = 0                                                     # Not urgent as this is connection setup
        synBit = 1                                                            # Syn bit has to be one since this is connection setup
        finBit = 0                                                            # Not trying to finish connection, therefore 0                                               
        rstBit = 0                                                            # Not trying to reset connection, therefore 0
        terBit = 0                                                            # Not trying to terminate connection, therefore 0

        # Create packet with above data
        responsePacket = helper.CreateTCPPacket(sourceID, destinationID, acknowledgementNumber, sequenceNumber, packetData, urgentPointer, 
                                        synBit, finBit, rstBit, terBit)
        
        # Send packet
        helper.SerializeAndSendPacket(responsePacket, portTalkingTo)

        # Log it
        timeStamp = time.time()
        data = datetime.datetime.fromtimestamp(timeStamp).strftime('%Y-%m-%d %H:%M:%S') + '\n'
        data = data + "Connection setup with Ann started. This is the first step of the threeway handshake.\n\n"
        helper.WriteToLogFile(pathToJanAnnLogFile, 'a', data)

        # Run till connection teardown or termination
        while not exitEvent.isSet():
            pass
        
        # Wait for Jan's server to finish
        janServer.join()
                
        sys.exit()
    except KeyboardInterrupt:
        exitEvent.set()  # Upon catching keyboard interrupt, let the threads know they have to exit
        
        # Wait for Jan's server to finish
        janServer.join()
                
        sys.exit()
