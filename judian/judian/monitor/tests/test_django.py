"""
Test if we can support django.test.TestCase

Model and View test can be found in test_models.py and test.views.py
"""
#import os
#import sys
from django.test import TestCase
from django.apps import apps

from monitor.models import Host

class SimpleDjangoTest(TestCase):
    """Tests for the application views."""

    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        print('test basic addition')
        self.assertEqual(1 + 1, 2)

    def test_app_config(self):
        """Test monitor.apps.monitorConfig"""
        self.assertEqual(apps.get_app_config('monitor').verbose_name, 'Monitor Everything You want.')

    def test_app_models(self):
        """Test monitor app has some model"""
        m = apps.get_models()
        self.assertIn(Host, m)
