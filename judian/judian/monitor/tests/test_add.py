import unittest
def add(x, y):
    return x+y
class SimpleTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('called once before any tests in class')

    @classmethod
    def tearDownClass(cls):
        print('called once after all tests in class')

    def setUp(self):
        self.name = self.shortDescription()
        print(f'setUp is called for {self.name}')
    def tearDown(self):
        print(f'tearDown is called {self.name}')
    def testadd1(self):
        """add1"""
        print('testadd1')
        self.assertEqual(add(4,5), 9)
    def testadd2(self):
        """add2"""
        print('testadd2')
        self.assertEqual(add(5,5), 10)
