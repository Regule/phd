'''
This is simple serial monitor that is used for testing if emulate_serial.py script
works correctly.
'''
import serial
import argparse


def main(args):
    with serial.Serial(args.port, args.baudrate, timeout=1) as port:
        line = input('Enter string >')
        port.write(line.encode('UTF-8'))
        response = []
        while port.inWaiting() > 0:
            response.append(port.read())
        print(''.join(response))

def parse_arguments():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-p', '--port', type=str, required=True,
            help='Port')
    parser.add_argument('-b', '--baudrate', type=int, default=9600,
            help='Baudrate')
    return parser.parse_args()


if __name__ == '__main__':
    main(parse_arguments())
