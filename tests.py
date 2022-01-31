import pytest
import unittest
from people import PeopleFixer as pf

class TestPeopleFixer(unittest.TestCase):
    def test_people_fixer(self):
        p = pf()
        self.assertEqual(p.__repr__(), 'PeopleFixer()')
