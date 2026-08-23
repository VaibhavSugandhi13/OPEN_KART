# -*- coding: utf-8 -*-
"""
Multilingual Voice Command Shopping Assistant & Smart Suggestion Manager.
Admin: Vaibhav Sugandhi (vaibhavjisugandhiji6999@gmail.com)
Powered by High-Level NLP Engine, Streamlit UI/UX, and Web Speech API.
"""
import streamlit as st
import pandas as pd
from datetime import datetime

# Import Engines & Database
from nlp_engine.processor import MultilingualNLPProcessor
from nlp_engine.languages import SUPPORTED_LANGUAGES
from database.catalog import get_all_products, get_product_by_key, search_products, get_categories
from database.recommendations import RecommendationEngine
from database.state_manager import StateManager
from voice_engine.web_speech import render_web_speech_mic
from voice_engine.audio_recorder import process_audio_file
from voice_engine.tts import speak_text_gtts
from components.ui_helpers import apply_custom_styles, render_header, render_toast, generate_receipt_text
from components.admin_view import render_admin_dashboard
from components.analytics_view import render_analytics_dashboard
from components.feedback_view import render_feedback_section

# Page Config
st.set_page_config(
    page_title="Voice Shopping Assistant | Vaibhav Sugandhi",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply Custom Styling
apply_custom_styles()

# Initialize Session States
if 'cart' not in st.session_state:
    st.session_state.cart = {}
if 'voice_response' not in st.session_state:
    st.session_state.voice_response = None
if 'tts_audio' not in st.session_state:
    st.session_state.tts_audio = None
if 'active_lang' not in st.session_state:
    st.session_state.active_lang = 'hi'
if 'currency' not in st.session_state:
    st.session_state.currency = 'INR'
if 'nlp_processor' not in st.session_state:
    st.session_state.nlp_processor = MultilingualNLPProcessor()
if 'state_manager' not in st.session_state:
    st.session_state.state_manager = StateManager()
if 'last_order' not in st.session_state:
    st.session_state.last_order = None

nlp = st.session_state.nlp_processor
state_mgr = st.session_state.state_manager

# Top Hero Header with Admin details
render_header(admin_name="Vaibhav Sugandhi", admin_email="vaibhavjisugandhiji6999@gmail.com")

# ==============================================================================
# SIDEBAR CONTROLS
# ==============================================================================
with st.sidebar:
    st.markdown("### 🌐 Voice & Language Settings")
    
    # Language Selector
    lang_keys = list(SUPPORTED_LANGUAGES.keys())
    lang_labels = [f"{SUPPORTED_LANGUAGES[k]['flag']} {SUPPORTED_LANGUAGES[k]['name']}" for k in lang_keys]
    curr_idx = lang_keys.index(st.session_state.active_lang) if st.session_state.active_lang in lang_keys else 1
    
    selected_lang_label = st.selectbox(
        "Active Speech Language",
        lang_labels,
        index=curr_idx,
        help="Select the language for microphone recognition and voice feedback."
    )
    selected_lang_key = lang_keys[lang_labels.index(selected_lang_label)]
    st.session_state.active_lang = selected_lang_key
    active_lang_code = SUPPORTED_LANGUAGES[selected_lang_key]['code']

    # Currency Switcher
    st.markdown("---")
    st.markdown("### 💰 Currency")
    curr_options = {"₹ INR (India)": "INR", "$ USD (Global)": "USD"}
    selected_curr_label = st.radio("Display Currency", list(curr_options.keys()), horizontal=True)
    st.session_state.currency = curr_options[selected_curr_label]
    curr_symbol = "₹" if st.session_state.currency == "INR" else "$"

    # Audio File Upload Alternative
    st.markdown("---")
    with st.expander("📁 Upload Voice Audio File", expanded=False):
        uploaded_audio = st.file_uploader("Upload .wav / .mp3", type=["wav", "mp3", "ogg"])
        if uploaded_audio is not None:
            if st.button("Transcribe & Process Audio"):
                with st.spinner("Processing speech audio..."):
                    rec_result = process_audio_file(uploaded_audio, language_code=active_lang_code)
                    if rec_result['status'] == 'success':
                        st.session_state.uploaded_transcript = rec_result['text']
                        st.success(f"Recognized: '{rec_result['text']}'")
                    else:
                        st.error(rec_result['message'])

    # Cheatsheet & Voice Guide
    st.markdown("---")
    with st.expander("🗣️ Voice Command Cheatsheet", expanded=False):
        st.markdown("""
        **Try speaking or typing:**
        - **Hindi**: `"do liter doodh dedo"`
        - **Hindi**: `"5 seb add karo"`
        - **Malayalam**: `"2 liter paal venam"`
        - **Malayalam**: `"ariyum panchasarayum venam"`
        - **English**: `"Buy 2 liters of milk"`
        - **Remove**: `"doodh hata do"` / `"remove apples"`
        - **Price Filter**: `"find items under 100"`
        - **Substitute**: `"cheeni ka substitute batao"`
        - **Feedback**: `"feedback excellent voice app"`
        """)

    # Quick Cart Stats
    total_cart_items = sum(item['quantity'] for item in st.session_state.cart.values())
    st.markdown("---")
    st.markdown(f"**🛒 Cart Count:** `{total_cart_items:.1f} items`")
    if st.button("🗑️ Clear Entire Cart", use_container_width=True):
        st.session_state.cart.clear()
        st.rerun()

# ==============================================================================
# HELPER: PROCESS NLP COMMAND
# ==============================================================================
def execute_nlp_command(cmd_text):
    if not cmd_text or not cmd_text.strip():
        return
    
    result = nlp.process(cmd_text, active_language=st.session_state.active_lang)
    st.session_state.voice_response = result
    
    intent = result['intent']
    items = result['items']
    
    # 1. ADD INTENT
    if intent == "ADD":
        for itm in items:
            key = itm['item_key']
            qty = itm['quantity']
            unit = itm['unit']
            prod = get_product_by_key(key)
            if prod:
                if key in st.session_state.cart:
                    st.session_state.cart[key]['quantity'] += qty
                else:
                    st.session_state.cart[key] = {
                        'key': key,
                        'name': prod['name'],
                        'brand': prod['brand'],
                        'category': prod['category'],
                        'unit': unit or prod['unit'],
                        'price_inr': prod['price_inr'],
                        'price_usd': prod['price_usd'],
                        'quantity': qty,
                        'image': prod['image'],
                        'emoji': prod['emoji']
                    }
                render_toast(f"Added {qty} {unit} of {prod['name']}!", icon="✅")

    # 2. REMOVE INTENT
    elif intent == "REMOVE":
        for itm in items:
            key = itm['item_key']
            if key in st.session_state.cart:
                del st.session_state.cart[key]
                render_toast(f"Removed {key.capitalize()} from cart!", icon="🗑️")

    # 3. CLEAR INTENT
    elif intent == "CLEAR":
        st.session_state.cart.clear()
        render_toast("Cart emptied!", icon="🧹")

    # 4. Generate TTS audio bytes if available
    if result.get('voice_tts_text'):
        audio_bytes = speak_text_gtts(result['voice_tts_text'], lang_code=st.session_state.active_lang)
        st.session_state.tts_audio = audio_bytes

# ==============================================================================
# LIVE VOICE MICROPHONE BAR & COMMAND INPUT
# ==============================================================================
tts_text_to_speak = st.session_state.voice_response.get('voice_tts_text') if st.session_state.voice_response else None
render_web_speech_mic(active_lang_code=active_lang_code, voice_feedback_text=tts_text_to_speak)

col_input, col_btn = st.columns([5, 1])
with col_input:
    user_command_input = st.text_input(
        "🎙️ Enter Spoken / Typed Voice Command:",
        placeholder="e.g. 'do liter doodh dedo', 'buy 2 liter milk', '2 liter paal venam', 'find apples under 100'",
        label_visibility="collapsed"
    )
with col_btn:
    submit_cmd = st.button("⚡ Execute", use_container_width=True)

if submit_cmd and user_command_input:
    execute_nlp_command(user_command_input)
    st.rerun()

# Display NLP Execution Banner if active
if st.session_state.voice_response:
    res = st.session_state.voice_response
    st.markdown(f"""
    <div class="voice-status-box">
        <span style="font-size: 24px;">🤖</span>
        <div style="flex: 1;">
            <div style="font-size: 11px; color: #94a3b8; text-transform: uppercase;">
                NLP Recognized [{res.get('language', 'en').upper()}] &bull; Intent: <b style="color: #38bdf8;">{res.get('intent')}</b>
            </div>
            <div style="font-size: 15px; font-weight: 600; color: #f8fafc;">
                {res.get('response_message')}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.tts_audio:
        st.audio(st.session_state.tts_audio, format="audio/mp3", autoplay=True)

# ==============================================================================
# MAIN NAVIGATION TABS
# ==============================================================================
tab_shop, tab_cart, tab_smart, tab_analytics, tab_feedback, tab_admin = st.tabs([
    "🛒 Shop & Catalog",
    f"🛍️ Shopping Cart ({len(st.session_state.cart)})",
    "💡 Smart Suggestions & Substitutes",
    "📊 Analytics & Insights",
    "💬 Contact & Feedback",
    "🛡️ Admin Portal"
])

# ------------------------------------------------------------------------------
# TAB 1: SHOP & CATALOG
# ------------------------------------------------------------------------------
with tab_shop:
    st.markdown("### 🏪 Product Marketplace")
    
    # Filter Controls
    f_col1, f_col2, f_col3 = st.columns([2, 2, 2])
    with f_col1:
        cat_list = ["All Categories"] + get_categories()
        sel_cat = st.selectbox("Filter Category", cat_list)
    with f_col2:
        price_limit = st.session_state.voice_response.get('price_filter') if (st.session_state.voice_response and st.session_state.voice_response.get('intent') == 'FILTER_PRICE') else None
        max_p = st.slider(
            f"Max Price ({curr_symbol})",
            min_value=10, max_value=300,
            value=int(price_limit) if price_limit else 300,
            step=10
        )
    with f_col3:
        search_query = st.text_input("🔍 Search Brand / Item", placeholder="e.g. milk, apple, tea, amul")

    filtered_prods = search_products(
        query=search_query,
        category=sel_cat,
        max_price=max_p,
        currency=st.session_state.currency
    )

    st.caption(f"Showing {len(filtered_prods)} available products")

    # Render Product Cards in 3-column Grid
    cols = st.columns(3)
    for idx, prod in enumerate(filtered_prods):
        with cols[idx % 3]:
            price_val = prod['price_inr'] if st.session_state.currency == 'INR' else prod['price_usd']
            diet_badges = "".join([f"<span class='tag-badge'>{d}</span>" for d in prod['dietary'][:2]])
            
            st.markdown(f"""
            <div class="product-card">
                <img src="{prod['image']}" class="product-img" alt="{prod['name']}">
                <div class="product-name">{prod['emoji']} {prod['name']}</div>
                <div class="product-brand">🏷️ {prod['brand']} &bull; {prod['category']}</div>
                <div>{diet_badges}</div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 10px;">
                    <div class="product-price">{curr_symbol}{price_val:.2f} <span style="font-size: 11px; color: #94a3b8;">/{prod['unit']}</span></div>
                    <div style="font-size: 12px; color: #f59e0b;">★ {prod['rating']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            b_col1, b_col2 = st.columns(2)
            with b_col1:
                if st.button(f"➕ Add", key=f"add_{prod['id']}", use_container_width=True):
                    execute_nlp_command(f"add 1 {prod['unit']} of {prod['key']}")
                    st.rerun()
            with b_col2:
                if st.button(f"🔄 Substitute", key=f"sub_{prod['id']}", use_container_width=True):
                    execute_nlp_command(f"substitute for {prod['key']}")
                    st.rerun()
            st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# TAB 2: SHOPPING CART & CHECKOUT
# ------------------------------------------------------------------------------
with tab_cart:
    st.markdown("### 🛍️ Your Smart Shopping List & Cart")
    
    if not st.session_state.cart:
        st.info("🛒 Your cart is currently empty. Speak a voice command like **'do liter doodh dedo'** or **'buy 2 liter milk'** to add items!")
    else:
        cart_rows = []
        subtotal_inr = 0.0
        subtotal_usd = 0.0
        
        for k, item in st.session_state.cart.items():
            tot_inr = item['price_inr'] * item['quantity']
            tot_usd = item['price_usd'] * item['quantity']
            subtotal_inr += tot_inr
            subtotal_usd += tot_usd
            
            cart_rows.append({
                'key': k,
                'Item': f"{item['emoji']} {item['name']}",
                'Category': item['category'],
                'Unit Price': f"₹{item['price_inr']:.2f}" if st.session_state.currency == 'INR' else f"${item['price_usd']:.2f}",
                'Quantity': f"{item['quantity']:.1f} {item['unit']}",
                'Total': f"₹{tot_inr:.2f}" if st.session_state.currency == 'INR' else f"${tot_usd:.2f}",
                'total_price_inr': tot_inr,
                'total_price_usd': tot_usd
            })

        # Display Interactive Cart Items
        for k, item in list(st.session_state.cart.items()):
            c1, c2, c3, c4, c5 = st.columns([3, 2, 2, 2, 1])
            with c1:
                st.markdown(f"**{item['emoji']} {item['name']}**<br><span style='font-size: 11px; color:#94a3b8;'>{item['brand']}</span>", unsafe_allow_html=True)
            with c2:
                p_unit = item['price_inr'] if st.session_state.currency == 'INR' else item['price_usd']
                st.markdown(f"{curr_symbol}{p_unit:.2f} / {item['unit']}")
            with c3:
                q_col1, q_col2, q_col3 = st.columns(3)
                with q_col1:
                    if st.button("➖", key=f"dec_{k}"):
                        if item['quantity'] > 1:
                            st.session_state.cart[k]['quantity'] -= 1
                        else:
                            del st.session_state.cart[k]
                        st.rerun()
                with q_col2:
                    st.markdown(f"**{item['quantity']:.0f}**")
                with q_col3:
                    if st.button("➕", key=f"inc_{k}"):
                        st.session_state.cart[k]['quantity'] += 1
                        st.rerun()
            with c4:
                item_tot = (item['price_inr'] if st.session_state.currency == 'INR' else item['price_usd']) * item['quantity']
                st.markdown(f"**{curr_symbol}{item_tot:.2f}**")
            with c5:
                if st.button("❌", key=f"del_{k}"):
                    del st.session_state.cart[k]
                    st.rerun()
            st.markdown("<hr style='margin: 8px 0; opacity: 0.15;'>", unsafe_allow_html=True)

        st.markdown("---")
        
        # Cart Summary Box & Checkout
        tot_curr = subtotal_inr if st.session_state.currency == 'INR' else subtotal_usd
        
        sum_col1, sum_col2 = st.columns([2, 1])
        with sum_col1:
            st.markdown("#### 🎁 Frequently Bought Together with Your Cart")
            cart_item_list = list(st.session_state.cart.values())
            recs = RecommendationEngine.get_cart_recommendations(cart_item_list, max_recommendations=3)
            r_cols = st.columns(len(recs))
            for i, r in enumerate(recs):
                with r_cols[i]:
                    r_price = r['price_inr'] if st.session_state.currency == 'INR' else r['price_usd']
                    st.caption(f"{r['emoji']} **{r['name']}** ({curr_symbol}{r_price:.2f})")
                    if st.button(f"+ Add {r['key'].capitalize()}", key=f"rec_add_{r['id']}", use_container_width=True):
                        execute_nlp_command(f"add 1 {r['unit']} of {r['key']}")
                        st.rerun()

        with sum_col2:
            st.markdown(f"""
            <div class="cart-card">
                <h4 style="margin-bottom: 14px; color: #f8fafc;">Order Summary</h4>
                <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                    <span>Subtotal:</span>
                    <b>{curr_symbol}{tot_curr:.2f}</b>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                    <span>Estimated Tax (GST):</span>
                    <span style="color: #22c55e;">FREE (0%)</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 12px;">
                    <span>Voice Priority Delivery:</span>
                    <span style="color: #22c55e;">FREE</span>
                </div>
                <hr style="opacity: 0.2;">
                <div style="display: flex; justify-content: space-between; font-size: 20px; font-weight: 800; color: #38bdf8; margin-top: 10px;">
                    <span>Total Amount:</span>
                    <span>{curr_symbol}{tot_curr:.2f}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
            if st.button("🚀 Place Order & Generate Bill", use_container_width=True, type="primary"):
                saved_order = state_mgr.save_order(
                    cart_items=list(st.session_state.cart.values()),
                    total_inr=subtotal_inr,
                    total_usd=subtotal_usd,
                    currency=st.session_state.currency
                )
                st.session_state.last_order = saved_order
                st.session_state.cart.clear()
                st.balloons()
                st.success(f"🎉 Order {saved_order['order_id']} placed successfully!")
                st.rerun()

    # If Last Order Exists, show Invoice
    if st.session_state.last_order:
        st.markdown("---")
        st.markdown("### 📄 Order Invoice & Printable Receipt")
        receipt_str = generate_receipt_text(st.session_state.last_order)
        st.code(receipt_str, language="text")
        st.download_button(
            "📥 Download Receipt (TXT)",
            data=receipt_str,
            file_name=f"Receipt_{st.session_state.last_order['order_id']}.txt",
            mime="text/plain"
        )

# ------------------------------------------------------------------------------
# TAB 3: SMART SUGGESTIONS & SUBSTITUTES
# ------------------------------------------------------------------------------
with tab_smart:
    st.markdown("## 💡 AI Smart Suggestions & Health Substitutes")
    st.markdown("Predictive reorder recommendations, seasonal harvest deals, and healthy ingredient alternatives.")

    # 1. Smart Substitutes Section
    st.markdown("### 🔄 Smart Substitutes Finder")
    st.markdown("Looking for dairy-free, sugar-free, keto, or low-carb alternatives? View smart alternatives below:")
    
    sub_keys = ['milk', 'sugar', 'bread', 'butter', 'potato', 'chicken', 'rice']
    sel_sub_item = st.selectbox("Select product to view substitutes:", sub_keys, format_func=lambda x: f"Substitutes for {x.capitalize()}")
    
    subs = nlp.substitute_engine.get_substitutes(sel_sub_item)
    if subs:
        sub_cols = st.columns(len(subs))
        for i, s in enumerate(subs):
            with sub_cols[i]:
                st.markdown(f"""
                <div style="background: rgba(30, 41, 59, 0.6); padding: 18px; border-radius: 14px; border: 1px solid rgba(255, 255, 255, 0.1); height: 100%;">
                    <div style="font-size: 15px; font-weight: 700; color: #38bdf8; margin-bottom: 4px;">{s['name']}</div>
                    <div style="font-size: 11px; color: #a78bfa; font-weight: 600; margin-bottom: 8px;">🏷️ {s['diet_type']}</div>
                    <p style="font-size: 13px; color: #cbd5e1; line-height: 1.4;">{s['reason']}</p>
                    <div style="font-size: 12px; color: #34d399; font-weight: 600; margin-top: 8px;">Price Diff: {s['price_diff']}</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Add Substitute #{i+1}", key=f"add_sub_{s['key']}"):
                    execute_nlp_command(f"add 1 {s['name']}")
                    st.rerun()

    st.markdown("---")

    # 2. Low-Stock Household Alerts
    st.markdown("### ⚠️ Running Low Prediction")
    low_stock_items = RecommendationEngine.get_low_stock_alerts([])
    ls_cols = st.columns(3)
    for i, ls in enumerate(low_stock_items):
        with ls_cols[i]:
            prod = ls['product']
            st.warning(f"**{prod['emoji']} {prod['name']}**\n\n{ls['message']}")
            if st.button(f"⚡ Reorder {prod['key'].capitalize()}", key=f"reorder_{prod['id']}"):
                execute_nlp_command(f"add 1 {prod['unit']} of {prod['key']}")
                st.rerun()

    st.markdown("---")

    # 3. Seasonal Produce Specials
    st.markdown("### ☀️ Seasonal Harvest Picks")
    seasonal_items = RecommendationEngine.get_seasonal_specials(season='Summer')
    sea_cols = st.columns(3)
    for i, s_item in enumerate(seasonal_items[:3]):
        with sea_cols[i]:
            st.info(f"**{s_item['emoji']} {s_item['name']}** ({s_item['season']})\n\n{s_item['description']}")

# ------------------------------------------------------------------------------
# TAB 4: ANALYTICS & INSIGHTS
# ------------------------------------------------------------------------------
with tab_analytics:
    render_analytics_dashboard(list(st.session_state.cart.values()))

# ------------------------------------------------------------------------------
# TAB 5: CONTACT & FEEDBACK
# ------------------------------------------------------------------------------
with tab_feedback:
    voice_fb = st.session_state.voice_response.get('raw_text') if (st.session_state.voice_response and st.session_state.voice_response.get('intent') == 'FEEDBACK') else ""
    render_feedback_section(voice_dictated_text=voice_fb)

# ------------------------------------------------------------------------------
# TAB 6: ADMIN PORTAL
# ------------------------------------------------------------------------------
with tab_admin:
    render_admin_dashboard()