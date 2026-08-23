# -*- coding: utf-8 -*-
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.catalog import get_all_products, get_product_by_key, search_products
from database.state_manager import StateManager

class TestCartAndCatalog(unittest.TestCase):
    def setUp(self):
        self.state_mgr = StateManager()

    def test_catalog_retrieval(self):
        prods = get_all_products()
        self.assertGreaterEqual(len(prods), 25)
        milk = get_product_by_key('milk')
        self.assertIsNotNone(milk)
        self.assertEqual(milk['key'], 'milk')

    def test_search_and_price_filter(self):
        results = search_products(query='apple', max_price=200, currency='INR')
        self.assertGreater(len(results), 0)
        self.assertTrue(all(p['price_inr'] <= 200 for p in results))

    def test_feedback_saving(self):
        entry = self.state_mgr.save_feedback(
            user_name="Test User",
            email="test@domain.com",
            category="Voice Recognition",
            rating=5,
            feedback_text="Test voice assistant feedback"
        )
        self.assertIn('id', entry)
        self.assertEqual(entry['rating'], 5)

if __name__ == '__main__':
    unittest.main()