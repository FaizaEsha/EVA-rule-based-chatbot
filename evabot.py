"""
================================================================================
  EVA — Intelligent Rule-Based Assistant
--------------------------------------------------------------------------------
  A deterministic, dictionary-driven chatbot with a hand-styled desktop GUI.
  No frameworks, no login/signup — just Python's built-in Tkinter, run and go.

  Created by : Faiza Ahmed Esha (aspiring software developer)
  Concept    : "The Logic Engine" — Input -> Sanitize -> Match -> Respond -> Loop

  About      : EVA quietly stands for "Esha's Virtual Assistant" — a personal
               touch behind an otherwise clean product name. Kept here rather
               than repeated across the interface, on purpose.
================================================================================
"""

import tkinter as tk
from tkinter import font as tkfont
import random
import re
import datetime

# ------------------------------------------------------------------------------
# 1. THEME — Midnight Navy + Lavender Glass
#    A single palette so the whole app feels designed, not default.
#    Change values here to re-theme the entire application.
# ------------------------------------------------------------------------------
THEME = {
    "bg_app":         "#060B1E",   # deep navy — main window background
    "bg_header":      "#0A1130",   # header strip, glass-tinted navy
    "bg_chat":        "#04081A",   # darkest navy — chat canvas
    "bg_input":       "#0C1330",   # input bar background
    "bg_input_field": "#121A3D",   # entry box fill

    "bubble_bot":         "#101A3C",   # navy glass panel (bot messages)
    "bubble_bot_border":  "#28345F",   # faint lighter edge = "glass" rim
    "bubble_user":        "#7C70C4",   # muted lavender glass (user messages)
    "bubble_user_border": "#D6CFFF",   # bright lavender edge highlight

    "text_bot":       "#E9EBF9",
    "text_user":      "#FFFFFF",
    "text_muted":     "#7C87B8",
    "text_header":    "#F4F2FF",

    "accent":         "#C9BFFF",   # soft lavender — primary accent
    "accent_dark":    "#B0A3F2",   # pressed/active state
    "accent_soft":    "#1C2550",   # pill/tag backgrounds
    "accent_warn":    "#D6A85F",   # amber, used sparingly
    "online_dot":     "#8FE3B0",   # mint green status dot
    "scrollbar":      "#1B2450",
    "input_border":   "#232B57",
}

FONT_FAMILY_HEADER = "Georgia"       # a touch of classic elegance for the title
FONT_FAMILY_BODY = "Segoe UI"        # clean, modern, widely available
FONT_FAMILY_MONO = "Consolas"        # for the little "system" tags

BOT_NAME = "EVA"
CREATOR = "Faiza Ahmed Esha"
TAGLINE = "Intelligent Rule-Based Assistant"

# ------------------------------------------------------------------------------
# 2. SANITIZATION — strips punctuation/case noise so "Hi!", "hi.", "HI??" and
#    "hi" are all treated identically. This is what your earlier report was
#    about: punctuation was silently breaking exact-match checks (like
#    greetings and "I am fine.").
# ------------------------------------------------------------------------------
_PUNCT_PATTERN = re.compile(r"[^\w\s]")    # keep letters, numbers, and spaces only
_WHITESPACE_PATTERN = re.compile(r"\s+")


def sanitize(raw_text: str) -> str:
    text = raw_text.lower().strip()
    text = text.replace("'", "")               # "I'm" -> "im", "don't" -> "dont"
    text = _PUNCT_PATTERN.sub(" ", text)        # any remaining punctuation -> space
    text = _WHITESPACE_PATTERN.sub(" ", text).strip()
    return text


# ------------------------------------------------------------------------------
# 3. KNOWLEDGE BASE — the "Logic Skeleton"
#    Each entry: (list_of_trigger_keywords, response_or_callable)
#    A dictionary/list lookup is used instead of a long if-elif ladder,
#    exactly the anti-pattern this project is meant to teach us to avoid.
#
#    Tone: professional by default, with a light, occasional touch of wit —
#    not sarcastic on every single line.
# ------------------------------------------------------------------------------

