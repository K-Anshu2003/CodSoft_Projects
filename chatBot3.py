import tkinter as tk
from tkinter import scrolledtext
import re

# ----- Chatbot Logic ----- #
main_topics = {
    "account": ["login", "password", "update"],
    "payment": ["refund", "invoice", "method"],
    "support": ["technical", "general", "feedback"],
    "services": ["subscription", "features", "cancel"],
    "delivery": ["tracking", "delay", "address"],
    "product": ["warranty", "availability", "specification"],
    "membership": ["benefits", "upgrade", "cancellation"]
}

sub_topic_responses = {
    "account": {
        "login": "For login help, go to Account > Login Help.",
        "password": "Reset your password via Account > Security Settings.",
        "update": "You can update account info in Account > Profile."
    },
    "payment": {
        "refund": "For refunds, go to Billing > Disputes and submit the form.",
        "invoice": "Invoices can be downloaded from Billing > History.",
        "method": "Add or remove payment methods in Billing > Payment Options."
    },
    "support": {
        "technical": "For tech issues, contact Support > Troubleshooting.",
        "general": "General support is available via Support > Contact Us.",
        "feedback": "Submit feedback in Support > Suggestions."
    },
    "services": {
        "subscription": "Manage subscriptions in Services > Plans.",
        "features": "Feature details are listed in Services > Catalog.",
        "cancel": "To cancel a service, go to Services > Manage > Cancel."
    },
    "delivery": {
        "tracking": "Track your order in Delivery > Track My Package.",
        "delay": "Delays are updated under Delivery > Notifications.",
        "address": "Modify your delivery address in Delivery > Address Book."
    },
    "product": {
        "warranty": "Warranty info is found under Product > Warranty Center.",
        "availability": "Check availability via Product > Stock Status.",
        "specification": "Product specs are listed in Product > Details."
    },
    "membership": {
        "benefits": "View membership perks in Membership > Benefits.",
        "upgrade": "Upgrade options are under Membership > Upgrade Now.",
        "cancellation": "Cancel your membership in Membership > Settings."
    }
}

current_topic = None

def chatbot_response(user_input):
    global current_topic
    user_input = user_input.lower()

    if user_input in ["yes", "yeah", "yep", "sure", "another", "continue"]:
        current_topic = None
        return "Great! 😊 Please choose a topic:\n- " + "\n- ".join(main_topics.keys())

    if user_input in ["no", "nope", "nah"]:
        current_topic = None
        return "It was a pleasure chatting with you! 😊 Type 'yes' anytime you need help again."

    if re.search(r"\b(hi|hello|hey|hii|hlo)\b", user_input):
        current_topic = None
        return "Hi there! 😊 I’m your Helpdesk Bot.\nChoose a topic:\n- " + "\n- ".join(main_topics.keys())

    for topic in main_topics:
        if topic in user_input:
            current_topic = topic
            options = ", ".join(main_topics[topic])
            return f"What would you like help with in {topic.title()}?\nOptions: {options}"

    if current_topic:
        for sub in main_topics[current_topic]:
            if sub in user_input:
                response = sub_topic_responses[current_topic][sub]
                current_topic = None
                return response + "\nWould you like help with another topic?"
        options = ", ".join(main_topics[current_topic])
        return f"Hmm... Please choose one of these options in {current_topic.title()}: {options}"

    return "I'm not sure I understood that. Try saying 'Hello' to begin. 🙂"

# ----- GUI Setup ----- #
def send_message():
    user_text = entry.get().strip()
    if not user_text:
        return
    entry.delete(0, tk.END)
    display_message("You: " + user_text, "user")
    bot_text = chatbot_response(user_text)
    display_message("Bot: " + bot_text, "bot")

def display_message(msg, sender):
    tag = "right" if sender == "user" else "left"
    chat_area.config(state="normal")
    chat_area.insert(tk.END, msg + "\n\n", tag)
    chat_area.config(state="disabled")
    chat_area.yview(tk.END)

root = tk.Tk()
root.title("Helpdesk Bot")
root.geometry("700x600")
root.configure(bg="#f2f6fc")

font_style = ("Segoe UI", 11)

# Chat Area
chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=font_style, bg="white", fg="#222")
chat_area.pack(padx=10, pady=(10,5), fill="both", expand=True)
chat_area.tag_configure("left", justify="left", lmargin1=10, rmargin=40, background="#ffffff", spacing3=3)
chat_area.tag_configure("right", justify="right", lmargin1=40, rmargin=10, background="#dcf8c6", spacing3=3)
chat_area.config(state="disabled")

# Input Area
input_frame = tk.Frame(root, bg="#f2f6fc")
input_frame.pack(side="bottom", fill="x", padx=10, pady=10)

entry = tk.Entry(input_frame, font=font_style, bg="white", fg="#333", relief=tk.SOLID, bd=1)
entry.pack(side="left", fill="x", expand=True, ipady=6)

send_btn = tk.Button(input_frame, text="Send", font=("Segoe UI", 10, "bold"),
                     bg="#075e54", fg="white", activebackground="#25d366",
                     relief=tk.RAISED, bd=0, command=send_message)
send_btn.pack(side="right", ipadx=12, ipady=6)

# Initial Message
display_message("Bot: Hi there! 😊 I’m your Helpdesk Bot.\nChoose a topic:\n- " + "\n- ".join(main_topics.keys()), "bot")

root.mainloop()