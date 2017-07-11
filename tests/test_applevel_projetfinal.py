import unittest 
from cast.application.test import run

class TestUnit(unittest.TestCase):
    
    def testName(self):
        run(kb_name='finalplugin_local', application_name='Final')     
        
if __name__ == "__main__":
    unittest.main()