GREETINGS = ["hi", "hello", "hey", "yo", "hola", "greetings", "sup", "good morning",
             "good afternoon", "good evening"]
FAREWELLS = ["bye", "goodbye", "exit", "quit", "see you", "later", "cya"]

KNOWLEDGE_BASE = [
    # --- Identity & small talk --------------------------------------------------
    (["your name", "who are you", "what are you called"],
     f"I'm {BOT_NAME} — a rule-based assistant built by {CREATOR}, an aspiring software "
     "developer. My replies come from clean if-else logic, not a live model."),

    (["what does eva stand for", "what does your name mean", "eva mean"],
     f"{BOT_NAME} is just my name — I'd rather be judged on how well my logic works "
     "than on what the letters stand for."),

    (["who made you", "who created you", "who built you", "who is your creator",
      "who developed you"],
     f"I was designed and built by {CREATOR} as a hands-on project in rule-based logic "
     "and conversational design."),

    (["how are you", "how re you", "how you doing", "how are things"],
     "Doing well, thank you — running smoothly with no errors so far. How about you?"),

    (["im fine", "i am fine", "im good", "i am good", "doing fine", "doing good",
      "im great", "i am great", "not bad", "pretty good", "fine thanks", "great thanks",
      "im ok", "i am okay", "im alright"],
     "Glad to hear that! Let me know if there's anything you'd like to ask me."),

    (["what can you do", "what do you do", "your purpose", "help"],
     "I can hold a focused conversation on a defined set of topics — greetings, small talk, "
     "core AI/ML concepts, and questions about this project. Ask away, and I'll tell you "
     "honestly if something's outside what I know."),

    (["thank", "thanks", "appreciate it"],
     "You're welcome! Happy to help."),

    (["love you", "i love you"],
     "That's kind of you to say — I'm a set of scripted responses, but I'll take the compliment."),

    (["joke", "make me laugh", "funny"],
     "Why do programmers prefer dark mode? Because light attracts bugs."),

    (["your age", "how old are you"],
     "I came into existence the moment this script started running — so, quite young, "
     "and entirely without a birthday."),

    (["favorite color", "favourite colour"],
     "Lavender — it's right there in my color palette."),

    (["bored", "i am bored", "im bored"],
     "You could ask me about AI, machine learning, or this project — or take a short break. "
     "Either works."),

    (["sad", "i am sad", "i feel down", "not feeling good", "im sad"],
     "I'm sorry to hear that. I'm a rule-based assistant, so I'm limited in how much I can "
     "help here — but talking to someone you trust is usually a good next step."),

    # --- About this project / creator ------------------------------------------
    (["this project", "what is this project", "about this project"],
     f"This is a personal project by {CREATOR}, built to practice control flow, "
     "decision-making logic, and rule-based conversational design in Python."),

    (["your creator background", "faiza", "esha"],
     f"{CREATOR} is an aspiring software developer — this chatbot is one of the projects "
     "on that journey."),

    # --- AI / ML concept questions ----------------------------------------------
    (["what is ai", "what is artificial intelligence"],
     "Artificial Intelligence is the broad field of building systems that perform tasks "
     "which normally require human-level thinking — reasoning, learning, or decision-making. "
     "I sit on the simple, deterministic end of that spectrum."),

    (["what is machine learning", "what is ml"],
     "Machine Learning is a subset of AI where systems learn patterns from data instead of "
     "following hard-coded rules. I don't do that myself — I run entirely on hard-coded rules."),

    (["what is deep learning", "what is a neural network", "neural network"],
     "Deep Learning uses layered neural networks to model complex patterns in data. "
     "It's the probabilistic side of AI; I represent the deterministic, rule-based side."),

    (["what is python", "why python"],
     "Python is the language powering me — readable syntax, a strong ecosystem, and a common "
     "choice for AI and software prototyping."),

    (["what is a chatbot", "define chatbot"],
     "A chatbot is software that simulates conversation. Rule-based chatbots, like me, match "
     "input to pre-written responses. Generative chatbots use language models to produce new "
     "replies on the fly."),

    (["what is nlp", "natural language processing"],
     "Natural Language Processing is the field focused on helping machines understand and "
     "generate human language. I use a small, literal slice of that idea: keyword matching."),

    (["ipo model", "input process output"],
     "The IPO model is Input -> Process -> Output. I sanitize your text (Input), match it "
     "against my knowledge base (Process), and return a response (Output) — then loop."),

    # --- Honest limitations (light wit, used sparingly) --------------------------
    (["read pdf", "read a pdf", "pdf file", "upload pdf", "open pdf"],
     "PDF reading isn't available yet — that capability is still under construction."),

    (["read image", "look at image", "see this picture", "analyze image", "upload photo",
      "vision"],
     "Image understanding is also under construction. Right now I only process typed text, "
     "matched against my existing rules."),

    (["are you real ai", "are you sentient", "are you conscious", "are you alive"],
     "Not in the way you might mean — I'm a dictionary lookup with a well-designed interface, "
     "not a thinking system."),

    (["can you learn", "do you learn", "will you remember me"],
     "I don't learn from conversations, and I won't remember this one after the window closes. "
     "Deterministic, and a little forgetful, by design."),

    (["weather", "what's the weather", "temperature outside"],
     "I'm not connected to any weather service, so I can't check that for you — a window "
     "might be the more reliable option."),

    (["time is it", "current time", "what time is it"],
     lambda: f"According to the system clock, it's "
             f"{datetime.datetime.now().strftime('%H:%M:%S')} on my end. Adjust for your timezone."),

    (["date today", "what is the date", "todays date"],
     lambda: f"Today is {datetime.datetime.now().strftime('%B %d, %Y')}, based on the system clock."),
]

