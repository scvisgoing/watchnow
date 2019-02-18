"""
Test if we can support django.test.TestCase

Model and View test can be found in test_models.py and test.views.py
"""
#import os
#import sys
from django.test import TestCase

class SimpleDjangoTest(TestCase):
    """Tests for the application views."""

    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        print('test basic addition')
        self.assertEqual(1 + 1, 2)
