# -*- coding: utf-8 -*-
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from nlp_engine.processor import MultilingualNLPProcessor
from nlp_engine.intent_detector import IntentType

class TestMultilingualNLPProcessor(unittest.TestCase):
    def setUp(self):
        self.nlp = MultilingualNLPProcessor()

    def test_english_add_milk(self):
        res = self.nlp.process("Buy 2 liters of milk")
        self.assertEqual(res['status'], 'success')
        self.assertEqual(res['intent'], 'ADD')
        self.assertEqual(len(res['items']), 1)
        self.assertEqual(res['items'][0]['item_key'], 'milk')
        self.assertEqual(res['items'][0]['quantity'], 2.0)
        self.assertEqual(res['items'][0]['unit'], 'liter')

    def test_hindi_do_liter_doodh(self):
        res = self.nlp.process("do liter doodh dedo")
        self.assertEqual(res['status'], 'success')
        self.assertEqual(res['intent'], 'ADD')
        self.assertEqual(len(res['items']), 1)
        self.assertEqual(res['items'][0]['item_key'], 'milk')
        self.assertEqual(res['items'][0]['quantity'], 2.0)
        self.assertEqual(res['items'][0]['unit'], 'liter')

    def test_malayalam_paal_venam(self):
        res = self.nlp.process("2 liter paal venam")
        self.assertEqual(res['status'], 'success')
        self.assertEqual(res['intent'], 'ADD')
        self.assertEqual(len(res['items']), 1)
        self.assertEqual(res['items'][0]['item_key'], 'milk')
        self.assertEqual(res['items'][0]['quantity'], 2.0)
        self.assertEqual(res['items'][0]['unit'], 'liter')

    def test_remove_item_command(self):
        res = self.nlp.process("doodh cart se hata do")
        self.assertEqual(res['intent'], 'REMOVE')
        self.assertEqual(res['items'][0]['item_key'], 'milk')

    def test_price_filter_command(self):
        res = self.nlp.process("find organic apples under 100")
        self.assertEqual(res['intent'], 'FILTER_PRICE')
        self.assertEqual(res['price_filter'], 100.0)
        self.assertEqual(res['items'][0]['item_key'], 'apple')

    def test_substitute_command(self):
        res = self.nlp.process("cheeni ka substitute batao")
        self.assertEqual(res['intent'], 'SUBSTITUTE')
        self.assertEqual(res['items'][0]['item_key'], 'sugar')
        self.assertTrue(len(res['substitutes']) > 0)

    def test_french_command(self):
        res = self.nlp.process("ajouter deux litres de lait")
        self.assertEqual(res['intent'], 'ADD')
        self.assertEqual(res['items'][0]['item_key'], 'milk')
        self.assertEqual(res['items'][0]['quantity'], 2.0)
        self.assertEqual(res['items'][0]['unit'], 'liter')

    def test_german_command(self):
        res = self.nlp.process("zwei Liter Milch kaufen")
        self.assertEqual(res['intent'], 'ADD')
        self.assertEqual(res['items'][0]['item_key'], 'milk')
        self.assertEqual(res['items'][0]['quantity'], 2.0)
        self.assertEqual(res['items'][0]['unit'], 'liter')

    def test_malayalam_compound_phrase(self):
        res = self.nlp.process("ariyum panchasarayum venam")
        self.assertEqual(res['intent'], 'ADD')
        keys = [item['item_key'] for item in res['items']]
        self.assertIn('rice', keys)
        self.assertIn('sugar', keys)

if __name__ == '__main__':
    unittest.main()