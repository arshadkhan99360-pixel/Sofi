# Sofi v2.0 Android Voice

from kivy.utils import platform


class SofiVoice:

    def __init__(self):
        self.available = False

        if platform == "android":
            self.available = True


    def speak(self, text):

        if not self.available:
            print("Sofi Voice:", text)
            return

        try:
            from jnius import autoclass

            PythonActivity = autoclass(
                "org.kivy.android.PythonActivity"
            )

            Intent = autoclass(
                "android.content.Intent"
            )

            intent = Intent(
                "android.intent.action.SEND"
            )

            print("Voice request:", text)

        except Exception as e:
            print("Voice error:", e)