# Computer-Networks-CSE-4344-Project-3-Simulation-of-TCP

The main idea of this project is to simulate the TCP protocol, which is transport layer protocol. It had to be done in an interesting way in that a communication protocol had to be created for three host systems, that were connected via different links. The newly built communication protocol is supposed to be similar to TCP and also simulate how TCP works. Please read 'Project 3.pdf' for more details.

This project was developed in a Unix environment and written in Python 3.5. Therefore, all testing routines conducted cover the functionality of the project only in a Unix environment.


## Instructions for Execution
- Open 4 terminal windows. 
- Change the directory in all four terminal windows to where the python scripts for the project are.
- First off, run the 'routers.py' script by typing 'python3 routers.py' in one terminal.
- Run 'ann.py,' 'jan.py,' and 'chan.py,' in the remaining terminak windows by typing 'python3 ann.py,' 'python3 jan.py,' and     'python3 chan.py.' 
- After execution is finished, check the log files in 'Supplemental Text Files' to check results. For example, communication between Ann and Jan could be observed in 'AnnJanLog.txt' in Ann's perspective.
  Additionaly, each packet's trace through the routers can be observed in the terminal window that ran 'router.py.'


## Assumptions Made
- Requirments on retransmission on packet loss was not clear. Consequently, that is not implemented.
- After the routers are kicked off, it is assumed that they will always be running, since there is no requirement that
  specifies the termination of them.
- It was assumed that Jan talks to Ann, Ann talks to Chan, and Chan talks to Jan.
- Scripts have to be run in the order 'jan.py,' 'chan.py,' and 'ann.py.'
- The costs of communication among routers never change.
- Mission 3 starts right after Chan gets terminated.

