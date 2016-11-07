 import os,sys, unittest
from os import path

if __name__ != "__main__":
        # We'll run ./runtest.py which imports these classes within
        # the ./test/ directory and then runs the test. So imports
        # are relative to root, not this file. 
    from src.camera import MyCamera
    from makevid import vid
    
class DeviceTest(unittest.TestCase):

    def setUp(self):
        print 'starting test'
        
    def test_1_basic(self):
        
        self.assertTrue(
        
    def test_2_fpsslow(self):
    
        self
        

def main():

    suite = unittest.TestLoader().loadTestsFromTestCase(DeviceTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

    return 1