# -*- coding: utf-8 -*-
"""
Interactive Plotly Analytics Dashboard.
Visualizes spending breakdown, category distributions, top items, and multilingual command usage.
"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from database.catalog import get_all_products

def render_analytics_dashboard(cart_items, order_history=None):
    st.markdown("## 📊 Smart Shopping Insights & NLP Telemetry")
    st.markdown("Analyze category expenditure, frequent product pairings, and voice language distribution.")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 🛍️ Catalog Categories Breakdown")
        products = get_all_products()
        df_cat = pd.DataFrame(products)['category'].value_counts().reset_index()
        df_cat.columns = ['Category', 'Item Count']
        fig_pie = px.pie(
            df_cat, values='Item Count', names='Category',
            hole=0.45,
            color_discrete_sequence=px.colors.qualitative.Prism
        )
        fig_pie.update_layout(margin=dict(t=20, b=20, l=20, r=20), height=320)
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        st.markdown("#### 🗣️ Voice NLP Language Distribution")
        lang_data = {
            'Language': ['English (en)', 'Hindi (hi)', 'Malayalam (ml)', 'Tamil (ta)', 'Spanish (es)', 'French/German (fr/de)'],
            'Commands Processed': [42, 38, 25, 14, 10, 8]
        }
        df_lang = pd.DataFrame(lang_data)
        fig_bar = px.bar(
            df_lang, x='Language', y='Commands Processed',
            color='Commands Processed',
            color_continuous_scale='Viridis'
        )
        fig_bar.update_layout(margin=dict(t=20, b=20, l=20, r=20), height=320)
        st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("#### 🏷️ Product Price Distribution (INR vs USD)")
    df_prods = pd.DataFrame(products)
    fig_scatter = px.scatter(
        df_prods, x='price_inr', y='rating', size='price_usd', color='category',
        hover_name='name',
        labels={'price_inr': 'Price (₹ INR)', 'rating': 'Customer Rating (★)'}
    )
    fig_scatter.update_layout(margin=dict(t=20, b=20, l=20, r=20), height=350)
    st.plotly_chart(fig_scatter, use_container_width=True)
    