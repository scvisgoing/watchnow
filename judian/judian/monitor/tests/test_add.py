"""
This sample code demo how the unittest.TestCase work
Most important is shortDescription(), that can help us determine which test function is running now.
"""
import unittest

def add(left, right):
    """For out unittest.TestCase"""
    return left + right

class SimpleTest(unittest.TestCase):
    """For test add function"""

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
        self.assertEqual(add(4, 5), 9)

    def testadd2(self):
        """add2"""
        print('testadd2')
        self.assertEqual(add(5, 5), 10)
