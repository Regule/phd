from rsneat import serial_protocol as sp
import unittest
  

class SerialProtocolTest(unittest.TestCase):
  
    # Returns True or False. 
    def testBasic(self):
        serial = sp.RstnSerialMasterNode()
        serial.open()
        serial.close()
        self.assertTrue(True)



if __name__ == '__main__':
    unittest.main()
