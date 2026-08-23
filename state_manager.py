# -*- coding: utf-8 -*-
"""
Application State and Data Persistence Manager.
Handles Cart, Order History, Admin Settings, and User Feedback.
"""
import os
import json
from datetime import datetime
from .catalog import get_product_by_key

DATA_DIR = r"C:\Users\ASUS\.gemini\antigravity\scratch\multilingual_voice_shopping_assistant\database\data"

class StateManager:
    def __init__(self):
        os.makedirs(DATA_DIR, exist_ok=True)
        self.feedback_file = os.path.join(DATA_DIR, "feedback.json")
        self.orders_file = os.path.join(DATA_DIR, "orders.json")
        self._init_storage()

    def _init_storage(self):
        if not os.path.exists(self.feedback_file):
            sample_feedback = [
                {
                    'id': 'fb_001',
                    'timestamp': '2026-08-20 14:32:10',
                    'user_name': 'Aarav Sharma',
                    'email': 'aarav.sharma@example.com',
                    'category': 'Voice Recognition',
                    'rating': 5,
                    'feedback_text': 'Amazing Malayalam and Hindi voice accuracy! Said "do liter doodh dedo" and it added perfectly.',
                    'status': 'Reviewed'
                },
                {
                    'id': 'fb_002',
                    'timestamp': '2026-08-22 10:15:40',
                    'user_name': 'Meera Nair',
                    'email': 'meera.nair@example.com',
                    'category': 'Substitutes',
                    'rating': 5,
                    'feedback_text': 'Love the smart almond milk & jaggery substitutes suggestions.',
                    'status': 'Resolved'
                }
            ]
            with open(self.feedback_file, 'w', encoding='utf-8') as f:
                json.dump(sample_feedback, f, indent=2)

        if not os.path.exists(self.orders_file):
            with open(self.orders_file, 'w', encoding='utf-8') as f:
                json.dump([], f, indent=2)

    def get_all_feedback(self):
        try:
            with open(self.feedback_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []

    def save_feedback(self, user_name, email, category, rating, feedback_text):
        entries = self.get_all_feedback()
        new_entry = {
            'id': f"fb_{len(entries) + 1:03d}",
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'user_name': user_name or "Anonymous Shopper",
            'email': email or "shopper@domain.com",
            'category': category,
            'rating': rating,
            'feedback_text': feedback_text,
            'status': 'New (Pending Admin Review)'
        }
        entries.insert(0, new_entry)
        with open(self.feedback_file, 'w', encoding='utf-8') as f:
            json.dump(entries, f, indent=2, ensure_ascii=False)
        return new_entry

    def get_all_orders(self):
        try:
            with open(self.orders_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []

    def save_order(self, cart_items, total_inr, total_usd, currency, payment_method="Voice UPI / Card"):
        orders = self.get_all_orders()
        order_id = f"ORD-{datetime.now().strftime('%Y%m%d')}-{len(orders)+1:04d}"
        new_order = {
            'order_id': order_id,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'items': cart_items,
            'total_inr': total_inr,
            'total_usd': total_usd,
            'currency': currency,
            'payment_method': payment_method,
            'status': 'Confirmed & Dispatched 🚚'
        }
        orders.insert(0, new_order)
        with open(self.orders_file, 'w', encoding='utf-8') as f:
            json.dump(orders, f, indent=2, ensure_ascii=False)
        return new_order