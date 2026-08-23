# Engineering Approach: Multilingual Voice Shopping Assistant

**Author / Admin:** Vaibhav Sugandhi (`vaibhavjisugandhiji6999@gmail.com`)

Our solution combines a client-side zero-latency voice interface with a robust, hybrid Multilingual Natural Language Processing (NLP) pipeline and an intelligent recommendation engine:

1. **Voice & Audio Architecture**: We integrated the HTML5 Web Speech API directly into Streamlit via a custom component, delivering real-time microphone transcription and Text-To-Speech (TTS) auditory feedback across English, Hindi (*Devanagari/Hinglish*), Malayalam (*Script/Manglish*), and global languages without server latency. Server-side audio file processing serves as a resilient fallback.
2. **High-Level NLP Pipeline**: We engineered a multi-stage parser that executes language detection, tokenization, synonym matching, multilingual word-to-number conversion (*"do"*, *"theen"*, *"randu"*, *"half"*), unit standardization (*liter, kg, packet*), and intent classification (`ADD`, `REMOVE`, `SEARCH`, `FILTER_PRICE`, `SUBSTITUTE`, `FEEDBACK`). Compound requests (e.g., *"ariyum panchasarayum venam"*) are parsed seamlessly.
3. **Smart Commerce & Substitutions**: We built Market Basket Association rules for complementary items (e.g., Bread -> Butter/Eggs), predictive low-stock replenishment alerts, and a healthy dietary substitution engine (e.g., Milk -> Almond/Oat milk; Sugar -> Stevia/Jaggery).
4. **Production UI & Administration**: Designed with modern glassmorphism, responsive live cart drawer, multi-currency switching (₹/$), interactive Plotly telemetry, and a dedicated executive dashboard for Admin Vaibhav Sugandhi.