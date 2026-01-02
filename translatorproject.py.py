import tkinter as tk
from tkinter import messagebox, scrolledtext
from gtts import gTTS
import os
from deep_translator import GoogleTranslator
from playsound import playsound
import time

USER_FILE = "users.txt"

# ---------- COLORS ----------
BG_COLOR = "#F5F7FA"
BTN_COLOR = "#2C3E50"
BTN_TEXT_COLOR = "white"
ACCENT_COLOR = "#34495E"

# ---------- USER FUNCTIONS ----------
def login_user():
    users = {}
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            for line in f:
                if "," in line:
                    u, p = line.strip().split(",", 1)
                    users[u] = p

    u = user_entry.get().strip()
    p = pwd_entry.get().strip()

    if u in users and users[u] == p:
        messagebox.showinfo("Success", "Login Successful!")
        translation_page.tkraise()
    else:
        messagebox.showerror("Error", "Login Failed!")

def register_user():
    users = {}
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            for line in f:
                if "," in line:
                    u, p = line.strip().split(",", 1)
                    users[u] = p

    u = user_entry.get().strip()
    p = pwd_entry.get().strip()
    users[u] = p

    with open(USER_FILE, "w") as f:
        for u, p in users.items():
            f.write(u + "," + p + "\n")
    messagebox.showinfo("Success", "Registered!")

def logout_user():
    messagebox.showinfo("Logout", "You have been logged out successfully!")
    home_page.tkraise()

# ---------- TRANSLATION FUNCTIONS ----------
languages_dict = {
    "English": "en", "Tamil": "ta", "Hindi": "hi", "Telugu": "te",
    "Malayalam": "ml", "Kannada": "kn", "Spanish": "es", "French": "fr",
    "German": "de", "Chinese": "zh-CN", "Japanese": "ja", "Korean": "ko",
    "Arabic": "ar", "Russian": "ru"
}

selected_languages = []
lang_btns = {}

def toggle_lang(lang):
    if lang in selected_languages:
        selected_languages.remove(lang)
        lang_btns[lang].config(relief=tk.RAISED)
    else:
        selected_languages.append(lang)
        lang_btns[lang].config(relief=tk.SUNKEN)

def clear_text():
    text_box.delete("1.0", tk.END)

def speak_here(text, lang):
    try:
        filename = f"voice_{int(time.time())}.mp3"
        tts = gTTS(text=text, lang=lang)
        tts.save(filename)
        time.sleep(0.5)
        playsound(filename)
    except Exception as e:
        messagebox.showerror("TTS Error", str(e))

def translate_selected():
    text = text_box.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("Warning", "Enter text!")
        return
    if not selected_languages:
        messagebox.showwarning("Warning", "Select languages!")
        return

    result_box.config(state=tk.NORMAL)
    result_box.delete("1.0", tk.END)

    for lang in selected_languages:
        code = languages_dict[lang]
        try:
            out = GoogleTranslator(source='auto', target=code).translate(text)
            result_box.insert(tk.END, f"{lang}:\n{out}  ")
            speak_btn = tk.Button(result_box, text="🔊",
                                  bg=ACCENT_COLOR, fg=BTN_TEXT_COLOR, border=0,
                                  font=("Arial", 10, "bold"),
                                  command=lambda t=out, c=code: speak_here(t, c))
            result_box.window_create(tk.END, window=speak_btn)
            result_box.insert(tk.END, "\n\n" + "-" * 40 + "\n\n")
        except Exception as e:
            result_box.insert(tk.END, f"{lang}: Failed ({e})\n\n")

    result_box.config(state=tk.DISABLED)

# ---------- MAIN WINDOW ----------
root = tk.Tk()
root.title("Translator")
root.state("zoomed")

# ---------- PAGES ----------
home_page = tk.Frame(root, bg=BG_COLOR)
login_page = tk.Frame(root, bg=BG_COLOR)
translation_page = tk.Frame(root, bg=BG_COLOR)
feedback_page = tk.Frame(root, bg=BG_COLOR)

for page in (home_page, login_page, translation_page, feedback_page):
    page.place(relwidth=1, relheight=1)

# ---------- HOME PAGE ----------
welcome_label = tk.Label(home_page, text="WELCOME", font=("Arial", 28, "bold"), bg=BG_COLOR)
welcome_label.place(relx=0.5, rely=0.4, anchor="center")  # Center horizontally, slightly above middle

bottom_home = tk.Frame(home_page, bg=BG_COLOR)
bottom_home.place(relx=0.5, rely=0.6, anchor="center")
tk.Button(bottom_home, text="Next → Login", width=15, bg=BTN_COLOR, fg=BTN_TEXT_COLOR,
          font=("Arial", 11, "bold"), border=0, command=lambda: login_page.tkraise()).pack()

# ---------- LOGIN PAGE ----------
tk.Label(login_page, text="Login", font=("Arial", 18, "bold"), bg=BG_COLOR).pack(pady=20)
tk.Label(login_page, text="Username:", bg=BG_COLOR, font=("Arial", 12)).pack()
user_entry = tk.Entry(login_page, width=30, font=("Arial", 12))
user_entry.pack(pady=3)
tk.Label(login_page, text="Password:", bg=BG_COLOR, font=("Arial", 12)).pack()
pwd_entry = tk.Entry(login_page, width=30, show="*", font=("Arial", 12))
pwd_entry.pack(pady=3)

