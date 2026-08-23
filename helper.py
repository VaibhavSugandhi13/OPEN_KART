# -*- coding: utf-8 -*-
"""
UI Styling, Glassmorphism CSS, and Visual Enhancements for Streamlit.
"""
import streamlit as st

def apply_custom_styles():
    custom_css = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        .hero-banner {
            background: linear-gradient(135deg, #1e1b4b 0%, #312e81 40%, #1e40af 100%);
            border-radius: 20px;
            padding: 28px 36px;
            color: #ffffff;
            margin-bottom: 24px;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.2), 0 8px 10px -6px rgba(0, 0, 0, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.1);
            position: relative;
            overflow: hidden;
        }
        .hero-banner::after {
            content: '';
            position: absolute;
            top: -50%;
            right: -20%;
            width: 350px;
            height: 350px;
            background: radial-gradient(circle, rgba(99, 102, 241, 0.25) 0%, rgba(0,0,0,0) 70%);
            pointer-events: none;
        }
        .hero-title {
            font-size: 32px;
            font-weight: 800;
            letter-spacing: -0.8px;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 12px;
            color: #ffffff !important;
        }
        .hero-subtitle {
            font-size: 15px;
            color: #cbd5e1;
            max-width: 780px;
            line-height: 1.5;
        }
        .admin-pill {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(255, 255, 255, 0.12);
            padding: 6px 14px;
            border-radius: 30px;
            font-size: 12px;
            font-weight: 600;
            color: #e0e7ff;
            margin-top: 14px;
            border: 1px solid rgba(255, 255, 255, 0.15);
        }

        .product-card {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 16px;
            padding: 16px;
            transition: all 0.25s ease;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
        .product-card:hover {
            transform: translateY(-4px);
            border-color: rgba(99, 102, 241, 0.5);
            box-shadow: 0 12px 20px -3px rgba(0, 0, 0, 0.2);
        }
        .product-img {
            width: 100%;
            height: 140px;
            object-fit: cover;
            border-radius: 12px;
            margin-bottom: 12px;
        }
        .product-name {
            font-size: 16px;
            font-weight: 700;
            color: #f8fafc;
            margin-bottom: 4px;
            line-height: 1.3;
        }
        .product-brand {
            font-size: 12px;
            color: #94a3b8;
            margin-bottom: 8px;
        }
        .product-price {
            font-size: 18px;
            font-weight: 800;
            color: #38bdf8;
        }
        .tag-badge {
            display: inline-block;
            padding: 3px 8px;
            border-radius: 6px;
            font-size: 10px;
            font-weight: 600;
            background: rgba(56, 189, 248, 0.15);
            color: #38bdf8;
            margin-right: 4px;
            margin-bottom: 4px;
        }

        .cart-card {
            background: linear-gradient(145deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.85) 100%);
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 18px;
            padding: 22px;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2);
        }

        .voice-status-box {
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid rgba(99, 102, 241, 0.3);
            border-radius: 12px;
            padding: 12px 18px;
            margin: 12px 0;
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .stat-card {
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 14px;
            padding: 16px;
            text-align: center;
        }
        .stat-value {
            font-size: 26px;
            font-weight: 800;
            color: #60a5fa;
        }
        .stat-label {
            font-size: 12px;
            color: #94a3b8;
            text-transform: uppercase;
            letter-spacing: 0.6px;
            margin-top: 4px;
        }

        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

def render_header(admin_name="Vaibhav Sugandhi", admin_email="vaibhavjisugandhiji6999@gmail.com"):
    st.markdown(f"""
    <div class="hero-banner">
        <div class="hero-title">
            🛒 Multilingual Voice Shopping Assistant
        </div>
        <div class="hero-subtitle">
            AI-Powered Voice Commerce with high-level NLP understanding <b>English</b>, <b>Hindi</b> (<i>"do liter doodh dedo"</i>), 
            <b>Malayalam</b> (<i>"2 liter paal venam"</i>), Tamil, Spanish, French, and smart substitutes recommendations.
        </div>
        <div class="admin-pill">
            👨‍💻 Project Admin: <b>{admin_name}</b> &nbsp;|&nbsp; ✉️ <b>{admin_email}</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_toast(message, icon="ℹ️"):
    st.toast(f"{icon} {message}")

def generate_receipt_text(order_data):
    lines = [
        "=" * 45,
        "       VOICE COMMAND SHOPPING ASSISTANT      ",
        "          Smart Multilingual Commerce        ",
        "=" * 45,
        f"Order ID   : {order_data['order_id']}",
        f"Date/Time  : {order_data['timestamp']}",
        f"Admin      : Vaibhav Sugandhi",
        f"Contact    : vaibhavjisugandhiji6999@gmail.com",
        "-" * 45,
        f"{'Item':<22} {'Qty':<8} {'Price':>12}",
        "-" * 45
    ]
    for item in order_data['items']:
        name = item['name'][:20]
        qty = f"{item['quantity']} {item['unit']}"
        price = f"₹{item['total_price_inr']:.2f}"
        lines.append(f"{name:<22} {qty:<8} {price:>12}")

    lines.extend([
        "-" * 45,
        f"Subtotal   : ₹{order_data['total_inr']:.2f} / ${order_data['total_usd']:.2f}",
        f"GST / Tax  : Included (0% Groceries)",
        f"Delivery   : FREE (Express Voice Order)",
        "=" * 45,
        f"TOTAL PAID : ₹{order_data['total_inr']:.2f} / ${order_data['total_usd']:.2f}",
        "=" * 45,
        "   Thank you for shopping with Voice Assistant!  ",
        "      Engineered by Vaibhav Sugandhi       ",
        "=" * 45
    ])
    return "\n".join(lines)