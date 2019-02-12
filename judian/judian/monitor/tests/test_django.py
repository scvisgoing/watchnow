import os, sys
import django
from django.test import TestCase

# TODO: Configure your database in settings.py and sync before running tests.
if not 'D:\\learn2earn\\watchnow\\judian\\judian' in sys.path:
    sys.path.insert(0, 'D:\\learn2earn\\watchnow\\judian\\judian')
    print(f'Let us see system path: {sys.path}')
os.environ.update({"DJANGO_SETTINGS_MODULE": "judian.settings"})

class SimpleDjangoTest(TestCase):
    """Tests for the application views."""

    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        print('test basic addition')
        self.assertEqual(1 + 1, 2)
