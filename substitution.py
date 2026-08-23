# -*- coding: utf-8 -*-
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from nlp_engine.substitutes import SubstituteEngine

class TestSubstituteEngine(unittest.TestCase):
    def test_milk_substitutes(self):
        subs = SubstituteEngine.get_substitutes('milk')
        self.assertGreaterEqual(len(subs), 2)
        names = [s['name'] for s in subs]
        self.assertTrue(any('Almond Milk' in n for n in names))

    def test_sugar_substitutes(self):
        subs = SubstituteEngine.get_substitutes('sugar')
        self.assertGreaterEqual(len(subs), 2)
        names = [s['name'] for s in subs]
        self.assertTrue(any('Jaggery' in n or 'Stevia' in n for n in names))

if __name__ == '__main__':
    unittest.main()