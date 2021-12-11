'''
This is library that handles communication protocoll betwen separate elements of 
experiment environment.
'''

import serial
import time
import subprocess

# Command codes for protocol
CMD_INI = 0x00 # Initialize simulation
CMD_RST = 0x00 # Request simualtion reset
CMD_AOK = 0x00 # Everything ok
CMD_ERR = 0x00 # Error occured
CMD_ORQ = 0x00 # Observation request
CMD_OSN = 0x01 # Observation sent
CMD_RSN = 0x03 # Response sent
CMD_DRQ = 0x00 # Request oservation and reaction description
CMD_DSN = 0x00 # Observation and reaction description sent
CMD_MRQ = 0x00 # Request simulation metadata
CMD_MSN = 0x00 # Simulation metadata sent

# Error codes for protocoll
ERR_UNK = 0x00 # Unknown error
ERR_CRT = 0x01 # Criticall error (simulation shutdown)
ERR_UIN = 0x02 # Simulation not initialized
ERR_SST = 0x03 # Simulation stopped
ERR_FMT = 0x04 # Wrong reaction format
ERR_ENV = 0x05 # Unknow environment requested

class RstnSerialMasterNode:
#'''
#This class is used for creation of pseudoterminal endpoint of simulator.
#'''
    def __init__(self, master_port='./tty_master',
            satellite_port='./tty_satellite', baudrate=9600):
        '''
        Initializer for serial master node. It does not create an actual serial port but only
        stores configuration in object. To enable port a function open must be called.

        @param master_port Path in which symbolic link to master endpoint of port will be 
            accessible (this endpoint is not used)
        @param satellite_port Path in which symbolic link to satellite endpoint, it is the 
            endpoint that will be accessed by other modules of experiment
        @param baudrate Baudrate must be set same for all modules comunicating on serial port
        '''
        self.master_port = master_port
        self.satellite_port = satellite_port
        self.baudrate = baudrate
        self.err = ''
        self.out = ''
        self.proc = None
        self.serial = None

    def open(self, safety_delay=1):
        '''
        This function uses "socat" command to create a pseudoterminal.
        
        @param safety_delay Time in seconds for which we wait so that socat will set up all 
            required files
        '''
        if self.serial is not None:
            return False
        cmd=['socat','-d','-d',f'PTY,link={self.master_port},raw,echo=0',
                f'PTY,link={self.satellite_port},raw,echo=0']
        self.proc = subprocess.Popen(cmd) 
        time.sleep(safety_delay)
        self.serial = serial.Serial(self.master_port, self.baudrate, rtscts=True, dsrdtr=True)

    def close(self):
        if self.proc is not None:
            self.proc.kill()
            self.out, self.err = self.proc.communicate()

    def __write(self, contents=[]):
        self.serial.write(bytearray(contents))
