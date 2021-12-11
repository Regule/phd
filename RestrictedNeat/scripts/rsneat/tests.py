from rsneat import serial_protocol as sp
import unittest
import serial
  

class SerialProtocolTest(unittest.TestCase):
  
    def testMasterNodeCreation(self):
        serial = sp.RstnSerialMasterNode()
        serial.open()
        serial.close()
        self.assertTrue(True)

    def testSendingStringTroughtSerial(self):
        TTY_SATELLITE = './tty_satellite'
        BAUDRATE = 9600
        TEST_STR_1 = 'qwert'
        TEST_STR_2 = 'asdfg'
        with sp.RstnSerialMasterNode(satellite_port=TTY_SATELLITE, baudrate=BAUDRATE) as rstn_port:
            with serial.Serial(TTY_SATELLITE, BAUDRATE, timeout=1) as test_port:
                rstn_port.write(TEST_STR_1.encode('UTF-8'))
                response = []
                while test_port.inWaiting() > 0:
                    response.append(test_port.read())
                response = b''.join(response).decode('UTF-8')
                self.assertEqual(TEST_STR_1, response)


if __name__ == '__main__':
    unittest.main()
