import customtkinter as ctk
import pyttsx3
from PyPDF2 import PdfReader
from tkinter.filedialog import askopenfilename, asksaveasfilename
import threading
import re

player = pyttsx3.init()
stop_flag = False
pdfreader = None
all_text = ""

def read_pdf(book):
    global stop_flag, pdfreader, all_text
    pdfreader = PdfReader(book)
    all_text = ""
    for page in pdfreader.pages:
        if stop_flag:
            break
        text = page.extract_text()
        if text:
            all_text += text + " "
            player.say(text)
            player.runAndWait()

    # Ask user if they want to save audio
    save_audio = ctk.CTkInputDialog(text="Do you want to save the audio? (yes/no)", title="Save Audio")
    choice = save_audio.get_input()
    if choice and choice.lower() == "yes":
        filename = asksaveasfilename(defaultextension=".mp3", filetypes=[("Audio Files", "*.mp3")])
        if filename:
            player.save_to_file(all_text, filename)
            player.runAndWait()

    # Show summary/short notes
    summary = generate_summary(all_text)
    summary_box.configure(state="normal")
    summary_box.delete("1.0", "end")
    summary_box.insert("1.0", summary)
    summary_box.configure(state="disabled")

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

def start_reading():
    global stop_flag
    stop_flag = False
    book = askopenfilename()
    if book:
        threading.Thread(target=read_pdf, args=(book,), daemon=True).start()

def stop_reading():
    global stop_flag
    stop_flag = True
    player.stop()

def save_summary():
    summary_text = summary_box.get("1.0", "end").strip()
    if summary_text:
        filename = asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if filename:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(summary_text)

# Modern GUI setup
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("📖 PDF to Audiobook Converter")
root.geometry("650x550")

title_label = ctk.CTkLabel(root, text="PDF to Audiobook Converter",
                           font=("Helvetica", 24, "bold"))
title_label.pack(pady=20)

start_btn = ctk.CTkButton(root, text="▶ Select PDF & Start Reading",
                          font=("Helvetica", 16), command=start_reading)
start_btn.pack(pady=10)

stop_btn = ctk.CTkButton(root, text="⏹ Stop Reading",
                         font=("Helvetica", 16), command=stop_reading)
stop_btn.pack(pady=10)

save_summary_btn = ctk.CTkButton(root, text="💾 Save Summary",
                                 font=("Helvetica", 16), command=save_summary)
save_summary_btn.pack(pady=10)

# Summary box
summary_box = ctk.CTkTextbox(root, width=550, height=200, font=("Helvetica", 14))
summary_box.pack(pady=20)

root.mainloop()
