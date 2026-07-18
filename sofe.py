from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
import json
from datetime import datetime

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button


# ---------- Load memory ----------
try:
    with open("memory.json", "r") as file:
        memory = json.load(file)
except:
    memory = {}

# ---------- Ask name only once ----------
if "user_name" not in memory:
    memory["user_name"] = input("What is your name? ")

    with open("memory.json", "w") as file:
        json.dump(memory, file, indent=4)

name = memory["user_name"]


# ---------- Sofi's Brain ----------
def get_response(question):
    question = question.lower()

    if question == "hello":
        return f"Hello, {name}!"

    elif question == "how are you":
        return "I'm doing well. How are you?"

    elif question == "time":
        return datetime.now().strftime("%I:%M %p")

    elif question == "date":
        return datetime.now().strftime("%d %B %Y")

    elif question == "what is your name":
        return "My name is Sofi."

    elif question == "what is my name":
        return f"Your name is {name}."

    elif question in memory:
        return memory[question]

    else:
        return "I don't know that yet. Teach me by typing:\nteach: your answer"


# ---------- GUI ----------
class SofiApp(App):

    def build(self):
        layout = BoxLayout(
            orientation="vertical",
            padding=10,
            spacing=10
        )

        self.chat = Label(
            text=f"Hello {name}! I am Sofi.",
            halign="left",
            valign="top"
        )

        self.chat.bind(size=self.chat.setter("text_size"))

        self.input = TextInput(
            multiline=False,
            hint_text="Type a message..."
        )

        button = Button(text="Send")
        button.bind(on_press=self.send_message)

        layout.add_widget(self.chat)
        layout.add_widget(self.input)
        layout.add_widget(button)

        return layout

    def send_message(self, instance):
        message = self.input.text.strip()

        if message == "":
            return

        # Teach Sofi
        if message.lower().startswith("teach:"):
            answer = message[6:].strip()

            if len(answer) > 0:
                last_question = memory.get("last_question", "")

                if last_question:
                    memory[last_question] = answer

                    with open("memory.json", "w") as file:
                        json.dump(memory, file, indent=4)

                    reply = "Thanks! I'll remember that."

                else:
                    reply = "I don't know what you're teaching."

            else:
                reply = "Please type an answer."

        else:
            memory["last_question"] = message.lower()

            reply = get_response(message)

        self.chat.text += f"\n\nYou: {message}\nSofi: {reply}"

        self.input.text = ""


SofiApp().run()