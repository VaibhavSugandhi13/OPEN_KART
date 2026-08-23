# -*- coding: utf-8 -*-
"""
Contact & Feedback Portal with Voice Input and Form Submission.
Admin Contact: Vaibhav Sugandhi (vaibhavjisugandhiji6999@gmail.com)
"""
import streamlit as st
from database.state_manager import StateManager

def render_feedback_section(voice_dictated_text=""):
    state_mgr = StateManager()

    st.markdown("## 💬 Contact Admin & Submit Feedback")
    st.markdown("""
    Have suggestions, voice recognition feedback, or product requests?  
    Directly reach out to our project lead **Vaibhav Sugandhi** (`vaibhavjisugandhiji6999@gmail.com`).
    """)

    col_form, col_info = st.columns([1.6, 1])

    with col_form:
        with st.form("feedback_form", clear_on_submit=True):
            user_name = st.text_input("Your Full Name", placeholder="e.g. Rahul Sharma")
            user_email = st.text_input("Your Email Address", placeholder="e.g. rahul@example.com")
            category = st.selectbox(
                "Feedback Category",
                ["Voice Recognition Accuracy", "Shopping UI / UX", "Smart Substitutes & Suggestions", "Catalog / Product Request", "General Inquiry"]
            )
            rating = st.slider("Rating (1 to 5 Stars)", min_value=1, max_value=5, value=5)
            
            initial_text = voice_dictated_text if voice_dictated_text else ""
            feedback_text = st.text_area(
                "Feedback / Message (You can also speak your feedback!)",
                value=initial_text,
                placeholder="Share your experience or voice accuracy feedback here..."
            )

            submitted = st.form_submit_button("🚀 Submit Feedback", use_container_width=True)
            if submitted:
                if feedback_text.strip():
                    new_entry = state_mgr.save_feedback(user_name, user_email, category, rating, feedback_text)
                    st.success(f"🎉 Thank you, {user_name or 'Shopper'}! Your feedback #{new_entry['id']} has been received by Admin Vaibhav Sugandhi.")
                else:
                    st.warning("Please enter your feedback text before submitting.")

    with col_info:
        st.markdown("""
        <div style="background: rgba(30, 41, 59, 0.6); padding: 20px; border-radius: 16px; border: 1px solid rgba(255, 255, 255, 0.1);">
            <h4 style="color: #60a5fa; margin-bottom: 12px;">📞 Administrative Contact</h4>
            <p><b>Lead Engineer & Admin:</b><br>Vaibhav Sugandhi</p>
            <p style="margin-top: 10px;"><b>Primary Email:</b><br><a href="mailto:vaibhavjisugandhiji6999@gmail.com" style="color: #38bdf8;">vaibhavjisugandhiji6999@gmail.com</a></p>
            <p style="margin-top: 10px;"><b>Response SLA:</b><br>Within 24 Hours</p>
            <p style="margin-top: 10px;"><b>Voice Feedback Shortcut:</b><br>Click mic and say: <i>"feedback bohot badiya app hai"</i></p>
        </div>
        """, unsafe_allow_html=True)
        