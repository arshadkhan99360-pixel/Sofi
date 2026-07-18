from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.scrollview import MDScrollView

from voice import SofiVoice
from speech import SofiSpeech


class SofiGUI(MDBoxLayout):

    def __init__(self, brain, **kwargs):

        super().__init__(**kwargs)

        self.brain = brain

        # Voice systems
        self.voice = SofiVoice()
        self.speech = SofiSpeech()


        self.orientation = "vertical"
        self.padding = 20
        self.spacing = 10


        # Chat area

        self.chat = MDLabel(
            text="Sofi v2.0 Online\n\n",
            size_hint_y=None,
            valign="top"
        )

        self.chat.bind(
            texture_size=self.chat.setter("size")
        )


        scroll = MDScrollView()
        scroll.add_widget(self.chat)

        self.add_widget(scroll)


        # Text input

        self.input_box = MDTextField(
            hint_text="Talk to Sofi...",
            mode="rectangle",
            size_hint_y=None,
            height=60
        )

        self.add_widget(self.input_box)


        # Send button

        self.send_button = MDRaisedButton(
            text="SEND",
            size_hint_y=None,
            height=50,
            on_release=self.send_message
        )

        self.add_widget(self.send_button)


        # Mic button

        self.mic_button = MDRaisedButton(
            text="MIC",
            size_hint_y=None,
            height=50,
            on_release=self.voice_input
        )

        self.add_widget(self.mic_button)



    def send_message(self, instance):

        text = self.input_box.text.strip()

        if not text:
            return


        self.chat.text += (
            f"\nYou: {text}\n"
        )


        response = self.brain.think(text)


        self.chat.text += (
            f"Sofi: {response}\n"
        )


        self.voice.speak(response)


        self.input_box.text = ""



    def voice_input(self, instance):

        self.chat.text += (
            "\nSofi: Listening...\n"
        )

        self.speech.listen(
            self.process_voice
        )



    def process_voice(self, text):

        if text:

            self.chat.text += (
                f"\nYou: {text}\n"
            )


            response = self.brain.think(text)


            self.chat.text += (
                f"Sofi: {response}\n"
            )


            self.voice.speak(response)