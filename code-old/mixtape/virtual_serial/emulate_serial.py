'''
This is a test of how serial emulation in linux can work. This is based on example
from stack overflow https://stackoverflow.com/questions/2291772/virtual-serial-master-in-python.
'''

import os
import subprocess
import serial
import time
import argparse
from serial.serialutil import SerialException 

class SerialEmulator():

    def __init__(self, master_port='./tty_master', satellite_port='./tty_satellite', baudrate=9600):
        self.master_port = master_port
        self.satellite_port = satellite_port
        self.baudrate = baudrate
        self.err = ''
        self.out = ''
        self.proc = None

    def __del__(self):
        self.close()

    def __enter__(self):
        self.open()

    def __exit__(self):
        self.close()

    def open(self):
        cmd=[f'socat','-d','-d','PTY,link={self.master_port},raw,echo=0',
                f'PTY,link={self.satellite_port},raw,echo=0']
        self.proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(5)
        self.serial = serial.Serial(self.master_port, self.baudrate, rtscts=True, dsrdtr=True)

    def close(self):
        if self.proc is not None:
            self.proc.kill()
            self.out, self.err = self.proc.communicate()

    def write(self, out):
        self.serial.write(out)

    def read(self):
        line = ''
        while self.serial.inWaiting() > 0:
            line += self.serial.read(1)
        return line

    def wait_for_serial(self):
        while self.serial.inWaiting() == 0:
            pass # Active spin



def main(args):
    try:
        with SerialEmulator(args.master_port, args.satellite_port, args.baudrate) as serial_port:
            serial_port.wait_for_serial()
            line = serial_port.read()
            print(line)
    except SerialException as e:
        print(f'Serial exception occured : {e}')
    except KeyboardInterrupt:
        print('Recieved user interrupt.')
    print('CLOSING SERIAL PORT')


def parse_arguments():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-d', '--master_port', type=str, default='./tty_master', 
            help='Master port')
    parser.add_argument('-s', '--satellite_port', type=str, default='./tty_satellite',
            help='Satellite port')
    parser.add_argument('-b', '--baudrate', type=int, default=9600,
            help='Baudrate')
    return parser.parse_args()


if __name__ == '__main__':
    main(parse_arguments())