FALLBACK_RESPONSES = [
    "I'm not able to help with that yet — it's outside my current knowledge base.",
    "That's not something I can answer right now. Try asking about AI, ML, or this project.",
    "I don't have a response for that one. I'm a rule-based assistant, so I only know what's "
    "explicitly programmed in.",
    "That wasn't something I recognized. Feel free to rephrase, or ask me something else.",
    "I can't help with that particular question — it isn't part of what I've been built to answer.",
]

GREETING_RESPONSES = [
    "Hello! I'm {bot}, a rule-based assistant. Ask me something, and I'll do my best to help.",
    "Hi there — {bot} here. I can answer questions on a defined set of topics; try me.",
    "Hey! {bot} is ready when you are.",
]

FAREWELL_RESPONSES = [
    "Goodbye! Thanks for stopping by.",
    "See you later — take care.",
    "Bye! It was good talking with you.",
]


def get_response(raw_text: str) -> str:
    """
    The Logic Engine.
    Sanitize -> Farewell check -> Greeting check -> Keyword match -> Fallback.
    Punctuation, casing, and extra whitespace are all normalized first, so
    "Hi!", "HELLO??" and "  hi " are treated the same as "hi".
    """
    text = sanitize(raw_text)
    if not text:
        return "You sent me nothing but whitespace. I need a bit more than that to work with."

    # Exit / farewell intent
    if any(word in text for word in FAREWELLS):
        return random.choice(FAREWELL_RESPONSES)

    # Greeting intent (exact word/phrase match, punctuation already stripped)
    if any(text == g or text.startswith(g + " ") for g in GREETINGS):
        return random.choice(GREETING_RESPONSES).format(bot=BOT_NAME)

    # Knowledge base keyword match
    for keywords, response in KNOWLEDGE_BASE:
        if any(sanitize(keyword) in text for keyword in keywords):
            return response() if callable(response) else response

    # Nothing matched — honest fallback
    return random.choice(FALLBACK_RESPONSES)


def is_exit_command(raw_text: str) -> bool:
    text = sanitize(raw_text)
    return text in FAREWELLS or text in ("exit", "close")


