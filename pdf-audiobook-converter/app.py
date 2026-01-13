import streamlit as st
from PyPDF2 import PdfReader
from gtts import gTTS
import re
import os

st.title("📖 PDF to Audiobook Converter")

# Upload PDF
uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

# Language selection
lang_choice = st.selectbox("Choose Language", ["en", "hi", "te"])  # en=English, hi=Hindi, te=Telugu

def generate_summary(text):
    sentences = re.split(r'(?<=[.!?]) +', text)
    notes = []
    for s in sentences:
        s_clean = s.strip()
        if len(s_clean) > 60 and any(word in s_clean.lower() for word in ["important", "key", "note", "summary", "conclusion"]):
            notes.append("• " + s_clean)
        elif len(s_clean) > 80:
            notes.append("• " + s_clean)
        if len(notes) >= 5:
            break
    return "📌 Important Notes:\n\n" + "\n".join(notes) if notes else "No summary available."

if uploaded_file:
    pdfreader = PdfReader(uploaded_file)
    all_text = ""
    for page in pdfreader.pages:
        page_text = page.extract_text()
        if page_text:
            all_text += page_text + " "

    # Show preview
    st.text_area("Extracted Text Preview", all_text[:1000])

    # Convert to audio
    if st.button("▶ Convert to Audio"):
        tts = gTTS(text=all_text, lang=lang_choice)
        audio_path = "audio.mp3"
        tts.save(audio_path)

        # Play audio in browser
        st.audio(audio_path)

        # Provide download option
        with open(audio_path, "rb") as f:
            st.download_button(
                label="💾 Save Audio",
                data=f,
                file_name="audiobook.mp3",
                mime="audio/mp3"
            )

    # Save summary
    if st.button("💾 Save Summary"):
        summary = generate_summary(all_text)
        st.text_area("Summary", summary, height=200)
        st.download_button("Download Summary", summary, file_name="summary.txt")

 
