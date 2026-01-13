import streamlit as st
from PyPDF2 import PdfReader
from gtts import gTTS
import pyttsx3
import os

st.title("📖 PDF to Audiobook Converter")

uploaded_file = st.file_uploader("Upload a PDF", type="pdf")
lang_choice = st.selectbox("Choose Language", ["English", "Hindi", "Telugu"])

if uploaded_file:
    pdfreader = PdfReader(uploaded_file)
    text = ""
    for page in pdfreader.pages:
        text += page.extract_text() + " "

    st.text_area("Extracted Text Preview", text[:1000])

    if st.button("Read Aloud"):
        if lang_choice == "English":
            player = pyttsx3.init()
            player.say(text)
            player.runAndWait()
        else:
            tts = gTTS(text=text, lang=lang_choice.lower())
            tts.save("audio.mp3")
            st.audio("audio.mp3")

    if st.button("Save Summary"):
        summary = "📌 Short Notes:\n\n" + "\n".join(text.split(".")[:5])
        st.download_button("Download Summary", summary, file_name="summary.txt")