tk.Button(login_page, text="Login", width=12, bg=BTN_COLOR, fg=BTN_TEXT_COLOR,
          font=("Arial", 11, "bold"), border=0, command=login_user).pack(pady=6)
tk.Button(login_page, text="Register", width=12, bg=ACCENT_COLOR, fg=BTN_TEXT_COLOR,
          font=("Arial", 11, "bold"), border=0, command=register_user).pack(pady=6)
tk.Button(login_page, text="Forgot Password", fg="#2980B9", bg=BG_COLOR,
          font=("Arial", 10, "underline"), border=0,
          command=lambda: messagebox.showinfo("Reset", "Use system file editor")).pack(pady=5)

bottom_login = tk.Frame(login_page, bg=BG_COLOR)
bottom_login.pack(side=tk.BOTTOM, pady=15)
tk.Button(bottom_login, text="← Home", width=14, bg=ACCENT_COLOR, fg=BTN_TEXT_COLOR,
          font=("Arial", 11, "bold"), border=0, command=lambda: home_page.tkraise()).grid(row=0, column=0, padx=10)
tk.Button(bottom_login, text="Next → Translate", width=14, bg=BTN_COLOR, fg=BTN_TEXT_COLOR,
          font=("Arial", 11, "bold"), border=0, command=lambda: translation_page.tkraise()).grid(row=0, column=1, padx=10)

# ---------- TRANSLATION PAGE ----------
tk.Label(translation_page, text="Enter Text:", font=("Arial", 16, "bold"), bg=BG_COLOR).pack(pady=10)
text_box = tk.Text(translation_page, height=4, width=80, font=("Arial", 13))
text_box.pack(pady=5)

tk.Button(translation_page, text="Translate", width=14, bg=BTN_COLOR, fg=BTN_TEXT_COLOR,
          font=("Arial", 11, "bold"), border=0, command=translate_selected).pack(pady=5)
tk.Button(translation_page, text="Clear Text", width=14, bg=ACCENT_COLOR, fg=BTN_TEXT_COLOR,
          font=("Arial", 11, "bold"), border=0, command=clear_text).pack(pady=5)

# ---------- REDUCED RESULT BOX ----------
tk.Label(translation_page, text="Result:", font=("Arial", 16, "bold"), bg=BG_COLOR).pack(pady=5)
result_box = scrolledtext.ScrolledText(translation_page, height=6, width=100, font=("Arial", 12))
result_box.pack(pady=6)
result_box.config(state=tk.DISABLED)

# ---------- LANGUAGE BUTTONS ----------
lang_frame = tk.Frame(translation_page, bg=BG_COLOR)
lang_frame.pack(pady=10)
for i, lang in enumerate(languages_dict):
    btn = tk.Button(lang_frame, text=lang, width=12, bg="white", fg="#2C3E50",
                    font=("Arial", 10, "bold"), border=1,
                    command=lambda l=lang: toggle_lang(l))
    btn.grid(row=i // 6, column=i % 6, padx=6, pady=6)
    lang_btns[lang] = btn

tk.Button(translation_page, text="Select All Languages", font=("Arial", 12, "bold"),
          bg=BTN_COLOR, fg=BTN_TEXT_COLOR, border=0,
          command=lambda: [toggle_lang(l) for l in list(languages_dict)]).pack(pady=5)

bottom_translate = tk.Frame(translation_page, bg=BG_COLOR)
bottom_translate.pack(side=tk.BOTTOM, pady=15)
tk.Button(bottom_translate, text="← Login", width=14, bg=ACCENT_COLOR, fg=BTN_TEXT_COLOR,
          font=("Arial", 11, "bold"), border=0, command=lambda: login_page.tkraise()).grid(row=0, column=0, padx=10)
tk.Button(bottom_translate, text="Next → Feedback", width=14, bg=BTN_COLOR, fg=BTN_TEXT_COLOR,
          font=("Arial", 11, "bold"), border=0, command=lambda: feedback_page.tkraise()).grid(row=0, column=1, padx=10)
tk.Button(bottom_translate, text="Logout", width=14, bg="#C0392B", fg="white",
          font=("Arial", 11, "bold"), border=0, command=logout_user).grid(row=0, column=2, padx=10)

# ---------- FEEDBACK PAGE ----------
tk.Label(feedback_page, text="Feedback", font=("Arial", 18, "bold"), bg=BG_COLOR).pack(pady=20)
feedback_input = tk.Text(feedback_page, height=5, width=70, font=("Arial", 12))
feedback_input.pack(pady=5)

tk.Button(feedback_page, text="Submit Feedback", width=15, bg=BTN_COLOR, fg=BTN_TEXT_COLOR,
          font=("Arial", 11, "bold"), border=0,
          command=lambda: messagebox.showinfo("Saved", "Thanks!")).pack(pady=10)

bottom_feedback = tk.Frame(feedback_page, bg=BG_COLOR)
bottom_feedback.pack(side=tk.BOTTOM, pady=15)
tk.Button(bottom_feedback, text="← Translate", width=14, bg=ACCENT_COLOR, fg=BTN_TEXT_COLOR,
          font=("Arial", 11, "bold"), border=0, command=lambda: translation_page.tkraise()).grid(row=0, column=0, padx=10)
tk.Button(bottom_feedback, text="Logout", width=14, bg="#C0392B", fg="white",
          font=("Arial", 11, "bold"), border=0, command=logout_user).grid(row=0, column=1, padx=10)

# ---------- START ----------
home_page.tkraise()
root.mainloop()