# ------------------------------------------------------------------------------
# 4. FRONT END — Tkinter GUI (Midnight Navy + Lavender Glass)
# ------------------------------------------------------------------------------
class EVAApp:
    def __init__(self, root):
        self.root = root
        self.root.title(f"{BOT_NAME} — {TAGLINE}")
        self.root.geometry("560x720")
        self.root.minsize(420, 560)
        self.root.configure(bg=THEME["bg_app"])

        self._build_fonts()
        self._build_header()
        self._build_chat_area()
        self._build_input_bar()

        self._bot_say(
            f"Hi, I'm {BOT_NAME} — a rule-based assistant. Ask me something, and I'll let "
            "you know if it's outside what I currently understand.",
            initial=True,
        )

    # -- setup helpers -----------------------------------------------------
    def _build_fonts(self):
        available = set(tkfont.families())
        header_family = FONT_FAMILY_HEADER if FONT_FAMILY_HEADER in available else "Times New Roman"
        body_family = FONT_FAMILY_BODY if FONT_FAMILY_BODY in available else "Helvetica"
        mono_family = FONT_FAMILY_MONO if FONT_FAMILY_MONO in available else "Courier New"

        self.font_title = tkfont.Font(family=header_family, size=18, weight="bold")
        self.font_subtitle = tkfont.Font(family=body_family, size=9)
        self.font_bubble = tkfont.Font(family=body_family, size=11)
        self.font_meta = tkfont.Font(family=mono_family, size=8)
        self.font_input = tkfont.Font(family=body_family, size=11)
        self.font_send = tkfont.Font(family=body_family, size=11, weight="bold")

    def _build_header(self):
        header = tk.Frame(self.root, bg=THEME["bg_header"], height=78)
        header.pack(side="top", fill="x")
        header.pack_propagate(False)

        left = tk.Frame(header, bg=THEME["bg_header"])
        left.pack(side="left", padx=18, pady=10)

        title_row = tk.Frame(left, bg=THEME["bg_header"])
        title_row.pack(anchor="w")

        dot = tk.Canvas(title_row, width=10, height=10, bg=THEME["bg_header"],
                         highlightthickness=0)
        dot.create_oval(1, 1, 9, 9, fill=THEME["online_dot"], outline="")
        dot.pack(side="left", padx=(0, 8))

        tk.Label(title_row, text=BOT_NAME, font=self.font_title,
                 fg=THEME["text_header"], bg=THEME["bg_header"]).pack(side="left")

        tk.Label(left, text=TAGLINE, font=self.font_subtitle, fg=THEME["text_muted"],
                 bg=THEME["bg_header"]).pack(anchor="w", pady=(2, 0))

        tag = tk.Label(header, text="ONLINE", font=self.font_meta,
                        fg=THEME["online_dot"], bg=THEME["accent_soft"], padx=10, pady=4)
        tag.pack(side="right", padx=18)

        # subtle glass-like divider (muted rather than a bright solid bar)
        tk.Frame(self.root, bg=THEME["input_border"], height=1).pack(side="top", fill="x")

    def _build_chat_area(self):
        outer = tk.Frame(self.root, bg=THEME["bg_chat"])
        outer.pack(side="top", fill="both", expand=True)

        self.canvas = tk.Canvas(outer, bg=THEME["bg_chat"], highlightthickness=0)
        scrollbar = tk.Scrollbar(outer, orient="vertical", command=self.canvas.yview,
                                  bg=THEME["scrollbar"], troughcolor=THEME["bg_chat"],
                                  activebackground=THEME["accent"])
        self.canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True, padx=(10, 0))

        self.chat_frame = tk.Frame(self.canvas, bg=THEME["bg_chat"])
        self.chat_window = self.canvas.create_window((0, 0), window=self.chat_frame, anchor="nw")

        self.chat_frame.bind("<Configure>",
                              lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", self._on_canvas_resize)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", lambda e: self.canvas.yview_scroll(-1, "units"))
        self.canvas.bind_all("<Button-5>", lambda e: self.canvas.yview_scroll(1, "units"))

    def _on_canvas_resize(self, event):
        self.canvas.itemconfig(self.chat_window, width=event.width)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _build_input_bar(self):
        bar = tk.Frame(self.root, bg=THEME["bg_input"], height=64)
        bar.pack(side="bottom", fill="x")
        bar.pack_propagate(False)

        # "glass" border simulated with a 1px frame in a lighter tone, wrapping
        # a slightly recessed inner field.
        border_wrap = tk.Frame(bar, bg=THEME["input_border"])
        border_wrap.pack(side="left", fill="both", expand=True, padx=(16, 8), pady=12)

        field_wrap = tk.Frame(border_wrap, bg=THEME["bg_input_field"])
        field_wrap.pack(fill="both", expand=True, padx=1, pady=1)

        self.entry = tk.Entry(field_wrap, font=self.font_input, bg=THEME["bg_input_field"],
                               fg=THEME["text_bot"], insertbackground=THEME["text_bot"],
                               relief="flat", bd=0)
        self.entry.pack(fill="both", expand=True, padx=12, pady=8)
        self.entry.focus_set()
        self.entry.bind("<Return>", lambda e: self._on_send())

        send_btn = tk.Button(bar, text="Send", font=self.font_send, fg=THEME["bg_app"],
                              bg=THEME["accent"], activebackground=THEME["accent_dark"],
                              activeforeground=THEME["bg_app"], relief="flat", bd=0,
                              padx=20, cursor="hand2", command=self._on_send)
        send_btn.pack(side="right", padx=(0, 16), pady=12)

    # -- chat logic ----------------------------------------------------------
    def _on_send(self):
        text = self.entry.get().strip()
        if not text:
            return
        self.entry.delete(0, "end")
        self._user_say(text)

        if is_exit_command(text):
            self.root.after(500, self._bot_say, random.choice(FAREWELL_RESPONSES))
            self.root.after(1800, self.root.destroy)
            return

        # tiny artificial delay so it doesn't feel instant/robotic
        self.root.after(350, lambda: self._bot_say(get_response(text)))

    def _user_say(self, text):
        self._add_bubble(text, sender="user")

    def _bot_say(self, text, initial=False):
        self._add_bubble(text, sender="bot")

    def _add_bubble(self, text, sender="bot"):
        is_user = sender == "user"
        row = tk.Frame(self.chat_frame, bg=THEME["bg_chat"])
        row.pack(fill="x", pady=6, padx=8, anchor="e" if is_user else "w")

        bubble_bg = THEME["bubble_user"] if is_user else THEME["bubble_bot"]
        border_color = THEME["bubble_user_border"] if is_user else THEME["bubble_bot_border"]
        text_fg = THEME["text_user"] if is_user else THEME["text_bot"]
        pack_side = "right" if is_user else "left"      # valid: left/right/top/bottom
        pack_anchor = "e" if is_user else "w"            # valid: n/s/e/w/ne/nw/se/sw/center
        justify = "right" if is_user else "left"

        col = tk.Frame(row, bg=THEME["bg_chat"])
        col.pack(side=pack_side, anchor=pack_anchor)

        label_name = tk.Label(col, text=("You" if is_user else BOT_NAME),
                               font=self.font_meta, fg=THEME["text_muted"], bg=THEME["bg_chat"])
        label_name.pack(anchor=pack_anchor, padx=4)

        # Glass-panel effect: a 1px lighter "edge" frame wrapping the bubble.
        border = tk.Frame(col, bg=border_color)
        border.pack(anchor=pack_anchor)

        inner = tk.Frame(border, bg=bubble_bg)
        inner.pack(padx=1, pady=1)

        bubble = tk.Label(inner, text=text, font=self.font_bubble, fg=text_fg, bg=bubble_bg,
                           wraplength=360, justify=justify, padx=14, pady=10)
        bubble.pack()

        self.root.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.canvas.yview_moveto(1.0)


def main():
    root = tk.Tk()
    try:
        root.iconbitmap(default="")
    except Exception:
        pass
    app = EVAApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()